# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#   "forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.4.1/forge_workshop_kit-0.4.1-py3-none-any.whl",
#   "abnf==2.2.0",
#   "annotated-types==0.8.0",
#   "anyio==4.16.0",
#   "attrs==26.1.0",
#   "cachetools==8.0.0",
#   "certifi==2026.10.23",
#   "cffi==2.1.1 ; (implementation_name == 'pypy' and sys_platform != 'emscripten') or platform_python_implementation != 'PyPy'",
#   "chardet==7.7.0",
#   "charset-normalizer==3.5.2",
#   "cint==1.0.0",
#   "click==8.5.1",
#   "coreweave==0.1.0b0",
#   "cryptography==50.0.2",
#   "cwevals==0.0.1b1",
#   "diskcache-weave==5.6.3.post1",
#   "distro==1.9.0",
#   "docutils==0.23",
#   "fickling==0.1.13",
#   "filelock==3.32.7",
#   "googleapis-common-protos==1.76.0",
#   "gql==4.4.0",
#   "graphql-core==3.3.2",
#   "graphviz==0.21",
#   "h11==0.16.0",
#   "httpcore==1.0.9",
#   "httpx==0.28.1",
#   "idna==3.20",
#   "intervaltree==3.2.1",
#   "itsdangerous==2.2.0",
#   "jedi==0.20.1",
#   "jinja2==3.1.6",
#   "jsonschema==4.26.0",
#   "jsonschema-specifications==2025.9.1",
#   "kaitaistruct==0.11",
#   "loro==1.17.1 ; sys_platform != 'android' and sys_platform != 'emscripten'",
#   "marimo==0.25.2",
#   "markdown==3.11.3",
#   "markupsafe==3.0.4",
#   "msgspec==0.22.0",
#   "multidict==7.2.1",
#   "narwhals==2.28.0",
#   "networkx==3.6.1 ; python_full_version < '3.12'",
#   "networkx==3.7 ; python_full_version >= '3.12'",
#   "opentelemetry-api==1.45.2",
#   "opentelemetry-exporter-http-transport==0.66b2",
#   "opentelemetry-exporter-otlp-common==0.66b2",
#   "opentelemetry-exporter-otlp-proto-common==1.45.2",
#   "opentelemetry-exporter-otlp-proto-http==1.45.2",
#   "opentelemetry-proto==1.45.2",
#   "opentelemetry-sdk==1.45.2",
#   "opentelemetry-semantic-conventions==0.66b2",
#   "packaging==26.3",
#   "parso==0.8.7",
#   "pdfminer-six==20260107",
#   "pillow==13.0.0",
#   "platformdirs==4.14.5",
#   "polyfile-weave==0.5.9",
#   "propcache==0.5.4",
#   "protobuf==7.36.2",
#   "psutil==7.2.2 ; sys_platform != 'android' and sys_platform != 'emscripten'",
#   "pycparser==3.12 ; (implementation_name != 'PyPy' and platform_python_implementation != 'PyPy') or (implementation_name == 'pypy' and platform_python_implementation == 'PyPy' and sys_platform != 'emscripten')",
#   "pydantic==2.14.3",
#   "pydantic-core==2.50.4",
#   "pygments==2.21.0",
#   "pymdown-extensions==11.0.2",
#   "pyreadline3==3.5.6 ; sys_platform == 'win32'",
#   "python-multipart==0.0.33",
#   "pyyaml==6.0.3",
#   "pyzmq==27.3.0 ; sys_platform != 'emscripten'",
#   "referencing==0.37.0",
#   "requests==2.34.2",
#   "rpds-py==2026.9.1",
#   "sentry-sdk==2.75.0",
#   "sniffio==1.3.1",
#   "sortedcontainers==2.4.0",
#   "starlette==1.10.0 ; sys_platform != 'emscripten'",
#   "tenacity==9.2.1",
#   "tomlkit==0.15.2",
#   "typing-extensions==4.16.0",
#   "typing-inspection==0.4.5",
#   "tzdata==2026.6 ; sys_platform == 'win32'",
#   "urllib3==2.8.0",
#   "uvicorn==0.54.0 ; sys_platform != 'emscripten'",
#   "wandb==0.31.0",
#   "wandb-workspaces==0.4.13",
#   "weave==0.54.0",
#   "websockets==17.4 ; sys_platform != 'emscripten'",
#   "xxhash==4.1.0",
#   "yarl==1.25.1",
# ]
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title='Workshop progress')


@app.cell(hide_code=True)
def _():
    import os
    from pathlib import Path
    from datetime import datetime, timezone
    import marimo as mo
    from forge_workshop_kit.monitoring import monitor, load_roster, save_roster
    from forge_workshop_kit.manifest import list_workshops
    monitor_roster_path = Path(os.getenv("WORKSHOP_MONITOR_ROSTER", ".workshop/facilitator/roster.json"))
    get_roster, set_roster = mo.state(load_roster(monitor_roster_path))
    return (Path, datetime, get_roster, list_workshops, load_roster, mo, monitor, monitor_roster_path, os, save_roster, set_roster, timezone,)


@app.cell(hide_code=True)
def _(get_roster, list_workshops, mo):
    monitor_intro = mo.md("# Workshop progress\nAdd participants’ public project links and save the roster. This notebook reads their progress; it cannot run their code. A missing update means unknown. Ask the participant before assuming a run failed.")
    _saved = get_roster()
    _options = {row["title"]: row["id"] for row in list_workshops()}
    _default = next((label for label, value in _options.items() if value == _saved.get("workshop")), next(iter(_options)))
    roster_form = mo.Html("<section><h3>Participants</h3>{projects}{workshop}<details><summary>Filter updates or select one notebook copy</summary>{since}{until}{workspace}{session}</details></section>").batch(
        projects= mo.ui.text_area(value="\n".join(_saved.get("projects", [])), label="Project links or entity/project, one per line", full_width=True),
        workshop=mo.ui.dropdown(_options, value=_default, label="Workshop"),
        since=mo.ui.text(value=_saved.get("since", ""), label="Updates since · UTC, for example 2026-11-13T13:00"),
        until=mo.ui.text(value=_saved.get("until", ""), label="Updates before · UTC, optional"),
        workspace=mo.ui.text(value=_saved.get("workspace", ""), label="Exact workspace ID · optional"),
        session=mo.ui.text(value=_saved.get("session", ""), label="Exact notebook copy ID · optional"),
    ).form(submit_button_label="Save roster and filters")
    mo.vstack([monitor_intro, roster_form, mo.md("The roster saves in this monitor’s runtime. Date filters use the last published update. Leave IDs blank to include all copies; each workspace gets its own row.")])
    return (monitor_intro, roster_form,)


@app.cell(hide_code=True)
def _(mo, monitor_roster_path, roster_form, save_roster, set_roster):
    mo.stop(roster_form.value is None)
    try:
        _values = {**roster_form.value, "projects": roster_form.value["projects"].splitlines()}
        _saved = save_roster(monitor_roster_path, _values)
        set_roster(_saved)
        mo.output.replace(mo.md("Roster saved. Click **Refresh progress** to read the projects."))
    except Exception as _error:
        mo.output.replace(mo.callout(mo.md(str(_error)), kind="warn"))
    return


@app.cell(hide_code=True)
def _(mo):
    auto_refresh = mo.ui.checkbox(label="Refresh every 30 seconds while this notebook is open")
    refresh = mo.ui.run_button(label="Refresh progress")
    mo.hstack([refresh, auto_refresh])
    return (auto_refresh, refresh,)


@app.cell(hide_code=True)
def _(auto_refresh, mo):
    timer = mo.ui.refresh(default_interval=30) if auto_refresh.value else None
    timer
    return (timer,)


@app.cell
def _(auto_refresh, datetime, get_roster, mo, monitor, refresh, timer, timezone):
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
    return (rows,)

if __name__ == "__main__":
    app.run()
