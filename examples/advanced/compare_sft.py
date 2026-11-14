"""Optional base/checkpoint evaluation. Plan first, explicitly run, then publish saved results."""

import argparse
import json
from pathlib import Path

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.advanced_comparison import (
    comparison_plan,
    publish_comparison_result,
    run_comparison,
)
from forge_workshop_kit.session import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['plan', 'run', 'publish'])
    parser.add_argument('--project', required=True)
    parser.add_argument('--state', required=True)
    parser.add_argument('--spec', type=Path, help='Frozen cases, intents and priced model identities')
    parser.add_argument('--plan', type=Path, default=Path('sft-comparison-plan.json'))
    parser.add_argument('--forecast', type=Path)
    parser.add_argument('--approve-usd', type=float)
    parser.add_argument('--identity', help='Saved advanced-sft/... identity for publication only')
    args = parser.parse_args()
    if args.action == 'plan':
        if args.spec is None:
            parser.error('Planning requires --spec; no provider calls are made')
        spec = json.loads(args.spec.read_text())
        plan = comparison_plan(spec['cases'], spec['intents'], spec['models'],
                               max_tokens=spec.get('max_tokens', 512))
        write_json(args.plan, plan)
        print(json.dumps({'file': str(args.plan), 'requests': len(plan['calls']),
                          'maximum_usd': plan['maximum_usd']}))
        return
    identity = json.loads((Path(args.state) / 'identity.json').read_text())
    session = WorkshopSession(args.project, 'banking-routing', state_dir=args.state,
                              notebook_identity=identity.get('notebook_identity'))
    if args.action == 'run':
        if args.forecast is None or args.approve_usd is None:
            parser.error('Running requires --forecast and --approve-usd')
        result = run_comparison(session, json.loads(args.plan.read_text()),
            forecast=json.loads(args.forecast.read_text()), approved_usd=args.approve_usd)
        print(json.dumps({'identity': result['identity'], 'summaries': result['summaries']}, indent=2))
    else:
        if not args.identity:
            parser.error('Publication requires --identity from the saved comparison')
        print(json.dumps(publish_comparison_result(session, args.identity), indent=2))


if __name__ == '__main__':
    main()
