"""Optional isolated code execution. Only main() creates billed resources."""
import argparse
import json
from pathlib import Path

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.managed_jobs import validate_approval
from forge_workshop_kit.session import digest


def run_candidate(session, source, *, approved_usd, forecast, restore=None):
    validate_approval(forecast, approved_usd)
    from cwsandbox import AuthStrategy, FileSystemSnapshotOptions, Sandbox
    with session.stage('advanced/sandbox', sources={'candidate.py': source},
                       config={'cpu': '1', 'memory': '1Gi', 'timeout_seconds': 180, 'restore': restore}) as stage:
        if stage.needs_run:
            # Never copy the notebook environment or credentials into this process.
            with Sandbox.run(auth=AuthStrategy.WANDB, container_image='python:3.11-slim',
                resources={'cpu': '1', 'memory': '1Gi'}, max_lifetime_seconds=300,
                file_system_snapshot=FileSystemSnapshotOptions(mount_path='/work', size='1Gi',
                    **({'file_system_snapshot_id': restore} if restore else {}))) as sandbox:
                with session.transaction() as state:
                    state['stages'][stage.id]['sandbox_id'] = sandbox.sandbox_id
                sandbox.exec(['python', '-c', 'from pathlib import Path; import sys; Path("/work/candidate.py").write_text(sys.argv[1])', source]).result()
                result = sandbox.exec(['timeout', '180', 'python', '/work/candidate.py']).result()
                receipt = {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode,
                           'sandbox_id': sandbox.sandbox_id, 'snapshot_id': None,
                           'source_fingerprint': digest(source), 'forecast': forecast,
                           'approved_usd': approved_usd}
                # The command has finished even if snapshot storage later fails.
                with session.transaction() as state:
                    state['stages'][stage.id]['execution_receipt'] = receipt
                try:
                    receipt['snapshot_id'] = sandbox.snapshot().result()
                    receipt['snapshot_status'] = 'saved'
                except Exception as error:  # noqa: BLE001 -- snapshot failure must retain completed work
                    receipt['snapshot_status'] = 'unavailable'
                    receipt['snapshot_error'] = type(error).__name__
                stage.record(receipt)
    return stage.result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--forecast', type=Path, required=True)
    parser.add_argument('--approve-usd', type=float, required=True)
    parser.add_argument('--restore')
    args = parser.parse_args()
    session = WorkshopSession.from_environment('advanced-sandbox', project=args.project)
    print(json.dumps(run_candidate(session, args.source.read_text(), approved_usd=args.approve_usd,
                                  forecast=json.loads(args.forecast.read_text()), restore=args.restore), indent=2))
