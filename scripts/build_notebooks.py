"""Build editable notebooks from authored cells; hosted/local use the same source."""
import argparse
from pathlib import Path
from notebook_builder import Cell, render
from release_support import notebook_header, templates
ROOT=Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--only', choices=[row['slug'] for row in templates()])
selected = parser.parse_args().only


def save(name,title,cells):
    if selected and name != selected + '.py':
        return
    header = notebook_header(Path(name).stem, title)
    (ROOT/'notebooks'/name).write_text(
        header+render(cells)+'\nif __name__ == "__main__":\n    app.run()\n',
        encoding='utf-8', newline='\n',
    )

if selected in (None, 'solar_autoresearch'):
    from solar_cells import cells as solar_cells
    save("solar_autoresearch.py","Solar Autoresearch",solar_cells)

def add(code,hide=False):
    cells.append(Cell(code,hide=hide))


cells=[]
add('''
import os
from pathlib import Path
from datetime import datetime, timezone
import marimo as mo
from forge_workshop_kit.monitoring import monitor, load_roster, save_roster
from forge_workshop_kit.manifest import list_workshops
monitor_roster_path = Path(os.getenv("WORKSHOP_MONITOR_ROSTER", ".workshop/facilitator/roster.json"))
get_roster, set_roster = mo.state(load_roster(monitor_roster_path))
''',True)
add('''
monitor_intro = mo.md("# Workshop progress\\nAdd participants’ public project links and save the roster. This notebook reads their progress; it cannot run their code. A missing update means unknown. Ask the participant before assuming a run failed.")
_saved = get_roster()
_options = {row["title"]: row["id"] for row in list_workshops()}
_default = next((label for label, value in _options.items() if value == _saved.get("workshop")), next(iter(_options)))
roster_form = mo.Html("<section><h3>Participants</h3>{projects}{workshop}<details><summary>Filter updates or select one notebook copy</summary>{since}{until}{workspace}{session}</details></section>").batch(
    projects= mo.ui.text_area(value="\\n".join(_saved.get("projects", [])), label="Project links or entity/project, one per line", full_width=True),
    workshop=mo.ui.dropdown(_options, value=_default, label="Workshop"),
    since=mo.ui.text(value=_saved.get("since", ""), label="Updates since · UTC, for example 2026-11-13T13:00"),
    until=mo.ui.text(value=_saved.get("until", ""), label="Updates before · UTC, optional"),
    workspace=mo.ui.text(value=_saved.get("workspace", ""), label="Exact workspace ID · optional"),
    session=mo.ui.text(value=_saved.get("session", ""), label="Exact notebook copy ID · optional"),
).form(submit_button_label="Save roster and filters")
mo.vstack([monitor_intro, roster_form, mo.md("The roster saves in this monitor’s runtime. Date filters use the last published update. Leave IDs blank to include all copies; each workspace gets its own row.")])
''',True)
add('''
mo.stop(roster_form.value is None)
try:
    _values = {**roster_form.value, "projects": roster_form.value["projects"].splitlines()}
    _saved = save_roster(monitor_roster_path, _values)
    set_roster(_saved)
    mo.output.replace(mo.md("Roster saved. Click **Refresh progress** to read the projects."))
except Exception as _error:
    mo.output.replace(mo.callout(mo.md(str(_error)), kind="warn"))
''',True)
add('''
auto_refresh = mo.ui.checkbox(label="Refresh every 30 seconds while this notebook is open")
refresh = mo.ui.run_button(label="Refresh progress")
mo.hstack([refresh, auto_refresh])
''',True)
add('''
timer = mo.ui.refresh(default_interval=30) if auto_refresh.value else None
timer
''',True)
add('''
mo.stop(not get_roster().get("projects"), mo.md("Save at least one project above."))
mo.stop(not refresh.value and not auto_refresh.value)
if timer is not None:
    _tick = timer.value
_settings = get_roster()
try:
    with mo.status.spinner(title="Reading participant progress"):
        rows = monitor(_settings["projects"], _settings["workshop"], since=_settings.get("since"), until=_settings.get("until"), workspace=_settings.get("workspace", ""), session=_settings.get("session", ""))
    _display = [{"Project": row["project"], "Step": row.get("step", "Unknown"), "Status": row["status"], "Help request": row.get("help", ""), "Last update": row["last_update"], "Completed checkpoints": row.get("completed", 0), "Failures": row.get("failed", []), "Workspace": row.get("workspace", ""), "Notebook copy": row.get("session", ""), "Evidence": row.get("evidence", {}), "Progress run": row.get("url", ""), "Read error": row.get("error", "")} for row in rows]
    mo.output.replace(mo.vstack([mo.md("Last refresh: **" + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") + "**. This is when the monitor checked; each row shows when its participant last published."), mo.ui.table(_display, selection=None, hidden_columns=["Workspace", "Notebook copy", "Evidence", "Failures", "Read error"], format_mapping={"Progress run": lambda url: mo.md("[Open progress](" + url + ")") if url else ""}, label="Participant progress")]))
except Exception as _error:
    rows = []
    mo.output.replace(mo.callout(mo.md("Progress unavailable: " + str(_error) + ". Participant notebooks can continue."), kind="warn"))
''')
save('facilitator.py','Workshop progress',cells)

cells=[]
add('''
import os
import time
import marimo as mo
from forge_workshop_kit import WorkshopSession, setup, ui
from coreweave.forge.agentlens import tracing
''',True)
add('''
mo.md("# My workshop\\nCopy this notebook to your project, then replace the square calculation below with your own exercise. The tracing scopes show how to send its arguments and result to Agent Lens.")
_context=setup.project_context()
project=mo.ui.text(value=_context["project"],label="entity/project",disabled=_context["hosted"] and _context["detected"])
connect=mo.ui.run_button(label="Check project access")
mo.vstack([mo.Html(ui.result("Copied notebook project", {"Project": _context["project"]})) if _context["hosted"] and _context["detected"] else project,connect])
''',True)
add('''
mo.stop(not connect.value)
session=WorkshopSession.from_environment("starter",project=project.value)
_access=session.check_access()
session.restore()
setup.save_access(session,_access)
mo.ui.table(setup.capabilities(session), selection=None, pagination=False)
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

if selected in (None, 'pending_inc'):
    from pending_cells import cells as pending_cells
    save("pending_inc.py","Pending, Inc.",pending_cells)
if selected in (None, 'request_routing'):
    from routing_cells import cells as routing_cells
    save('request_routing.py', 'Route customer requests', routing_cells)
if selected in (None, 'visual_inspection'):
    from inspection_cells import cells as inspection_cells
    save('visual_inspection.py', 'Find defective parts before they ship', inspection_cells)

if selected in (None, "transit_factory"):
    from transit_cells import cells as transit_cells
    save("transit_factory.py", "Build a transit app with a team of coding agents", transit_cells)
