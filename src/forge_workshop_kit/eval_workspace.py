"""Saved Forge workspace for comparing the same cases across evaluated versions."""
import json
from collections.abc import Mapping

from .eval_tables import stored_eval_calls
from .session import digest


def native_panel(name, run_ids, columns=None, evaluation_call_ids=()):
    """Run IDs here are GraphQL identities, not the short IDs in a run URL."""
    columns = columns or {}
    outputs = columns.get('output_columns', [])
    # EvalTable wraps model values in `output`; the grid adds its own `output`.
    # Keep group keys and current leaves for frontends on either side of the
    # group-visibility rollout. Evidence remains available in row details.
    visibility = {}
    for key in outputs:
        if key == 'evidence' or key.startswith('evidence.'):
            group = 'output.output.' + key
            visibility[group] = False
            visibility.update({f'{group}.{call_id}': False for call_id in evaluation_call_ids})
    widths = {'inputs.case_id': 180}
    for key in columns.get('image_columns', []):
        prefix = 'inputs.' if key in columns.get('input_columns', []) else 'output.output.'
        group = prefix + key
        widths[group] = 240
        if prefix == 'output.output.':
            widths.update({f'{group}.{call_id}': 240 for call_id in evaluation_call_ids})
    return {
        'evalName': name, 'evalTableType': 'eval-table',
        'referenceRunId': run_ids[0],
        'comparedEvals': [{'runId': value} for value in run_ids[1:]],
        'aggregatedScoresCollapsed': False,
        'rowSize': 'large' if columns.get('image_columns') else 'medium', 'pageSize': 10,
        'columnVisibility': visibility, 'columnWidths': widths,
    }


def comparison_columns(session, records):
    """Older exports recover their column names from one saved example per version."""
    result = {key: set() for key in ('input_columns', 'output_columns', 'score_columns', 'image_columns')}
    client = None
    for record in records:
        roles = record.get('native_transport', {}).get('column_roles')
        if roles is None:
            if client is None:
                import weave
                client = weave.init(session.project)
            calls = stored_eval_calls(client,
                filter={'parent_ids': [record['native']['evaluate_call_id']]}, limit=2,
                columns=['op_name', 'inputs', 'output'])
            roles = None
            for call in calls:
                if call.op_name.split('/op/')[-1].split(':')[0] != 'Evaluation.predict_and_score':
                    continue
                if not isinstance(call.output, Mapping):
                    continue
                outputs = call.output.get('output', {})
                inputs = call.inputs.get('example', {})
                roles = {'input_columns': list(inputs), 'output_columns': list(outputs),
                         'score_columns': list(call.output.get('scores', {})), 'image_columns': []}
                # Reading keys does not download all the image values in an older export.
                break
            if roles is None:
                raise RuntimeError('Saved EvalTable columns are not available yet. Retry publication readback.')
        for key, values in result.items():
            values.update(roles.get(key, []))
    return {key: sorted(values) for key, values in result.items()}


def publish_workspace(session, name, records, *, previous=None, save=lambda value: None):
    import wandb_workspaces.workspaces as ws
    from wandb_workspaces.reports.v2.interface import UnknownPanel

    import wandb

    ready = [row for row in records.values()
             if row.get('native_verified') and row.get('native_status') == 'published']
    if not ready or len(ready) != len(records):
        return {'status': 'pending', 'reason': 'Publish and verify every version before comparing them.'}
    columns = comparison_columns(session, ready)
    signature = digest({'versions': [[r['run_id'], r['native']['evaluate_call_id']] for r in ready],
                        'columns': columns, 'layout_version': 3})
    if previous and previous.get('status') == 'published' and previous.get('signature') == signature:
        return previous
    entity, project = session.project.split('/')
    api = wandb.Api()
    ids = [r['run_id'] for r in ready]
    gids = [api.run(f'{session.project}/{run_id}')._attrs['id'] for run_id in ids]
    config = native_panel(name, gids, columns, [r['native']['evaluate_call_id'] for r in ready])
    title = f'{name} / {session.workspace_id[:8]}'
    sections = [ws.Section(name='Compare the same cases', is_open=True,
        panels=[UnknownPanel(viewType='Evaluation Tables', config=config,
                             layout={'x': 0, 'y': 0, 'w': 24, 'h': 14})])]
    settings = ws.RunsetSettings(filters=' or '.join(f"ID = '{value}'" for value in ids), baseline_run=ids[0])
    old_url = (previous or {}).get('url')
    if old_url:
        view = ws.Workspace.from_url(old_url.replace('https://forge.coreweave.com/wandb/', 'https://wandb.ai/', 1))
        view.sections, view.runset_settings = sections, settings
        view.save()
    else:
        view = ws.Workspace(entity=entity, project=project, name=title,
                            sections=sections, runset_settings=settings)
        view.save_as_new_view()
    url = f'https://forge.coreweave.com/wandb/{session.project}?' + view.url.split('?', 1)[1]
    result = {'status': 'created', 'url': url, 'signature': signature}
    save(result)
    # Workspace SDK currently drops fields not described by its generic panel model.
    # Write the native panel configuration, then read it back before linking it.
    wire = ws.Workspace.from_url(view.url)._spec
    section = wire['spec']['section']
    section['runSets'][0].update(baselineRunId=gids[0], pinnedRunIds=[gids[0]])
    bank = section['panelBankConfig']['sections'][0]
    bank['panels'] = [{'__id__': 'workshop-evaluation', 'viewType': 'Evaluation Tables',
                       'isAuto': False, 'config': config,
                       'layout': {'x': 0, 'y': 0, 'w': 24, 'h': 14}}]
    bank['flowConfig'].update(columnsPerPage=1, rowsPerPage=1, boxHeight=1050)
    query = '''mutation($id:ID,$entityName:String,$projectName:String,$type:String,
      $name:String,$displayName:String,$spec:String){upsertView(input:{id:$id,
      entityName:$entityName,projectName:$projectName,type:$type,name:$name,
      displayName:$displayName,spec:$spec}){view{id name}}}'''
    api._service_api.execute_graphql(query, {'id': wire['id'], 'entityName': entity,
        'projectName': project, 'type': 'project-view', 'name': wire['name'],
        'displayName': wire['displayName'], 'spec': json.dumps(wire['spec'])})
    stored = ws.Workspace.from_url(view.url)._spec['spec']['section']
    if stored['panelBankConfig']['sections'][0]['panels'][0]['config'] != config:
        raise RuntimeError('Forge did not retain the comparison settings. Retry publication from saved results.')
    result.update(status='published', config=config)
    save(result)
    return result
