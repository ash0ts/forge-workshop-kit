"""Publish saved examples through the public, Weave-backed EvalTable API."""

from collections.abc import Mapping, Sequence

from .media import is_image, map_values, wandb_value
from .session import digest


class EvalTableNeedsReview(RuntimeError):
    pass


class EvalTableMarkerMissing(RuntimeError):
    pass


def _flatten(value, prefix, result):
    if isinstance(value, dict) and value and not is_image(value):
        for key, child in value.items():
            _flatten(child, prefix + '.' + str(key), result)
    else:
        if prefix in result:
            raise ValueError('Evaluation columns collide at ' + prefix)
        result[prefix] = value


def _plain_rows(rows):
    identities = [row['case_id'] for row in rows]
    if not identities or any(not isinstance(value, str) or not value for value in identities):
        raise ValueError('An EvalTable needs nonempty string case identities.')
    if len(set(identities)) != len(identities):
        raise ValueError('Each version needs one saved row per case identity.')
    prepared = []
    for row in rows:
        inputs = {'case_id': row['case_id']}
        _flatten(row['input'], 'input', inputs)
        outputs = {}
        for field in ('prediction', 'target', 'evidence'):
            _flatten(row.get(field), field, outputs)
        scores = {'error': row.get('error'), **row.get('scores', {})}
        if any(not isinstance(key, str) or not key.strip() for key in scores):
            raise ValueError('Score names must be nonempty strings.')
        for key, value in scores.items():
            if value is not None and type(value) not in (bool, int, float, str):
                raise ValueError('EvalTable score ' + key + ' must be a scalar or missing.')
        if (set(inputs) | set(outputs)) & set(scores):
            raise ValueError('Score names must not collide with input or output columns.')
        prepared.append({'inputs': inputs, 'outputs': outputs, 'scores': scores})
    return prepared


def column_roles(rows):
    """Column names are also saved for the native comparison's initial layout."""
    prepared = _plain_rows(rows)
    inputs = ['case_id'] + sorted({key for row in prepared for key in row['inputs']} - {'case_id'})
    output_names = {key for row in prepared for key in row['outputs']}
    outputs = sorted(output_names, key=lambda key: (
        {'prediction': 0, 'target': 1, 'evidence': 2}.get(key.split('.')[0], 3), key))
    scores = sorted({key for row in prepared for key in row['scores']})
    columns = inputs + outputs + scores
    if len(set(columns)) != len(columns):
        raise ValueError('Evaluation column roles collide across examples.')
    images = sorted({key for row in prepared for role in ('inputs', 'outputs')
                     for key, value in row[role].items() if is_image(value)})
    return {'input_columns': inputs, 'output_columns': outputs,
            'score_columns': scores, 'image_columns': images}


def eval_table_data(rows):
    """Keep stable case inputs, individual scores, and actual image cells."""
    prepared = _plain_rows(rows)
    roles = column_roles(rows)
    roles.pop('image_columns')
    columns = roles['input_columns'] + roles['output_columns'] + roles['score_columns']
    data = []
    for row in prepared:
        values = {**row['inputs'], **row['outputs'], **row['scores']}
        data.append([wandb_value(values.get(column)) for column in columns])
    return {'columns': columns, 'data': data, **roles}


def _request_digest(run, rows, name):
    # A restored image can live under another absolute directory, with identical bytes.
    portable = map_values(rows, lambda value: {k: v for k, v in value.items() if k != 'path'})
    return digest({'project': run.entity + '/' + run.project, 'run_id': run.id,
                   'name': name, 'rows': portable, 'format': 1, 'backend': 'weave'})


def _matches_non_media(actual, expected):
    if isinstance(expected, dict):
        if not isinstance(actual, Mapping) or set(actual) != set(expected):
            return False
        # Image cells are checked in the native view; do not download every image
        # while retrying row publication. All other values are compared exactly.
        return all(is_image(value) or _matches_non_media(actual[key], value)
                   for key, value in expected.items())
    if isinstance(expected, list):
        return (isinstance(actual, Sequence) and not isinstance(actual, str)
                and len(actual) == len(expected)
                and all(is_image(value) or _matches_non_media(actual[index], value)
                        for index, value in enumerate(expected)))
    if isinstance(expected, bool) or isinstance(actual, bool):
        return type(actual) is type(expected) and actual == expected
    return actual == expected


def stored_eval_calls(client, *, filter, limit, columns):
    """Read call JSON without materializing the SDK's custom image objects."""
    return client.server.calls_query_stream({
        'project_id': client.project_id, 'filter': filter, 'limit': limit,
        'columns': columns, 'expand_columns': None,
        'return_expanded_column_values': False,
    })


def verify_eval_table(client, marker, rows):
    """Read every saved row and score without running a scorer or downloading images."""
    if marker.get('_type') != 'eval-table' or not marker.get('evaluate_call_id'):
        raise ValueError('Expected an EvalTable marker returned by the W&B SDK.')
    client.flush()
    parents = list(stored_eval_calls(client, filter={'call_ids': [marker['evaluate_call_id']]},
        limit=1, columns=['id', 'ended_at', 'exception']))
    if len(parents) != 1:
        raise RuntimeError('The saved evaluation is not available yet. Retry publication readback.')
    call = parents[0]
    if call.ended_at is None or call.exception is not None:
        raise RuntimeError('The saved evaluation is unfinished or failed. Retry publication readback.')
    expected = {row['inputs']['case_id']: row for row in _plain_rows(rows)}
    roles = column_roles(rows)
    score_names = sorted({key for row in expected.values() for key in row['scores']})
    found = set()
    children = stored_eval_calls(client,
        filter={'parent_ids': [marker['evaluate_call_id']]}, limit=len(rows) + 2,
        columns=['id', 'parent_id', 'op_name', 'ended_at', 'exception', 'inputs', 'output'])
    for child in children:
        if child.op_name.split('/op/')[-1].split(':')[0] != 'Evaluation.predict_and_score':
            continue
        if child.ended_at is None or child.exception is not None:
            raise RuntimeError('A saved evaluation example is unfinished or failed.')
        example = child.inputs.get('example', {})
        case_id = example.get('case_id')
        if case_id not in expected or case_id in found:
            raise ValueError('Stored evaluation case identities differ from the saved examples.')
        output = child.output
        if not isinstance(output, Mapping):
            raise TypeError('A stored evaluation example has no score output.')
        expected_inputs = {key: expected[case_id]['inputs'].get(key) for key in roles['input_columns']}
        expected_outputs = {key: expected[case_id]['outputs'].get(key) for key in roles['output_columns']}
        if not _matches_non_media(example, expected_inputs):
            raise ValueError('Stored evaluation inputs differ from the saved examples.')
        if not _matches_non_media(output.get('output'), expected_outputs):
            raise ValueError('Stored evaluation outputs differ from the saved examples.')
        expected_scores = {key: expected[case_id]['scores'].get(key) for key in score_names}
        if not _matches_non_media(output.get('scores', {}), expected_scores):
            raise ValueError('Stored evaluation scores differ from the saved examples.')
        found.add(case_id)
    if found != set(expected) or marker.get('nrows') != len(rows):
        raise RuntimeError('Stored evaluation rows are incomplete. Retry publication readback.')
    return {'row_count': len(found), 'verified': True,
            'verification': 'Completed evaluation; all row identities, non-image inputs/outputs, and scores',
            'image_content_verified': False}


def verify_run_history(run_path, name, marker, *, api=None):
    """Check the native panel's run marker after the logging run has finished."""
    import wandb
    stored = (api or wandb.Api()).run(run_path)
    for row in stored.scan_history(keys=[name], page_size=100):
        value = row.get(name)
        if isinstance(value, Mapping) and all(value.get(key) == item for key, item in marker.items()):
            return {'history_verified': True, 'history_key': name}
    raise EvalTableMarkerMissing('The EvalTable run marker is not stored yet. Retry publication readback; '
                                 'if needed, log the saved marker without recreating the evaluation.')


def publish_eval_table(run, rows, name, *, receipt=None, save, client=None):
    """Save once, then retry readback without recreating an evaluation.

    ``save`` must durably write the supplied receipt before returning. An interrupted
    write without a saved SDK marker needs review; it is never automatically resent.
    Image paths must already be bound to the current workspace.
    """
    import weave

    import wandb

    receipt = receipt if receipt is not None else {}
    request = _request_digest(run, rows, name)
    if receipt.get('request_digest') not in (None, request):
        raise ValueError('The EvalTable publication request changed. Use a new receipt.')
    if receipt.get('status') in ('writing', 'uncertain') and not receipt.get('marker'):
        raise EvalTableNeedsReview(
            'The previous EvalTable export has an uncertain outcome. Check its run history '
            'for the saved evaluate_call_id before retrying; the experiment need not run again.')
    if client is None:
        client = weave.init(run.entity + '/' + run.project)
    receipt['column_roles'] = column_roles(rows)
    if not receipt.get('marker'):
        table = wandb.EvalTable(**eval_table_data(rows), backend='weave',
                               unsupported_media_mode='raise')
        receipt.update(request_digest=request, backend='weave', status='writing', verified=False)
        save(dict(receipt))
        try:
            run.log({name: table})
            marker = table.to_json(run)
            if marker.get('_type') != 'eval-table' or not marker.get('evaluate_call_id'):
                raise ValueError('W&B did not return a Weave-backed EvalTable marker.')
        except Exception:
            receipt.update(status='uncertain')
            save(dict(receipt))
            raise
        receipt.update(marker=marker, evaluate_call_id=marker['evaluate_call_id'], status='exported')
        save(dict(receipt))
    try:
        verified = verify_eval_table(client, receipt['marker'], rows)
    except Exception as error:
        receipt.update(status='readback_pending', verified=False, error=str(error)[:400])
        save(dict(receipt))
        raise
    receipt.update(verified, status='published')
    receipt.pop('error', None)
    save(dict(receipt))
    return receipt
