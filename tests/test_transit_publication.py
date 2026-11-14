"""The mixed scenario outputs must remain usable in native evaluation columns."""
import json

import wandb

from forge_workshop_kit import WorkshopSession, transit, transit_workshop
from forge_workshop_kit.eval_tables import eval_table_data


def test_transit_comparison_has_stable_native_columns_and_lossless_answers(tmp_path):
    session = WorkshopSession('participant/transit', 'transit-factory', state_dir=tmp_path)
    sources = transit.worked_sources(2)
    result = transit.evaluate(sources, order=2)
    result['stage_id'] = 'saved-evaluation'
    result['rows'][0]['scores']['participant_departure_check'] = 1.0
    with session.transaction() as state:
        state['factory_workshop'] = {'frozen': {'with-memory': {'fingerprint': 'frozen-source'}},
                                    'base_release': {'label': 'team'}}
    rows = transit_workshop._comparison_rows(session, 'with-memory', result)
    ordinary = wandb.Table(columns=list(rows[0]), data=[list(row.values()) for row in rows])
    native = eval_table_data(rows)
    native_table = wandb.Table(columns=native['columns'], data=native['data'])
    assert len(ordinary.data) == len(native_table.data) == 18
    for displayed, original in zip(rows, result['rows'], strict=True):
        assert json.loads(displayed['input']['arguments']) == original['inputs']['arguments']
        assert json.loads(displayed['prediction']['actual']) == original['outputs'].get('prediction')
        assert json.loads(displayed['target']) == original['outputs'].get('expected')
        assert displayed['scores']['pass_rate'] == original['scores']['scenario_pass']
    assert rows[-1]['prediction']['participant_departure_check'] == 'null'
