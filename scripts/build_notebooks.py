"""Build editable notebooks from authored cells; hosted/local use the same source."""
import json
import argparse
from pathlib import Path
from notebook_builder import Cell, render
ROOT=Path(__file__).resolve().parents[1]
DEFAULT=(ROOT/'examples/solar/candidate.py').read_text()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--only', choices=['solar_autoresearch', 'pending_inc', 'starter', 'facilitator'])
selected = parser.parse_args().only


def save(name,title,cells):
    if selected and name != selected + '.py':
        return
    header=f'''# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.2.1/forge_workshop_kit-0.2.1-py3-none-any.whl", "torch==2.15.0"]
# [tool.uv.sources]
# torch = [{{ index = "pytorch-cpu", marker = "sys_platform != 'darwin'" }}]
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title={title!r})
'''
    (ROOT/'notebooks'/name).write_text(header+render(cells)+'\nif __name__ == "__main__":\n    app.run()\n')

from solar_cells import cells as solar_cells
save("solar_autoresearch.py","Solar Autoresearch",solar_cells)

def add(code,hide=False):
    cells.append(Cell(code,hide=hide))


cells=[]
add('''
import marimo as mo
from forge_workshop_kit.publication import monitor
''',True)
add('''
mo.md("# Workshop progress\\nThis notebook only reads participant projects. Missing updates mean unknown, not failure. It never starts participant work.")
roster=mo.ui.text_area(label="Public project links: entity/project, one per line",full_width=True)
workshop=mo.ui.dropdown({"Solar Autoresearch · four hours":"solar-autoresearch","Pending, Inc. · three hours":"pending-direct-teaching"},value="Solar Autoresearch · four hours",label="Workshop")
auto_refresh=mo.ui.checkbox(label="Refresh every 30 seconds while this notebook is open")
refresh=mo.ui.run_button(label="Refresh progress")
mo.vstack([roster,workshop,auto_refresh,refresh])
''',True)
add('''
timer=mo.ui.refresh(default_interval=30) if auto_refresh.value else None
timer
''',True)
add('''
mo.stop(not roster.value.strip())
mo.stop(not refresh.value and not auto_refresh.value)
if timer is not None:
    _tick=timer.value
rows=monitor(roster.value.splitlines(),workshop.value)
mo.ui.table(rows,selection=None)
''')
save('facilitator.py','Workshop progress',cells)

cells=[]
add('''
import os
import time
import marimo as mo
from forge_workshop_kit import WorkshopSession
from coreweave.forge.agentlens import tracing
''',True)
add('''
mo.md("# My workshop\\nCopy this notebook to your project. Add your exercise code below; keep the SDK calls visible.")
project=mo.ui.text(value=os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None,[os.getenv("WANDB_ENTITY"),os.getenv("WANDB_PROJECT")])),label="entity/project")
connect=mo.ui.run_button(label="Check project access")
mo.vstack([project,connect])
''',True)
add('''
mo.stop(not connect.value)
session=WorkshopSession.from_environment("starter",project=project.value)
session.check_access()
session.restore()
''')
add('''
run_exercise=mo.ui.run_button(label="Run my instrumented exercise")
run_exercise
''',True)
add('''
mo.stop(not run_exercise.value)
sdk=tracing.init(session.project,autopatch_integrations=False)
with session.stage("exercise",config={"input":3}) as stage:
    if stage.needs_run:
        with tracing.Conversation(conversation_id=stage.id,conversation_name="My first exercise"):
            with tracing.Turn(agent_name="participant",messages=[tracing.Message(role="user",content="Check the function I wrote")]):
                with tracing.Tool(name="square",arguments={"x":3}) as span:
                    result=3*3  # Replace this with your exercise.
                    span.result={"answer":result}
                    stage.record({"answer":result})
        sdk.force_flush()
session.checkpoint("exercise")
mo.md(str(stage.result))
''')
save('starter.py','My Forge workshop',cells)

from pending_cells import cells as pending_cells
save("pending_inc.py","Pending, Inc.",pending_cells)
