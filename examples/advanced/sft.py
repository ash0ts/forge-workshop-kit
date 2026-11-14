"""Optional SFT: prepare reviewed data, submit once, or resume job monitoring."""
import argparse
import json
from pathlib import Path

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.advanced import TrainingClient, publish_sft_data, sft_examples, sft_request
from forge_workshop_kit.review import reviewed_dataset


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'prepare', 'launch', 'status', 'checkpoints'])
    parser.add_argument('--project', required=True)
    parser.add_argument('--state', required=True, help='The routing notebook workspace, not a new folder')
    parser.add_argument('--dataset-version')
    parser.add_argument('--cases', type=Path, help='Mapping from case IDs to public training/review records')
    parser.add_argument('--base-model', help='Verify current model support before registration')
    parser.add_argument('--forecast', type=Path, help='JSON with maximum_usd, checked_at, and pricing basis')
    parser.add_argument('--approve-usd', type=float)
    parser.add_argument('--job-key')
    parser.add_argument('--model-id')
    args = parser.parse_args()
    identity = json.loads((Path(args.state) / 'identity.json').read_text())
    session = WorkshopSession(args.project, 'banking-routing', state_dir=args.state,
                              notebook_identity=identity.get('notebook_identity'))
    client = TrainingClient()
    if args.action == 'check':
        print(json.dumps(client.check_access(), indent=2))
    elif args.action == 'status':
        if not args.job_key:
            parser.error('Monitoring requires --job-key from the saved submission')
        print(json.dumps(client.poll(session, args.job_key), indent=2))
    elif args.action == 'checkpoints':
        if not args.model_id:
            parser.error('Listing checkpoints requires --model-id')
        print(json.dumps(client.checkpoints(args.model_id), indent=2))
    else:
        if not args.dataset_version or not args.cases:
            parser.error('Preparation requires --dataset-version and --cases')
        cases = json.loads(args.cases.read_text())
        examples = sft_examples(reviewed_dataset(session, args.dataset_version), cases)
        data = publish_sft_data(session, examples)
        if args.action == 'prepare':
            print(json.dumps(data, indent=2))
            return
        if not args.forecast or args.approve_usd is None or not args.base_model:
            parser.error('Launch requires --forecast, --approve-usd, and --base-model')
        forecast = json.loads(args.forecast.read_text())
        if forecast['maximum_usd'] > args.approve_usd:
            parser.error('Forecast exceeds the approved amount')
        model = client.register_model(session, 'routing-specialist-' + session.workspace_id[:8], args.base_model)
        request = sft_request(model['id'], data['url'], len(examples))
        receipt = client.start_sft(session, request, forecast=forecast, approved_usd=args.approve_usd)
        session.checkpoint('advanced/sft')
        print(json.dumps(receipt, indent=2))
        print('Job keys:', ', '.join(session.read().get('managed_jobs', {})))


if __name__ == '__main__':
    main()
