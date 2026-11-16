# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#   "forge-workshop-kit[solar] @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.12.0/forge_workshop_kit-0.12.0-py3-none-any.whl",
#   "abnf==2.2.0",
#   "aioftp==0.28.3",
#   "aiohappyeyeballs==2.7.1",
#   "aiohttp==3.14.5",
#   "aiosignal==1.4.0",
#   "annotated-types==0.8.0",
#   "anyio==4.16.0",
#   "astropy==8.0.2",
#   "astropy-healpix==2.0.1",
#   "astropy-iers-data==0.2026.11.9.0.35.9",
#   "attrs==26.1.0",
#   "cachetools==8.0.0",
#   "certifi==2026.10.23",
#   "cffi==2.1.1 ; (implementation_name == 'pypy' and sys_platform != 'emscripten') or platform_python_implementation != 'PyPy'",
#   "chardet==7.7.0",
#   "charset-normalizer==3.5.2",
#   "cint==1.0.0",
#   "click==8.5.1",
#   "cloudpickle==3.1.2",
#   "colorama==0.4.6 ; sys_platform == 'win32'",
#   "contourpy==1.3.3 ; python_full_version < '3.12'",
#   "contourpy==1.4.0 ; python_full_version >= '3.12'",
#   "coreweave==0.1.0b0",
#   "cryptography==50.0.2",
#   "cwevals==0.0.1b1",
#   "cycler==0.12.1",
#   "dask==2026.8.0",
#   "dask-image==2026.5.0",
#   "diskcache-weave==5.6.3.post1",
#   "distro==1.9.0",
#   "docutils==0.23",
#   "donfig==0.8.1.post1",
#   "fickling==0.1.13",
#   "filelock==3.32.7",
#   "fonttools==4.68.0",
#   "frozenlist==1.8.0",
#   "fsspec==2026.9.0",
#   "google-crc32c==1.9.0",
#   "googleapis-common-protos==1.76.0",
#   "gql==4.4.0",
#   "graphql-core==3.3.2",
#   "graphviz==0.21",
#   "h11==0.16.0",
#   "httpcore==1.0.9",
#   "httpx==0.28.1",
#   "idna==3.20",
#   "imageio==2.38.1",
#   "importlib-metadata==10.2.0 ; python_full_version < '3.12'",
#   "intervaltree==3.2.1",
#   "itsdangerous==2.2.0",
#   "jedi==0.20.1",
#   "jinja2==3.1.6",
#   "jsonschema==4.26.0",
#   "jsonschema-specifications==2025.9.1",
#   "kaitaistruct==0.11",
#   "kiwisolver==1.5.1",
#   "lazy-importer==0.1.0 ; python_full_version < '3.12'",
#   "locket==1.0.0",
#   "loro==1.17.1 ; sys_platform != 'android' and sys_platform != 'emscripten'",
#   "marimo==0.25.2",
#   "markdown==3.11.3",
#   "markupsafe==3.0.4",
#   "matplotlib==3.11.2",
#   "mpl-animators==1.2.4",
#   "mpmath==1.3.0",
#   "msgspec==0.22.0",
#   "multidict==7.2.1",
#   "narwhals==2.28.0",
#   "networkx==3.6.1 ; python_full_version < '3.12'",
#   "networkx==3.7 ; python_full_version >= '3.12'",
#   "numcodecs==0.16.6 ; python_full_version < '3.12'",
#   "numcodecs==0.17.1 ; python_full_version >= '3.12'",
#   "numpy==2.4.6 ; python_full_version < '3.12'",
#   "numpy==2.5.4 ; python_full_version >= '3.12'",
#   "opentelemetry-api==1.45.2",
#   "opentelemetry-exporter-http-transport==0.66b2",
#   "opentelemetry-exporter-otlp-common==0.66b2",
#   "opentelemetry-exporter-otlp-proto-common==1.45.2",
#   "opentelemetry-exporter-otlp-proto-http==1.45.2",
#   "opentelemetry-proto==1.45.2",
#   "opentelemetry-sdk==1.45.2",
#   "opentelemetry-semantic-conventions==0.66b2",
#   "packaging==26.3",
#   "pandas==2.3.3",
#   "parfive==2.3.1",
#   "parso==0.8.7",
#   "partd==1.4.2",
#   "pdfminer-six==20260107",
#   "pillow==12.3.0",
#   "pims==0.7",
#   "platformdirs==4.14.5",
#   "polyfile-weave==0.5.9",
#   "propcache==0.5.4",
#   "protobuf==6.33.6",
#   "psutil==7.2.2 ; sys_platform != 'android' and sys_platform != 'emscripten'",
#   "pyavm==0.9.9",
#   "pycparser==3.12 ; (implementation_name != 'PyPy' and platform_python_implementation != 'PyPy') or (implementation_name == 'pypy' and platform_python_implementation == 'PyPy' and sys_platform != 'emscripten')",
#   "pydantic==2.14.3",
#   "pydantic-core==2.50.4",
#   "pyerfa==2.0.1.5",
#   "pygments==2.21.0",
#   "pymdown-extensions==11.0.2",
#   "pyparsing==3.3.3",
#   "pyreadline3==3.5.6 ; sys_platform == 'win32'",
#   "python-dateutil==4.0.0",
#   "python-multipart==0.0.33",
#   "pytz==2026.6",
#   "pyyaml==6.0.3",
#   "pyzmq==27.3.0 ; sys_platform != 'emscripten'",
#   "referencing==0.37.0",
#   "reproject==0.21.0",
#   "requests==2.34.2",
#   "rpds-py==2026.9.1",
#   "scipy==1.17.1 ; python_full_version < '3.12'",
#   "scipy==1.18.1 ; python_full_version >= '3.12'",
#   "sentry-sdk==2.75.0",
#   "setuptools==84.2.1",
#   "slicerator==1.1.0",
#   "sniffio==1.3.1",
#   "sortedcontainers==2.4.0",
#   "starlette==1.10.0 ; sys_platform != 'emscripten'",
#   "sunpy==7.0.5 ; python_full_version < '3.12'",
#   "sunpy==8.0.1 ; python_full_version >= '3.12'",
#   "sympy==1.14.0",
#   "tenacity==9.2.1",
#   "tifffile==2026.3.3 ; python_full_version < '3.12'",
#   "tifffile==2026.11.12 ; python_full_version >= '3.12'",
#   "tomlkit==0.15.2",
#   "toolz==1.2.0",
#   "torch==2.15.0 ; sys_platform == 'darwin'",
#   "torch==2.15.0+cpu ; sys_platform != 'darwin'",
#   "tqdm==4.70.1",
#   "typing-extensions==4.16.0",
#   "typing-inspection==0.4.5",
#   "tzdata==2026.6",
#   "urllib3==2.8.0",
#   "uvicorn==0.54.0 ; sys_platform != 'emscripten'",
#   "wandb==0.31.0",
#   "wandb-workspaces==0.4.13",
#   "weave==0.54.0",
#   "websockets==17.4 ; sys_platform != 'emscripten'",
#   "xxhash==4.1.0",
#   "yarl==1.25.1",
#   "zarr==3.1.6 ; python_full_version < '3.12'",
#   "zarr==3.4.2 ; python_full_version >= '3.12'",
#   "zipp==4.1.2 ; python_full_version < '3.12'",
# ]
# [tool.uv.sources]
# torch = [{ index = "pytorch-cpu", marker = "sys_platform != 'darwin'" }]
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title='Solar forecasting with agent-assisted experiments')


# workshop-cell: solar_autoresearch/definitions/technical_guide_controls
@app.cell(hide_code=True)
def _():
    import os
    import json
    import time
    from pathlib import Path
    import numpy as np
    import marimo as mo
    from forge_workshop_kit import WorkshopSession, setup
    from forge_workshop_kit import aria, technical_guides
    from forge_workshop_kit import solar, training, research, ui, plots, solar_teaching as teaching
    from forge_workshop_kit import solar_views as views
    from forge_workshop_kit.session import digest
    from forge_workshop_kit.download import dataset
    from forge_workshop_kit.publication import publish_comparison, publish_report
    from forge_workshop_kit.traces import export_trace, event, stamp, saved_trace_inputs
    get_lab, set_lab = mo.state({})
    get_feedback, set_feedback = mo.state({})
    get_tracing_check, set_tracing_check = mo.state({})
    get_technical_guide_view, set_technical_guide_view = mo.state({}, allow_self_loops=True)
    technical_guide_controls = technical_guides.controls(mo, 'solar_autoresearch', set_technical_guide_view)
    get_step, set_step = mo.state("setup", allow_self_loops=True)
    get_recovery_revision, set_recovery_revision = mo.state(0)
    return (Path, WorkshopSession, aria, dataset, digest, event, export_trace, get_feedback, get_lab, get_recovery_revision, get_step, get_technical_guide_view, get_tracing_check, json, mo, np, os, plots, publish_comparison, publish_report, research, saved_trace_inputs, set_feedback, set_lab, set_recovery_revision, set_step, set_technical_guide_view, set_tracing_check, setup, solar, stamp, teaching, technical_guide_controls, technical_guides, time, training, ui, views,)


# workshop-cell: solar_autoresearch/display/2
@app.cell(hide_code=True)
def _(get_step, mo, ui):
    mo.stop(get_step() != "setup")
    mo.vstack([mo.md("**6-hour workshop, including breaks and exercises.** [Open the companion deck](https://ash0ts.github.io/forge-workshop-kit/solar/). Its worked examples explain the code you will edit below."),mo.Html(ui.heading("Solar forecasting with agent-assisted experiments", "You're preparing a forecast for a fictional research lab's weekly review. The team needs to decide which model to develop further. Your job is to compare its predictions with later satellite observations and bring an experiment a colleague can repeat.", theme="lab")),
    mo.md("Last week's shared folder had four notebooks called final. One reported a lower error, but nobody could tell which preprocessing or weights produced it. You'll save those details with each run."),
    mo.md("### The observations you'll use"),
    mo.md("The lab is fictional; the data are real satellite observations from **February 1–14, 2014**. SunPy is the Python library we'll use to inspect the observations and their metadata. We'll tackle two related prediction tasks separately:"),
    mo.md("**First, measurements over time.** GOES-15 recorded the Sun's X-ray flux: the X-ray power received per square metre. Each example gives the model 60 one-minute readings from two sensor channels. It must predict the XRS-B channel **30 minutes ahead**. We'll compare that number with the later measurement, using average error in log-flux units."),
    mo.md("**Then, images over time.** SDO's AIA instrument recorded extreme-ultraviolet images of the Sun. We use its 171 Å channel, reduced to **64 × 64 pixels**. Each example contains an image from an hour ago and one from now; the target is the image **one hour later**. We'll compare predicted and observed brightness inside the solar disk. The displayed colors represent intensity."),
    mo.md("### What you need to bring to the review"),
    mo.md("Start by copying the latest observation as the forecast. This is **persistence**. Compare each trained model with this baseline to find out whether it reduces error. Train on February 1–10, choose changes using 11–12, then freeze your choice before testing on 13–14. We'll skip windows with missing observations; normalization comes from training dates only."),
    mo.md("Train one model and inspect its forecast before comparing the other settings. Open the training run to find its loss history, then its saved files to recover the source and weights. Later, a research agent will propose edits to the image-model code. You'll read each diff, train it, and compare its validation error with the previous version. Bring those forecasts to the review, including any that got worse. Two final-test days are enough for this teaching exercise, but not to establish a reliable solar forecast."),
    mo.accordion({"Where these observations come from":mo.md("[GOES X-ray measurements and SunPy](https://docs.sunpy.org/en/stable/generated/gallery/time_series/goes_xrs_example.html) · [NASA's explanation of the AIA channels](https://sdo.gsfc.nasa.gov/data/channels.php) · [Workshop acquisition and preparation code](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_solar.py). The prepared download contains measurements, image arrays, a representative FITS image, source checksums, and quality exclusions. You do not need to download the raw archive yourself.")})])
    return


# workshop-cell: solar_autoresearch/definitions/preview_target
@app.cell(hide_code=True)
def _(get_step, mo, teaching):
    mo.stop(get_step() != "setup")
    _solar_preview = teaching.development_preview()
    preview_target = mo.ui.checkbox(label="Show the later observation and this forecast's error")
    mo.vstack([mo.md("### Try one forecast before signing in"), mo.md("This bundled example is a real training-date reading, not a model run. At **" + _solar_preview["origin"] + " UTC**, XRS-B log-flux is **" + str(round(_solar_preview["latest_log10"], 6)) + "**. Persistence predicts the same value 30 minutes later. Before revealing the target, say what that assumption means."), mo.md("```python\nforecast = latest_log10\nabsolute_error = abs(forecast - target_log10)\n```"), preview_target])
    return (preview_target,)


# workshop-cell: solar_autoresearch/display/4
@app.cell(hide_code=True)
def _(get_step, mo, preview_target, teaching, ui):
    mo.stop(get_step() != "setup")
    _example = teaching.development_preview()
    mo.Html(ui.result("One observed forecast window", {"Forecast origin (UTC)": _example["origin"], "Target time (UTC)": _example["target_time"], "Persistence forecast": _example["latest_log10"], "Observed target": _example["target_log10"], "Absolute log-flux error": abs(_example["latest_log10"] - _example["target_log10"]), "Source": "Bundled GOES-15 training example; not a new experiment"})) if preview_target.value else mo.md("You can inspect this example without authentication. Connect below when you are ready to save your own work.")
    return


# workshop-cell: solar_autoresearch/definitions/go_to
@app.cell(hide_code=True)
def _(get_lab, set_step):
    def go_to(step):
        session = get_lab().get("session")
        if session:
            session.set_view(step)
        set_step(step)
    return (go_to,)


# workshop-cell: solar_autoresearch/definitions/refresh_saved
@app.cell(hide_code=True)
def _(get_lab, set_lab, teaching):
    def refresh_saved():
        context = get_lab()
        set_lab({**context, **teaching.restore_state(context["session"])})
    return (refresh_saved,)


# workshop-cell: solar_autoresearch/definitions/checked
@app.cell(hide_code=True)
def _(set_feedback):
    def checked(name, action):
        try:
            result = action()
            set_feedback(lambda current: {**current, name: {"status": "complete", **result}})
        except Exception as error:
            set_feedback(lambda current: {**current, name: {"status": "needs work", "message": str(error)}})
    return (checked,)


# workshop-cell: solar_autoresearch/definitions/solar_navigation
@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, teaching, technical_guides, ui):
    _s = get_lab().get("session")
    solar_navigation = ui.navigation(mo, teaching.STEPS, get_step(), go_to, completed=teaching.completed_steps(_s) if _s else (), label="Workshop steps")
    mo.vstack([mo.Html(ui.STYLE + technical_guides.theme_style()), solar_navigation, mo.Html(ui.context(_s)) if _s else mo.md("**Start at Connect.** Your code and results stay in your project. Training and model calls run only when you click their Run buttons.")])
    return (solar_navigation,)


# workshop-cell: solar_autoresearch/visual_guide
@app.cell(hide_code=True)
def _(get_step, get_technical_guide_view, mo, technical_guide_controls, technical_guides):
    technical_guide_view = technical_guides.panel(mo, 'solar_autoresearch', get_step(), get_technical_guide_view(), technical_guide_controls)
    technical_guide_view
    return (technical_guide_view,)


# workshop-cell: solar_autoresearch/definitions/solar_recovery_refresh
@app.cell(hide_code=True)
def _(get_lab, get_recovery_revision, get_step, mo, set_recovery_revision, setup):
    _s = get_lab().get("session")
    _revision = get_recovery_revision()
    _view = get_step()
    solar_recovery_refresh = mo.ui.button(label="Check for stopped or failed work", on_click=lambda _: set_recovery_revision(lambda previous: previous + 1), disabled=not bool(_s))
    _options = _s.recovery_options() if _s else []
    _choices = {setup.recovery_label(_s.workshop, row) + " · " + row["id"][:6]: row["id"] for row in _options}
    solar_recovery_choice = mo.ui.dropdown(_choices, value=next(iter(_choices), None), label="Execution to review", full_width=True) if _choices else mo.ui.dropdown({"No failed executions": ""}, value="No failed executions", disabled=True)
    mo.vstack([mo.md("**A run stopped?** Check its saved status here. Reviewing it never starts work."), solar_recovery_refresh, solar_recovery_choice]) if _options else mo.accordion({"A run stopped? Review recovery": mo.vstack([mo.md("Click below to read saved execution status. Completed results stay saved. An upload failure uses Retry publication in the final comparison instead."), solar_recovery_refresh])})
    return (solar_recovery_choice, solar_recovery_refresh,)


# workshop-cell: solar_autoresearch/controls/solar_recovery_allow
@app.cell(hide_code=True)
def _(get_lab, mo, solar_recovery_choice, ui):
    _s = get_lab().get("session")
    _row = next((row for row in _s.recovery_options() if row["id"] == solar_recovery_choice.value), None) if _s else None
    _needs_confirmation = bool(_row and (_row["has_uncertain_requests"] or _row["status"] == "running"))
    solar_recovery_confirm = mo.ui.checkbox(label="I checked that the previous execution has stopped. Keep unresolved requests charged at their reserved maximum.")
    solar_recovery_allow = mo.ui.run_button(label="Allow retry of this failed execution", disabled=not bool(_row), full_width=True)
    mo.vstack([mo.Html(ui.result("Review the saved execution", {"Execution": _row["name"], "Status": _row["status"], "Issue": _row.get("error") or "The execution has not finished.", "Next": "Allow another attempt, then click the normal run button for this step. This control does not run the experiment."}, status="failed")), solar_recovery_confirm if _needs_confirmation else mo.md("The previous attempt has ended. Its result and costs remain in the record."), solar_recovery_allow]) if _row else mo.md("")
    return (solar_recovery_allow, solar_recovery_confirm,)


# workshop-cell: solar_autoresearch/action/solar_recovery_allow
@app.cell(hide_code=True)
def _(get_lab, mo, refresh_saved, set_feedback, set_recovery_revision, solar_recovery_allow, solar_recovery_choice, solar_recovery_confirm):
    mo.stop(not solar_recovery_allow.value)
    _s = get_lab()["session"]
    try:
        _route = _s.retry_stage(solar_recovery_choice.value, confirm_stopped=solar_recovery_confirm.value)
        _message = "Retry allowed. Return to this step’s run button to start attempt " + str(_route["attempt"]) + ". Completed work will be reused."
    except Exception as _error:
        _message = str(_error)
    set_feedback(lambda current: {**current, "recovery": _message})
    refresh_saved()
    set_recovery_revision(lambda previous: previous + 1)
    return


# workshop-cell: solar_autoresearch/display/13
@app.cell(hide_code=True)
def _(get_feedback, mo):
    _message = get_feedback().get("recovery")
    mo.callout(mo.md(_message), kind="info") if _message else mo.md("")
    return


# workshop-cell: solar_autoresearch/controls/help_button
@app.cell(hide_code=True)
def _(get_lab, mo):
    help_message = mo.ui.text_area(label="What do you need help with?", full_width=True)
    help_button = mo.ui.run_button(label="Send a help request", disabled=not bool(get_lab().get("session")))
    mo.accordion({"Ask the facilitator": mo.vstack([help_message, help_button, mo.md("Tell the facilitator which step you’re on and what happened. They can read this request in the workshop monitor.")])})
    return (help_button, help_message,)


# workshop-cell: solar_autoresearch/action/help_button
@app.cell(hide_code=True)
def _(get_lab, help_button, help_message, mo):
    mo.stop(not help_button.value)
    get_lab()["session"].request_help(help_message.value)
    mo.md("Help request saved. Send an empty message when it is resolved.")
    return


# workshop-cell: solar_autoresearch/controls/connect_button
@app.cell(hide_code=True)
def _(get_step, mo, setup, ui):
    mo.stop(get_step() != "setup")
    _context = setup.project_context()
    project_input = mo.ui.text(value=_context["project"], placeholder="your-name/solar-research", label="Your Forge project", disabled=_context["hosted"] and _context["detected"], full_width=True)
    allowance = mo.ui.number(value=8, start=.01, stop=1000, label="Inference allowance in USD; notebook compute is separate")
    connect_button = mo.ui.run_button(label="Connect and restore my work")
    mo.vstack([mo.Html(ui.step("1. Connect to your own project", "Enter your writable Forge entity/project below, then click Connect and restore my work. Use the login command from the start page first. If you imported this file into Forge, check the detected project.", "Once the connection succeeds, add your first trace in the code below.")), mo.Html(ui.result("Copied notebook project", {"Project": _context["project"], "Access": "Uses your Forge login"})) if _context["hosted"] and _context["detected"] else project_input, allowance, connect_button])
    return (allowance, connect_button, project_input,)


# workshop-cell: solar_autoresearch/action/connect_button
@app.cell(hide_code=True)
def _(WorkshopSession, allowance, connect_button, mo, project_input, set_feedback, set_lab, set_step, setup, teaching):
    mo.stop(not connect_button.value)
    _s = None
    _access = None
    try:
        _s = WorkshopSession.from_environment("solar-autoresearch", project=project_input.value, budget_usd=allowance.value)
        _access = _s.check_access()
        _restored = _s.restore()
        setup.save_access(_s, _access)
        set_lab(teaching.restore_state(_s))
        set_step(_s.get_view("setup"))
        set_feedback(lambda current: {**current, "setup": {"status": "complete", **_access, "restore": _restored}})
    except Exception as _error:
        if _s is not None and _access is None:
            setup.save_access(_s, {"write_access": False, "error": str(_error)})
        set_feedback(lambda current: {**current, "setup": {"status": "unavailable", "message": str(_error), "next": "Check that you’re signed in and can write to this project, then try Connect again."}})
    return


# workshop-cell: solar_autoresearch/controls/check_instrumentation
@app.cell(hide_code=True)
def _(get_lab, get_step, mo, teaching):
    _s = get_lab().get("session")
    instrumentation_editor = mo.ui.code_editor(value=_s.get_draft("solar/instrumentation", teaching.INSTRUMENTATION_STARTER) if _s else teaching.INSTRUMENTATION_STARTER, language="python", on_change=lambda value: _s.save_draft("solar/instrumentation", value) if _s else None, debounce=False)
    check_instrumentation = mo.ui.run_button(label="Check my tracing code")
    mo.vstack([mo.md("**Give your first trace a label.** In `instrument_tool`, add `workshop.exercise` with the value `solar-research` inside the Tool scope. Click **Check my tracing code**, then **Send my first Agent Lens trace**. We’ll reuse this function when you train a model."), instrumentation_editor, check_instrumentation, mo.accordion({"Hint": mo.md("Add `tool.set_attributes({'workshop.exercise': 'solar-research'})` inside the `with tracing.Tool(...)` block. Leave the other fields in place so the trace still shows what ran."), "Worked answer": mo.md("```python\n" + teaching.INSTRUMENTATION_SOLUTION + "\n```")})]) if get_step() == "setup" else mo.md("")
    return (check_instrumentation, instrumentation_editor,)


# workshop-cell: solar_autoresearch/definitions/instrument_tool
@app.cell
def _(instrumentation_editor, teaching):
    # The edited function below is the writer used by every export in this notebook.
    def instrument_tool(observation):
        return teaching.functions(instrumentation_editor.value)["instrument_tool"](observation)
    return (instrument_tool,)


# workshop-cell: solar_autoresearch/action/check_instrumentation
@app.cell(hide_code=True)
def _(check_instrumentation, digest, instrumentation_editor, mo, set_tracing_check, teaching):
    mo.stop(not check_instrumentation.value)
    try:
        _result = teaching.check_instrumentation(instrumentation_editor.value)
        set_tracing_check({"status": "complete", **_result, "source": digest(instrumentation_editor.value)})
    except Exception as _error:
        set_tracing_check({"status": "needs work", "message": str(_error)})
    return


# workshop-cell: solar_autoresearch/controls/first_trace
@app.cell(hide_code=True)
def _(digest, get_feedback, get_lab, get_step, get_tracing_check, go_to, instrumentation_editor, mo, setup, teaching, ui):
    mo.stop(get_step() != "setup")
    _s = get_lab().get("session")
    _checked = get_tracing_check()
    first_trace = mo.ui.run_button(label="Send my first Agent Lens trace", disabled=not bool(_s) or _checked.get("source") != digest(instrumentation_editor.value))
    _setup = get_feedback().get("setup", {"Project": _s.project} if _s else {})
    solar_next_step_2 = ui.next_step(mo, "Next: inspect the solar data", "data", go_to)
    mo.vstack([mo.Html(ui.result("Connection", _setup, status=_setup.get("status", "not checked"))) if _setup else mo.md("Enter your project above, then click **Connect and restore my work**."), mo.ui.table(setup.capabilities(_s), selection=None, pagination=False) if _s else mo.md(""), mo.Html(ui.result("Local tracing check", _checked, status=_checked.get("status", "not checked"))) if _checked else mo.md("Add the attribute in the code above, then click **Check my tracing code**."), mo.md("The Send button runs a small environment check and saves its trace. Open the link below when it finishes."), first_trace, ui.evidence(mo, _s, stage_ids=[teaching.saved(_s, "setup/trace")["id"]] if _s and teaching.saved(_s, "setup/trace") else (), question="Open inspect_training_environment in Agent Lens. Find workshop.exercise=solar-research and the NumPy version returned by the tool.") if _s else mo.md("Connect above first."), solar_next_step_2])
    return (first_trace, solar_next_step_2,)


# workshop-cell: solar_autoresearch/action/first_trace
@app.cell(hide_code=True)
def _(event, export_trace, first_trace, get_lab, instrument_tool, instrumentation_editor, mo, np, refresh_saved, set_feedback, teaching):
    mo.stop(not first_trace.value)
    _s = get_lab()["session"]
    teaching.check_instrumentation(instrumentation_editor.value)
    with _s.stage("setup/trace", config={"device": "cpu"}, sources={"instrumentation.py": instrumentation_editor.value}) as _stage:
        if _stage.needs_run:
            _result, _event = event("inspect_training_environment", {}, lambda: {"numpy": np.__version__, "device": "cpu"}, on_error=_stage.record_event)
            _stage.record({"events": [_event]})
    try:
        _trace = export_trace(_s, _stage.id, "Inspect my CPU research environment", _stage.result["events"], tool_writer=instrument_tool)
        _s.checkpoint("setup", evidence={"Setup conversation": _trace["url"]})
        set_feedback(lambda current: {**current, "setup_trace": {"status": "complete", "stored spans": _trace["stored_spans"]}})
    except Exception as _error:
        set_feedback(lambda current: {**current, "setup_trace": {"status": "publication pending", "message": str(_error), "next": "The check is saved. Click Send my first Agent Lens trace again to retry its upload."}})
    refresh_saved()
    return


# workshop-cell: solar_autoresearch/display/23
@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, mo, teaching, ui):
    mo.stop(get_step() != "setup")
    _status = get_feedback().get("setup_trace", {})
    _s = get_lab().get("session")
    _saved = teaching.saved(_s, "setup/trace") if _s else None
    _receipt = _s.read()["publications"].get("trace/" + _saved["id"], {}) if _saved else {}
    if not _status and _receipt.get("verified"):
        _status = {"status": "complete", "stored spans": _receipt["stored_spans"], "result": "Your saved trace is available in Agent Lens."}
    mo.Html(ui.result("Your first trace", _status, status=_status.get("status", "not sent"))) if _status else mo.md("Your trace will appear here after you click **Send my first Agent Lens trace**.")
    return


# workshop-cell: solar_autoresearch/controls/load_data
@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, ui):
    mo.stop(get_step() != "data")
    _s = get_lab().get("session")
    load_data = mo.ui.run_button(label="Load the solar dataset", disabled=not bool(_s))
    solar_prerequisite_3 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.vstack([mo.Html(ui.step("2. Inspect the observations", "Click Load the solar dataset. We’ll use SunPy to read an image’s FITS metadata, then look at the measurements we want to predict.", "Find the observation date and wavelength below. We train on February 1–10, compare changes on 11–12, and save 13–14 for the final test.")), mo.md("**Real observations, two prediction tasks.** First, use an hour of GOES-15 X-ray measurements to forecast flux 30 minutes ahead. The measurements are in W/m²; we predict log10 XRS-B flux. Later, use AIA 171 Å images of the Sun to predict an image one hour ahead. Both come from the February 2014 archives."), mo.md("[SunPy GOES retrieval](https://docs.sunpy.org/en/stable/generated/gallery/time_series/goes_xrs_example.html) · [AIA archive and calibration](https://jsoc1.stanford.edu/data/aia/synoptic/README.html) · [Our acquisition code](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_solar.py)"), load_data, solar_prerequisite_3 if not _s else mo.md("The download is about 26 MB. You’ll see the date, wavelength, and number of usable windows below."), mo.accordion({"What is reserved?": mo.md("A window contains the past observations and the future value we want to predict. Windows stay within their date split and are dropped if observations are missing. February 8 is missing from the GOES archive. We fit normalization on training data and keep the final dates out of the research agent’s input."), "Inspect the acquisition code": mo.md("[Source, quality checks and preprocessing](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_solar.py)")})])
    return (load_data, solar_prerequisite_3,)


# workshop-cell: solar_autoresearch/action/load_data
@app.cell(hide_code=True)
def _(dataset, get_lab, load_data, mo, set_lab, solar):
    mo.stop(not load_data.value)
    _s = get_lab()["session"]
    _path, _fingerprint = dataset()
    _goes, _normalization = solar.load_goes(_path)
    _images, _image_normalization = solar.load_aia(_path)
    from sunpy.map import Map
    _map = Map(_path / "sample-aia.fits")
    with _s.stage("data/loaded", inputs={"dataset": _fingerprint}) as _stage:
        if _stage.needs_run:
            _stage.record({"dataset": _fingerprint, "development_windows": {k: len(v["ids"]) for k, v in _goes.items() if k != "test"}, "normalization": _normalization, "image_date": str(_map.date), "wavelength": str(_map.wavelength)})
    _s.checkpoint("data")
    set_lab({**get_lab(), "data_path": str(_path), "dataset": _fingerprint, "goes": _goes, "goes_normalization": _normalization, "images": _images})
    return (Map,)


# workshop-cell: solar_autoresearch/definitions/solar_next_step_4
@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, plots, teaching, ui):
    mo.stop(get_step() != "data")
    _s = get_lab().get("session")
    _record = teaching.saved(_s, "data/loaded") if _s else None
    solar_next_step_4 = ui.next_step(mo, "Next: implement persistence", "baseline", go_to)
    mo.vstack([mo.Html(ui.result("Dataset loaded", _record["result"])) if _record else mo.md("Click Load the solar dataset to see the observations and a first forecast plot."), plots.forecast(get_lab()["goes"]["validation"]["persistence"], get_lab()["goes"]["validation"], title="Validation measurements: the latest observation as a forecast") if get_lab().get("goes") else mo.md("Returning to the notebook? Click Load the solar dataset to put the arrays back in memory. Your completed experiments stay saved."), ui.evidence(mo, _s, stage_ids=[_record["id"]], question="Open data / loaded · files. This W&B Artifact is a versioned collection of saved files. Find the observation date and wavelength in its dataset record; later runs will save code, weights, and predictions the same way.") if _record else mo.md(""), solar_next_step_4])
    return (solar_next_step_4,)


# workshop-cell: solar_autoresearch/definitions/window_split
@app.cell(hide_code=True)
def _(get_lab, get_step, mo):
    mo.stop(get_step() not in ("data", "baseline"))
    mo.stop(not get_lab().get("goes"))
    window_split = mo.ui.radio({"Training dates": "train", "Validation dates": "validation"}, value="Training dates", inline=True, label="Inspect an observed window")
    mo.vstack([mo.md("### Follow one observation into the model"), mo.md("Choose a window, then switch its input units. The future target stays in log-flux units. This viewer reads the data; it does not run a forecast."), window_split])
    return (window_split,)


# workshop-cell: solar_autoresearch/definitions/window_index
@app.cell(hide_code=True)
def _(get_lab, mo, window_split):
    _split = get_lab()["goes"][window_split.value]
    window_index = mo.ui.slider(start=0, stop=len(_split["ids"])-1, value=0, step=1, show_value=True, label="Window index")
    window_standardized = mo.ui.checkbox(label="Show the standardized inputs the neural model receives")
    mo.hstack([window_index, window_standardized])
    return (window_index, window_standardized,)


# workshop-cell: solar_autoresearch/display/29
@app.cell(hide_code=True)
def _(get_lab, mo, views, window_index, window_split, window_standardized):
    _values = views.window_values(get_lab()["goes"][window_split.value], get_lab()["goes_normalization"], window_index.value, standardized=window_standardized.value)
    mo.vstack([views.window_figure(_values), mo.ui.table(views.window_rows(_values), selection=None, pagination=False), mo.md("**Code to inspect:** `x = (log_flux - training_mean) / training_std`. Only the input changes scale. `split['persistence']` holds the latest log10 XRS-B reading; `split['y']` is the future target. Copying the standardized last input would give the baseline the wrong units."), mo.accordion({"Why some times have no window": mo.md("`load_goes` checks every minute from the first input through the target, including the 30-minute gap after the forecast origin. A missing minute or a crossed date boundary rejects that window. February 8 is absent from this archive. The slider contains accepted windows only.")})])
    return


# workshop-cell: solar_autoresearch/controls/check_persistence
@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, teaching, ui):
    mo.stop(get_step() != "baseline")
    _s = get_lab().get("session")
    solar_prerequisite_5 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.stop(not _s, solar_prerequisite_5)
    persistence_editor = mo.ui.code_editor(value=_s.get_draft("solar/persistence", teaching.PERSISTENCE_STARTER), language="python", min_height=130, label="Implement persistence_forecast", on_change=lambda value: _s.save_draft("solar/persistence", value))
    check_persistence = mo.ui.run_button(label="Check my persistence function")
    baseline_button = mo.ui.run_button(label="Run my persistence baseline", disabled=not bool(get_lab().get("goes")))
    solar_prerequisite_6 = ui.prerequisite(mo, "Load the dataset before running the baseline.", "data", go_to)
    mo.vstack([mo.Html(ui.step("3. Predict 30 minutes ahead by copying the latest reading", "In persistence_forecast, replace the exception with a copy of the latest measurement. This is persistence: predict that the current value will stay the same. Check the function, then click Run my persistence baseline.", "Read its validation error below. This is the score your trained models will try to beat.")), persistence_editor, check_persistence, mo.accordion({"Hint": mo.md("Use `split['persistence'].copy()`. The latest value is already provided; you don’t need the future target in `split['y']`."), "Worked answer": mo.md("```python\n" + teaching.PERSISTENCE_SOLUTION + "\n```")}), baseline_button, solar_prerequisite_6 if not get_lab().get("goes") else mo.md("After the check passes, run your function and compare its error with the models in the next step.")])
    return (baseline_button, check_persistence, persistence_editor, solar_prerequisite_5, solar_prerequisite_6,)


# workshop-cell: solar_autoresearch/action/check_persistence
@app.cell(hide_code=True)
def _(check_persistence, checked, mo, persistence_editor, teaching):
    mo.stop(not check_persistence.value)
    checked("persistence-check", lambda: teaching.check_persistence(persistence_editor.value))
    return


# workshop-cell: solar_autoresearch/action/baseline_button
@app.cell(hide_code=True)
def _(baseline_button, export_trace, get_lab, instrument_tool, mo, np, persistence_editor, refresh_saved, set_feedback, solar, teaching, time):
    mo.stop(not baseline_button.value)
    teaching.check_persistence(persistence_editor.value)
    _s = get_lab()["session"]
    _split = get_lab()["goes"]["validation"]
    with _s.stage("goes/persistence", inputs={"dataset": get_lab()["dataset"], "split": "validation"}, sources={"persistence.py": persistence_editor.value}) as _stage:
        if _stage.needs_run:
            _started = time.time()
            _prediction = teaching.functions(persistence_editor.value)["persistence_forecast"](_split)
            np.save(_stage.output_dir / "predictions.npy", _prediction)
            _metrics = solar.score(_prediction, _split)
            _stage.record({"metrics": _metrics, "events": [{"id": _stage.id + "/predict", "name": "persistence_forecast", "arguments": {"split": "validation", "windows": len(_split["ids"])}, "result": _metrics, "started_at": _started, "ended_at": time.time()}]}, files=[_stage.output_dir / "predictions.npy"])
    try:
        export_trace(_s, _stage.id, "Evaluate my persistence forecast on validation dates", _stage.result["events"], tool_writer=instrument_tool)
    except Exception as _error:
        set_feedback(lambda current: {**current, "baseline-export": str(_error)})
    _s.checkpoint("baseline")
    refresh_saved()
    return


# workshop-cell: solar_autoresearch/definitions/solar_next_step_7
@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, go_to, mo, persistence_editor, teaching, ui):
    mo.stop(get_step() != "baseline")
    _s = get_lab().get("session")
    _row = teaching.saved(_s, "goes/persistence") if _s else None
    _check = get_feedback().get("persistence-check", {})
    solar_next_step_7 = ui.next_step(mo, "Next: track six model configurations", "search", go_to)
    mo.vstack([mo.md(teaching.draft_status(_s, "solar/persistence", persistence_editor.value)) if _s else mo.md(""), mo.Html(ui.result("Local function check", _check, status=_check.get("status", "not checked"))), mo.Html(ui.result("Persistence validation result", _row["result"].get("metrics", {}))) if _row else mo.md("Click Run my persistence baseline to calculate its validation error."), ui.evidence(mo, _s, stage_ids=[_row["id"]], question="Open the persistence run. Find its error and validation dates, then open its files and compare persistence.py with the function you wrote.") if _row else mo.md(""), solar_next_step_7])
    return (solar_next_step_7,)


# workshop-cell: solar_autoresearch/display/34
@app.cell(hide_code=True)
def _():
    DEFAULT_SOURCE = '"""Editable research code. The data split and final scorer live elsewhere."""\nimport torch\nfrom torch import nn\n\n\ndef build_model(input_shape, config):\n    width=config.get(\'width\',16)\n    architecture=config.get(\'architecture\',\'mlp\')\n    if len(input_shape)==2:\n        if architecture==\'mlp\':\n            return nn.Sequential(nn.Flatten(),nn.Linear(input_shape[0]*input_shape[1],width),\n                                 nn.ReLU(),nn.Linear(width,1))\n        return nn.Sequential(nn.Conv1d(input_shape[0],width,5,padding=2),nn.ReLU(),\n                             nn.AdaptiveAvgPool1d(1),nn.Flatten(),nn.Linear(width,1))\n    class ImagePredictor(nn.Module):\n        def __init__(self):\n            super().__init__()\n            self.net=nn.Sequential(nn.Conv2d(2,width,3,padding=1),nn.ReLU(),\n                                   nn.Conv2d(width,width,3,padding=1),nn.ReLU(),\n                                   nn.Conv2d(width,1,3,padding=1))\n        def forward(self,x):\n            prediction=self.net(x)\n            return prediction+x[:,1:2] if architecture==\'residual\' else prediction\n    return ImagePredictor()\n\n\ndef training_loss(prediction,target,mask):\n    return ((prediction-target).square()*mask).sum()/mask.sum()\n\n\ndef fit(model,x,y,mask,config):\n    optimizer=torch.optim.Adam(model.parameters(),lr=config.get(\'learning_rate\',.001))\n    generator=torch.Generator().manual_seed(config.get(\'seed\',17))\n    losses=[]\n    model.train()\n    for step in range(config.get(\'steps\',40)):\n        indices=torch.randint(len(x),(min(config.get(\'batch_size\',16),len(x)),),generator=generator)\n        prediction=model(x[indices])\n        loss=training_loss(prediction,y[indices],mask[indices])\n        optimizer.zero_grad()\n        loss.backward()\n        optimizer.step()\n        losses.append(float(loss.detach()))\n    return losses\n'
    GOES_REPAIR_SOURCE = '"""Predict log-flux on a consistent scale, optionally correcting persistence.\n\nThe caller supplies normalization fitted on training observations only. Validation\nand final targets never enter build_model or fit.\n"""\nimport torch\nfrom torch import nn\n\n\ndef build_model(input_shape, config):\n    width = config.get("width", 16)\n\n    class FluxPredictor(nn.Module):\n        def __init__(self):\n            super().__init__()\n            if config["architecture"] == "mlp":\n                self.net = nn.Sequential(\n                    nn.Flatten(), nn.Linear(input_shape[0] * input_shape[1], width),\n                    nn.ReLU(), nn.Linear(width, 1),\n                )\n            else:\n                self.net = nn.Sequential(\n                    nn.Conv1d(input_shape[0], width, 5, padding=2), nn.ReLU(),\n                    nn.AdaptiveAvgPool1d(1), nn.Flatten(), nn.Linear(width, 1),\n                )\n            self.residual = config["residual"]\n            self.register_buffer("center", torch.tensor(float(config["target_center"])))\n            self.register_buffer("scale", torch.tensor(float(config["target_scale"])))\n            if self.residual:\n                nn.init.zeros_(self.net[-1].weight)\n                nn.init.zeros_(self.net[-1].bias)\n\n        def forward(self, x):\n            value = self.net(x)\n            if self.residual:\n                value = value + x[:, 1, -1:]\n            return value * self.scale + self.center\n\n    return FluxPredictor()\n\n\ndef training_loss(prediction, target, mask):\n    return ((prediction - target).abs() * mask).sum() / mask.sum()\n\n\ndef fit(model, x, y, mask, config):\n    optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"])\n    generator = torch.Generator().manual_seed(config["seed"])\n    losses = []\n    model.train()\n    for _ in range(config["steps"]):\n        indices = torch.randint(len(x), (min(config["batch_size"], len(x)),), generator=generator)\n        # Both prediction and target use the same training-fitted flux scale.\n        loss = training_loss(model(x[indices]), y[indices], mask[indices]) / model.scale\n        optimizer.zero_grad()\n        loss.backward()\n        optimizer.step()\n        losses.append(float(loss.detach()))\n    return losses\n'
    return (DEFAULT_SOURCE, GOES_REPAIR_SOURCE,)


# workshop-cell: solar_autoresearch/controls/check_measurement
@app.cell(hide_code=True)
def _(DEFAULT_SOURCE, get_lab, get_step, go_to, mo, teaching, ui):
    mo.stop(get_step() != "search")
    _s = get_lab().get("session")
    solar_prerequisite_8 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.stop(not _s, solar_prerequisite_8)
    measurement_editor = mo.ui.code_editor(value=_s.get_draft("solar/measurement", teaching.model_starter(DEFAULT_SOURCE, "measurement")), language="python", min_height=320, max_height=650, label="Measurement model source: complete training_loss", on_change=lambda value: _s.save_draft("solar/measurement", value))
    flux_metric_editor = mo.ui.code_editor(value=_s.get_draft("solar/flux-metric", teaching.FLUX_STARTER), language="python", min_height=120, label="Implement my_flux_mae", on_change=lambda value: _s.save_draft("solar/flux-metric", value))
    check_measurement = mo.ui.run_button(label="Check my measurement code")
    solar_prerequisite_9 = ui.prerequisite(mo, "Load the dataset before training.", "data", go_to)
    mo.vstack([mo.Html(ui.step("4. Follow the model before training it", "Start with build_model in the source below. Choose an architecture and use the free forward-pass check to see how a batch becomes a prediction. Then complete training_loss and my_flux_mae.", "Train one tracked Sweep trial, inspect its files and forecast, then schedule the remaining five configurations.")), measurement_editor, solar_prerequisite_9 if not get_lab().get("goes") else mo.md("The free shape check does not train weights. Your loss and metric will be checked before the first training run.")])
    return (check_measurement, flux_metric_editor, measurement_editor, solar_prerequisite_8, solar_prerequisite_9,)


# workshop-cell: solar_autoresearch/action/check_measurement
@app.cell(hide_code=True)
def _(check_measurement, checked, flux_metric_editor, measurement_editor, mo, teaching):
    mo.stop(not check_measurement.value)
    def _check():
        return {"model": teaching.check_model(measurement_editor.value, "measurement"), "metric": teaching.check_flux_metric(flux_metric_editor.value)}
    checked("measurement-check", _check)
    return


# workshop-cell: solar_autoresearch/controls/inspect_shapes
@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, ui):
    mo.stop(get_step() != "search")
    shape_architecture = mo.ui.radio({"MLP": "mlp", "Temporal CNN": "cnn"}, value="MLP", inline=True, label="Which implementation should receive a batch?")
    inspect_shapes = mo.ui.run_button(label="Run one forward pass and show tensor shapes", disabled=not bool(get_lab().get("session")))
    solar_shapes_prerequisite = ui.prerequisite(mo, "Connect to open your editable model source, then return here for the free shape check.", "setup", go_to)
    mo.vstack([mo.md("### Follow a batch through your code"), mo.md("Choose an architecture and run one forward pass with two synthetic inputs. It uses your current `build_model` function. No weights are trained and no provider is called. N is the batch size; the other axes are channels and time."), shape_architecture, inspect_shapes, solar_shapes_prerequisite if not get_lab().get("session") else mo.md("")])
    return (inspect_shapes, shape_architecture, solar_shapes_prerequisite,)


# workshop-cell: solar_autoresearch/action/inspect_shapes
@app.cell(hide_code=True)
def _(checked, digest, inspect_shapes, measurement_editor, mo, shape_architecture, views):
    mo.stop(not inspect_shapes.value)
    checked("forward-shapes", lambda: {"source": digest(measurement_editor.value), "architecture": shape_architecture.value, "layers": views.forward_shapes(measurement_editor.value, shape_architecture.value)})
    return


# workshop-cell: solar_autoresearch/display/39
@app.cell(hide_code=True)
def _(digest, get_feedback, get_step, measurement_editor, mo):
    mo.stop(get_step() != "search")
    _check = get_feedback().get("forward-shapes", {})
    mo.vstack([mo.ui.table(_check.get("layers", []), selection=None, pagination=False), mo.md("MLP flattens two channels × 60 samples into 120 numbers. CNN slides five-sample filters across those channels, then averages the time positions. Both return one prediction per input."), mo.md("This shape check used an earlier draft. Click the forward-pass button again to inspect your current code.") if _check.get("source") and _check["source"] != digest(measurement_editor.value) else mo.md("")]) if _check.get("status") == "complete" else mo.md(_check.get("message", "Run the forward pass to see its intermediate shapes."))
    return


# workshop-cell: solar_autoresearch/explanation/loss
@app.cell(hide_code=True)
def _(get_step, mo):
    mo.stop(get_step() != 'search')
    mo.md("### Read the calculation before filling the gap\nThe subtraction measures each miss. Squaring makes large misses count more during training; absolute error keeps the reported score in the target's units. This excerpt explains the existing loss, not a new training recipe.\n```python\n# One predicted value is compared with its matching target.\nerror = prediction - target\n# Keep only scored entries. GOES uses an all-ones mask.\nweighted_error = error.square() * mask\n# Divide by the number of included entries, not the tensor's size.\nloss = weighted_error.sum() / mask.sum()\n```\nFor an illustrative miss of −0.5, squared loss is 0.25 and absolute error is 0.5. Opposite-signed misses cannot cancel in either calculation. Training updates forecasting weights; validation only measures them.")
    return


# workshop-cell: solar_autoresearch/display/41
@app.cell(hide_code=True)
def _(check_measurement, flux_metric_editor, get_step, mo, teaching):
    mo.stop(get_step() != "search")
    mo.vstack([mo.md("### Write the loss and the reported metric"), mo.md("Complete `training_loss` in the model source above, then implement `my_flux_mae` below. The loss trains the model; MAE measures its forecast error. A negative miss must not cancel a positive one."), flux_metric_editor, check_measurement, mo.accordion({"Hint": mo.md("Square the prediction error, multiply by the mask, sum, and divide by the mask sum for training_loss. Average absolute errors for my_flux_mae."), "Worked answers": mo.md("```python\ndef training_loss(prediction, target, mask):\n    return ((prediction - target).square() * mask).sum() / mask.sum()\n\n" + teaching.FLUX_SOLUTION + "\n```"), "The six settings": mo.md("Three width/learning-rate pairs for each architecture. All six use seed 17, 60 updates, and batch size 32. The first trial and remaining trials belong to this same Sweep.")})])
    return


# workshop-cell: solar_autoresearch/display/42
@app.cell(hide_code=True)
def _(get_step, mo):
    mo.stop(get_step() != "search")
    mo.accordion({"Read run_training in three parts": mo.md("**1. Execute:** `training.train(...)` runs the source you wrote and returns predictions and metrics.\n\n**2. Save:** `stage.record(..., files=...)` preserves that source with weights.pt, predictions.npy, losses.json, and the plot. A W&B Artifact is the versioned bundle of those files.\n\n**3. Inspect:** `export_trace(...)` sends the observed training call to Agent Lens. `session.checkpoint(name)` saves progress. A failed upload can be retried without training again.\n\nFind these three statements in the editable function below. After a run, open the matching training span and its Artifact.")})
    return


# workshop-cell: solar_autoresearch/definitions/run_training
@app.cell
def _(event, export_trace, instrument_tool, np, plots, teaching, training):
    def run_training(session, name, source, splits, config, data_fingerprint, metric_source):
        # The learner's source and metric both belong to this execution's identity.
        with session.stage(name, config=config,
            sources={"candidate.py": source, "development_metric.py": metric_source},
            inputs={"dataset": data_fingerprint, "split": "validation"}) as stage:
            if stage.needs_run:
                (result, prediction), training_event = event("train_and_validate",
                    {"config": config, "source_fingerprint": stage.source_fingerprint, "split": "validation"},
                    lambda: training.train(source, splits["train"], splits["validation"], config, stage.output_dir),
                    on_error=stage.record_event)
                figure = plots.forecast(prediction, splits["validation"], title=name)
                figure.savefig(stage.output_dir / "predictions.png", dpi=130)
                functions = teaching.functions(metric_source)
                learner_error = functions["my_flux_mae"](prediction, splits["validation"]["y"]) if prediction.ndim == 2 else functions["my_image_mae"](prediction, splits["validation"]["y"], splits["validation"]["mask"])
                result["metrics"]["learner_metric"] = learner_error
                result["metrics"]["learner_metric_matches"] = bool(np.isclose(learner_error, result["metrics"]["error"]))
                training_event.update(id=stage.id + "/train", result=result["metrics"])
                result["events"] = [training_event]
                # These files, not just the score, make the result reproducible.
                stage.record(result, files=[stage.output_dir / file for file in ("candidate.py", "weights.pt", "predictions.npy", "predictions.png", "losses.json", "stderr.txt")])
        try:
            export_trace(session, stage.id, "Train this exact code and evaluate it on validation dates", stage.result["events"], tool_writer=instrument_tool)
        except Exception as error:
            with session.transaction() as state:
                state["publications"].setdefault("trace/" + stage.id, {}).update(status="unavailable", error=str(error))
            # The execution stays complete. Retry exports from the final step without training.
        session.checkpoint(name)
        return teaching.training_record(session, session.read()["stages"][stage.id])
    return (run_training,)


# workshop-cell: solar_autoresearch/definitions/run_measurement_sweep
@app.cell
def _(digest, flux_metric_editor, get_lab, measurement_editor, os, refresh_saved, run_training, teaching):
    def run_measurement_sweep(max_new_trials):
        import wandb
        teaching.check_model(measurement_editor.value, "measurement")
        teaching.check_flux_metric(flux_metric_editor.value)
        session = get_lab()["session"]
        plan = teaching.freeze_search_plan(session, measurement_editor.value, flux_metric_editor.value, get_lab()["dataset"])
        with session.stage("goes/create-sweep", inputs={"source": plan["source"], "metric": plan["metric"], "configurations": plan["configurations"]}) as sweep_stage:
            if sweep_stage.needs_run:
                sweep_id = wandb.sweep({"method": "grid", "metric": {"name": "validation_error", "goal": "minimize"}, "parameters": {"trial": {"values": list(range(6))}}}, entity=session.project.split('/')[0], project=session.project.split('/')[1])
                sweep_stage.record({"sweep_id": sweep_id})
        sweep_id = sweep_stage.result["sweep_id"]
        path = session.project + "/" + sweep_id.split('/')[-1]
        def scheduled():
            native = [{"trial": int(run.config["trial"]), "id": run.id, "state": run.state} for run in wandb.Api().sweep(path).runs]
            local = list(session.read().get("solar_sweep_trials", {}).get(sweep_id, {}).values())
            status = teaching.sweep_assignments(native, local)
            for row in native:
                teaching.record_sweep_assignment(session, sweep_id, row["trial"], row["id"], row["state"])
            return status
        before = scheduled()
        if max_new_trials > 1 and not before["finished"]:
            raise ValueError("Run one tracked Sweep trial first, then inspect its saved result before scheduling the remaining configurations.")
        if before["unresolved"]:
            raise ValueError("An assigned Sweep run is still running, failed, or unavailable. Inspect its native run before requesting more jobs; no ambiguous trial is resent. Saved training remains available.")
        # A cached model is not a scheduled Sweep job. Its job still has to publish
        # that cached result under the appropriate trial index.
        count = min(max_new_trials, len(before["unassigned"]))
        if max_new_trials == 1 and before["assigned"]:
            count = 0
        def trial():
            run_id, index = None, None
            try:
                with wandb.init(entity=session.project.split('/')[0], project=session.project.split('/')[1], job_type="workshop-sweep") as run:
                    index, run_id = int(run.config.trial), run.id
                    config = plan["configurations"][index]
                    teaching.record_sweep_assignment(session, sweep_id, index, run_id, "running")
                    run.name = f"GOES / {config['architecture'].upper()} / width {config['width']} / lr {config['learning_rate']}"
                    run.config.update({"experiment": config, "dataset": plan["dataset"], "source_fingerprint": digest({"candidate.py": plan["source"], "development_metric.py": plan["metric"]})})
                    publisher = session.publisher
                    session.publisher = None
                    try:
                        record = run_training(session, "goes/search-" + str(index), plan["source"], get_lab()["goes"], config, plan["dataset"], plan["metric"])
                    finally:
                        session.publisher = publisher
                    run.summary["execution_stage"] = record["stage_id"]
                    run.log(record["metrics"])
                teaching.record_sweep_assignment(session, sweep_id, index, run_id, "finished")
            except Exception:
                if run_id is not None:
                    teaching.record_sweep_assignment(session, sweep_id, index, run_id, "failed")
                raise
        if count:
            environment = {key: os.environ.get(key) for key in ("WANDB_RUN_ID", "WANDB_SWEEP_ID", "WANDB_SWEEP_PARAM_PATH")}
            try:
                wandb.agent(sweep_id, function=trial, count=count, entity=session.project.split('/')[0], project=session.project.split('/')[1])
            finally:
                for key, value in environment.items():
                    if value is None: os.environ.pop(key, None)
                    else: os.environ[key] = value
        status = scheduled()
        rows = teaching.sweep_training_rows(session, plan)
        complete = len(status["finished"]) == len(rows) == 6
        session.checkpoint("search" if complete else "search-first-trial", evidence={"Measurement Sweep": "https://wandb.ai/" + session.project + "/sweeps/" + sweep_id.split('/')[-1]})
        refresh_saved()
        return {"Sweep trial assignments": len(status["assigned"]), "Finished Sweep runs": len(status["finished"]), "Saved training results": len(rows), "Still unassigned": status["unassigned"], "Unresolved Sweep runs": status["unresolved"], "Complete": complete}
    return (run_measurement_sweep,)


# workshop-cell: solar_autoresearch/controls/run_first_trial
@app.cell(hide_code=True)
def _(get_lab, get_step, mo, teaching):
    mo.stop(get_step() != "search")
    _s = get_lab().get("session")
    _plan = teaching.saved(_s, "goes/sweep-plan") if _s else None
    _sweep = teaching.saved(_s, "goes/create-sweep") if _s else None
    _trials = _s.read().get("solar_sweep_trials", {}).get(_sweep["result"]["sweep_id"], {}) if _sweep else {}
    _first_done = any(row["state"] == "finished" for row in _trials.values())
    _locked = bool(_s and teaching.saved(_s, "images/freeze"))
    run_first_trial = mo.ui.run_button(label="Run one tracked Sweep trial", disabled=not bool(get_lab().get("goes")) or _locked or _first_done)
    run_search = mo.ui.run_button(label="Run the remaining Sweep trials", disabled=not _first_done or _locked)
    restore_search_code = mo.ui.run_button(label="Restore the frozen Sweep drafts", disabled=not bool(_plan))
    mo.vstack([mo.md("### Train one configuration, then inspect it"), mo.md("The first button schedules one job in the six-configuration Sweep. Open that run's configuration, loss curve, source, and predictions below. Then schedule the remaining five. Both buttons use the same frozen model source, metric, dataset and settings. Editing a draft after the first trial does not change that Sweep."), run_first_trial, run_search, mo.accordion({"Changed a draft during the Sweep?": mo.vstack([mo.md("Restore the frozen drafts, then return to this step to reload the editors. A saved training result can be reused by its matching Sweep job; it does not count as a job that has already been scheduled."), restore_search_code])})])
    return (restore_search_code, run_first_trial, run_search,)


# workshop-cell: solar_autoresearch/action/run_first_trial
@app.cell
def _(checked, mo, run_first_trial, run_measurement_sweep):
    mo.stop(not run_first_trial.value)
    checked("sweep", lambda: run_measurement_sweep(1))
    return


# workshop-cell: solar_autoresearch/action/run_search
@app.cell
def _(checked, mo, run_measurement_sweep, run_search):
    mo.stop(not run_search.value)
    checked("sweep", lambda: run_measurement_sweep(6))
    return


# workshop-cell: solar_autoresearch/action/restore_search_code
@app.cell(hide_code=True)
def _(get_lab, mo, refresh_saved, restore_search_code, teaching):
    mo.stop(not restore_search_code.value)
    _s = get_lab()["session"]
    _plan = teaching.saved(_s, "goes/sweep-plan")["result"]
    _s.save_draft("solar/measurement", _plan["source"])
    _s.save_draft("solar/flux-metric", _plan["metric"])
    refresh_saved()
    mo.md("Frozen drafts restored. Leave Track and search and return to reload the editors.")
    return


# workshop-cell: solar_autoresearch/display/49
@app.cell(hide_code=True)
def _(get_feedback, get_step, mo, ui):
    mo.stop(get_step() != "search")
    _status = get_feedback().get("sweep")
    mo.Html(ui.result("Sweep scheduling and saved training", _status, status=_status.get("status", "not started"))) if _status else mo.md("")
    return


# workshop-cell: solar_autoresearch/display/50
@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, measurement_editor, mo, teaching, ui):
    mo.stop(get_step() != "search")
    _s = get_lab().get("session")
    _plan = teaching.saved(_s, "goes/sweep-plan") if _s else None
    _rows = teaching.sweep_training_rows(_s, _plan["result"]) if _plan else [] if not _s else [row for row in _s.completed() if row["name"].startswith("goes/search-")]
    _check = get_feedback().get("measurement-check", {})
    mo.vstack([mo.md(teaching.draft_status(_s, "solar/measurement", measurement_editor.value, stage_prefix="goes/search-")) if _s else mo.md(""), mo.Html(ui.result("Local measurement checks", _check, status=_check.get("status", "not checked"))), mo.ui.table([{"Run": row["name"], "Architecture": row["config"]["architecture"], "Width": row["config"]["width"], "Learning rate": row["config"]["learning_rate"], **row["result"]["metrics"]} for row in _rows], selection=None), ui.evidence(mo, _s, stage_ids=[row["id"] for row in _rows], question="Open the Measurement Sweep and choose one MLP and one CNN. Compare validation_error, width, and learning rate. In each run’s files, find candidate.py and losses.json to see which code trained and how its loss changed.") if _s else mo.md("")])
    return


# workshop-cell: solar_autoresearch/display/51
@app.cell(hide_code=True)
def _(get_lab, get_step, mo, teaching):
    mo.stop(get_step() != "search")
    _s = get_lab().get("session")
    _plan = teaching.saved(_s, "goes/sweep-plan") if _s else None
    _rows = teaching.sweep_training_rows(_s, _plan["result"]) if _plan else [] if not _s else [row for row in _s.completed() if row["name"].startswith("goes/search-") and "validation_error" in row["result"].get("metrics", {})]
    _options = {row["name"] + " · " + row["config"]["architecture"] + " · " + row["id"][:6]: row["id"] for row in _rows}
    inspect_goes_run = mo.ui.dropdown(_options, value=next(iter(_options), None), label="Inspect a saved measurement run", full_width=True) if _options else None
    mo.vstack([mo.md("### Bring a forecast to the lab review"), mo.md("A decreasing training loss is not enough. Compare the saved model forecast with persistence and the observed future. This reads saved arrays; it does not extend training."), inspect_goes_run]) if _options else mo.md("")
    return (inspect_goes_run,)


# workshop-cell: solar_autoresearch/display/52
@app.cell(hide_code=True)
def _(get_lab, inspect_goes_run, mo, np, ui, views):
    mo.stop(inspect_goes_run is None)
    _s = get_lab()["session"]
    _row = _s.read()["stages"][inspect_goes_run.value]
    _path = _s.file("outputs/" + _row["id"] + "/predictions.npy")
    mo.stop(not get_lab().get("goes"), mo.md("Load the solar dataset to inspect this saved forecast."))
    mo.stop(not _path.exists(), mo.md("The prediction file is missing. Restore its saved Artifact before comparing it."))
    _metrics = _row["result"]["metrics"]
    _primary = {label: _metrics[key] for key, label in (("error", "Forecast MAE"), ("persistence_error", "Persistence MAE"), ("examples", "Validation windows"), ("seconds", "Execution seconds")) if key in _metrics}
    mo.vstack([mo.Html(ui.result("Settings used for this execution", _row["config"])), views.goes_investigation(np.load(_path, allow_pickle=False), get_lab()["goes"]["validation"], losses=_row["result"].get("losses", []), title=_row["name"]), mo.Html(ui.result("Validation result", _primary)), mo.accordion({"All saved metrics, including your development scorer": mo.Html(ui.result("Saved metrics", _metrics))}), ui.evidence(mo, _s, stage_ids=[_row["id"]], question="Open this run’s training span and find steps and learning_rate. Then open losses.json in its files. Do the saved values match this plot?")])
    return


# workshop-cell: solar_autoresearch/definitions/goes_diagnosis
@app.cell(hide_code=True)
def _(get_lab, get_step, mo):
    mo.stop(get_step() != "search")
    _s = get_lab().get("session")
    mo.stop(not _s)
    goes_diagnosis = mo.ui.text_area(value=_s.get_draft("solar/goes-diagnosis", ""), label="What would you check before changing this model?", full_width=True, on_change=lambda value: _s.save_draft("solar/goes-diagnosis", value))
    show_goes_repair = mo.ui.checkbox(label="Show the worked GOES repair and its recorded results", value=_s.get_draft("solar/show-goes-repair", "") == "yes", on_change=lambda value: _s.save_draft("solar/show-goes-repair", "yes" if value else ""))
    mo.vstack([mo.md("### Diagnose the forecast before reading the repair"), mo.md("For your selected validation run, compare the output's units with the target, the loss history, and the forecast. Write one possible cause and one check that could disprove it. A falling training loss alone does not establish better forecasting."), goes_diagnosis, mo.md("The diagnostic note is optional. It stays in your notebook and is not supplied to the research agent. Opening the worked answer does not train a model.")])
    return (goes_diagnosis, show_goes_repair,)


# workshop-cell: solar_autoresearch/aria/investigate
@app.cell(hide_code=True)
def _(aria, get_lab, get_step, goes_diagnosis, inspect_goes_run, mo, teaching):
    mo.stop(get_step() != "search")
    _s=get_lab().get("session")
    _baseline=teaching.saved(_s,"goes/persistence") if _s else None
    _ids=([inspect_goes_run.value] if inspect_goes_run is not None and inspect_goes_run.value else [])+([_baseline["id"]] if _baseline else [])
    solar_aria_investigate=aria.investigation(mo,_s,"investigate",record_ids=_ids,interpretation=goes_diagnosis.value,workshop="solar-autoresearch")
    mo.vstack([mo.md("Ask ARIA to check your diagnosis against the selected forecast, persistence, and loss history. If it suggests a cause, find the saved value supporting that explanation and name the experiment you would need to test it."),solar_aria_investigate])
    return (solar_aria_investigate,)


# workshop-cell: solar_autoresearch/aria_response/investigate
@app.cell(hide_code=True)
def _(aria, mo, show_goes_repair, solar_aria_investigate):
    mo.vstack([aria.response(mo,solar_aria_investigate),show_goes_repair])
    return


# workshop-cell: solar_autoresearch/controls/check_measurement_repair
@app.cell(hide_code=True)
def _(GOES_REPAIR_SOURCE, get_lab, get_step, mo, show_goes_repair, teaching):
    mo.stop(get_step() != "search" or not show_goes_repair.value)
    _s = get_lab()["session"]
    measurement_repair_editor = mo.ui.code_editor(value=_s.get_draft("solar/measurement-repair", GOES_REPAIR_SOURCE), language="python", min_height=280, max_height=650, label="Worked GOES repair: inspect or edit the forecasting code", on_change=lambda value: _s.save_draft("solar/measurement-repair", value))
    check_measurement_repair = mo.ui.run_button(label="Check the GOES repair code")
    run_measurement_repair = mo.ui.run_button(label="Train the worked GOES repair", disabled=not bool(get_lab().get("goes")) or teaching.saved(_s, "images/freeze") is not None)
    mo.vstack([mo.md("### Worked answer: compare your diagnosis with this recipe"), mo.md("`forward` adds a learned correction to the latest standardized XRS-B reading, then converts back to log-flux units. The correction starts at zero. `fit` puts predictions and targets on the same training-fitted scale and trains for 1,200 updates. Inspect those lines before running the recipe."), measurement_repair_editor, check_measurement_repair, run_measurement_repair, mo.md("**Recorded original result:** the 60-update model scored 2.468975 on final dates; persistence scored 0.192706. This unsuccessful rehearsal remains part of the record. **Recorded qualification:** this fixed recipe beat persistence on seeds 17, 29, and 43. Those runs reused previously inspected final dates, so they are teaching retests. Your run is separate. The recipe changes several choices together and does not isolate which caused the gain. [All qualification outcomes](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-qualification.md).")])
    return (check_measurement_repair, measurement_repair_editor, run_measurement_repair,)


# workshop-cell: solar_autoresearch/action/check_measurement_repair
@app.cell(hide_code=True)
def _(check_measurement_repair, checked, measurement_repair_editor, mo, teaching):
    mo.stop(not check_measurement_repair.value)
    checked("measurement-repair-check", lambda: teaching.check_model(measurement_repair_editor.value, "measurement"))
    return


# workshop-cell: solar_autoresearch/action/run_measurement_repair
@app.cell
def _(flux_metric_editor, get_lab, measurement_repair_editor, mo, refresh_saved, run_measurement_repair, run_training, teaching):
    mo.stop(not run_measurement_repair.value)
    teaching.check_model(measurement_repair_editor.value, "measurement")
    teaching.check_flux_metric(flux_metric_editor.value)
    _s = get_lab()["session"]
    _config = teaching.measurement_repair_config(get_lab()["goes_normalization"])
    run_training(_s, "goes/worked-repair", measurement_repair_editor.value, get_lab()["goes"], _config, get_lab()["dataset"], flux_metric_editor.value)
    refresh_saved()
    return


# workshop-cell: solar_autoresearch/definitions/solar_next_step_10
@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, go_to, mo, show_goes_repair, teaching, ui):
    mo.stop(get_step() != "search")
    _s = get_lab().get("session")
    _repair = teaching.saved(_s, "goes/worked-repair") if _s else None
    _check = get_feedback().get("measurement-repair-check", {})
    solar_next_step_10 = ui.next_step(mo, "Next: predict a solar image", "images", go_to)
    _repair_details = [mo.Html(ui.result("Repair code check", _check, status=_check.get("status", "not checked"))) if _check else mo.md("Click Check the GOES repair code above to test this function without training."), mo.Html(ui.result("Your worked repair", _repair["result"]["metrics"])) if _repair else mo.md("The repair has not run. Its button trains one model; editing this code does not start training."), ui.evidence(mo, _s, stage_ids=[_repair["id"]], question="Open this training call and its Artifact. Find the 1,200 updates, training-fitted scale, candidate.py, and weights.pt. Compare validation_error with the persistence run.") if _repair else mo.md("")] if show_goes_repair.value else []
    mo.vstack([*_repair_details, solar_next_step_10])
    return (solar_next_step_10,)


# workshop-cell: solar_autoresearch/controls/check_images
@app.cell(hide_code=True)
def _(DEFAULT_SOURCE, get_lab, get_step, go_to, mo, teaching, ui):
    mo.stop(get_step() != "images")
    _s = get_lab().get("session")
    solar_prerequisite_11 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.stop(not _s, solar_prerequisite_11)
    image_editor = mo.ui.code_editor(value=_s.get_draft("solar/image", teaching.model_starter(DEFAULT_SOURCE, "image")), language="python", min_height=320, max_height=650, label="Image model source: complete ImagePredictor.forward", on_change=lambda value: _s.save_draft("solar/image", value))
    image_metric_editor = mo.ui.code_editor(value=_s.get_draft("solar/image-metric", teaching.IMAGE_METRIC_STARTER), language="python", min_height=140, label="Implement my_image_mae", on_change=lambda value: _s.save_draft("solar/image-metric", value))
    check_images = mo.ui.run_button(label="Check my image code")
    _locked = teaching.saved(_s, "images/round-1/propose") is not None
    run_images = mo.ui.run_button(label="Compare convolutional and residual predictors", disabled=not bool(get_lab().get("images")) or _locked)
    solar_prerequisite_12 = ui.prerequisite(mo, "Load the image arrays before training.", "data", go_to)
    mo.vstack([mo.Html(ui.step("5. Predict the image, or predict its correction", "Complete ImagePredictor.forward: the residual model should add its predicted correction to the current image. Then finish my_image_mae, run the local check, and click Compare convolutional and residual predictors.", "Compare the two error scores and forecast images below. Where did the prediction miss a change on the solar disk?")), mo.md("**What these images represent.** AIA records the Sun in extreme ultraviolet light. We use its 171 Å channel, sampled every 12 minutes and reduced to 64×64 pixels. Each model sees an image from an hour ago and one from now, then predicts an hour ahead. The score averages absolute error over the solar disk; lower is better."), mo.md("[Inspect the source archive](https://jsoc1.stanford.edu/data/aia/synoptic/README.html) · [Inspect the preprocessing](https://github.com/ash0ts/forge-workshop-kit/blob/main/scripts/prepare_solar.py)"), image_editor, image_metric_editor, check_images, mo.accordion({"How the images are prepared": mo.md("We divide each image by exposure time, then apply log1p and normalize using training dates only. The fixed score uses this normalized intensity and ignores pixels outside the solar disk. The acquisition link above contains the source checks and preprocessing."), "Hint": mo.md("In the residual model, add `x[:, 1:2]` to the network output. For the metric, average each image’s error over pixels where disk_mask is true, then average the images. An error of +1 everywhere on the disk should score 1; an error outside the disk should score 0."), "Worked answers": mo.md("```python\ndef forward(self, x):\n    prediction = self.net(x)\n    return prediction + x[:, 1:2] if architecture == 'residual' else prediction\n\n" + teaching.IMAGE_METRIC_SOLUTION + "\n```")}), run_images, mo.md("The research agent has already started from your selected manual model. That starting version is now fixed for this comparison.") if _locked else solar_prerequisite_12 if not get_lab().get("images") else mo.md("These image edits are saved separately from your measurement model.")])
    return (check_images, image_editor, image_metric_editor, run_images, solar_prerequisite_11, solar_prerequisite_12,)


# workshop-cell: solar_autoresearch/action/check_images
@app.cell(hide_code=True)
def _(check_images, checked, image_editor, image_metric_editor, mo, teaching):
    mo.stop(not check_images.value)
    def _check():
        return {"model": teaching.check_model(image_editor.value, "image"), "metric": teaching.check_image_metric(image_metric_editor.value)}
    checked("image-check", _check)
    return


# workshop-cell: solar_autoresearch/controls/try_scorer
@app.cell(hide_code=True)
def _(get_step, mo):
    mo.stop(get_step() != "images")
    fixture_error = mo.ui.slider(start=-3, stop=3, step=.5, value=1, show_value=True, label="Error in the first synthetic image")
    fixture_inside = mo.ui.checkbox(value=True, label="Put the error inside the scoring mask")
    try_scorer = mo.ui.run_button(label="Try my image scorer on these pixels")
    mo.vstack([mo.md("### Check what the score counts"), mo.md("These two tiny grids are arithmetic examples, not solar observations. The second image has four included pixels and twice the error. Move the error outside the mask, then test your own function. Each image gets equal weight in the final average."), mo.hstack([fixture_error, fixture_inside]), try_scorer])
    return (fixture_error, fixture_inside, try_scorer,)


# workshop-cell: solar_autoresearch/display/63
@app.cell(hide_code=True)
def _(fixture_error, fixture_inside, mo, views):
    _fixture = views.scorer_fixture(fixture_error.value, inside=fixture_inside.value)
    mo.vstack([views.fixture_figure(_fixture), mo.ui.table(_fixture["rows"], selection=None, pagination=False), mo.md("Expected mean of the two image errors: **" + str(_fixture["expected"]) + "**. The target is zero, so each displayed signed value is prediction minus target.")])
    return


# workshop-cell: solar_autoresearch/action/try_scorer
@app.cell(hide_code=True)
def _(checked, digest, fixture_error, fixture_inside, image_metric_editor, mo, np, teaching, try_scorer, views):
    mo.stop(not try_scorer.value)
    def _try():
        identity = {"source": digest(image_metric_editor.value), "fixture": [fixture_error.value, fixture_inside.value]}
        example = views.scorer_fixture(fixture_error.value, inside=fixture_inside.value)
        try:
            actual = teaching.functions(image_metric_editor.value)["my_image_mae"](example["prediction"], example["target"], example["mask"])
            return {**identity, "Your scorer": float(actual), "Expected": example["expected"], "Matches": bool(np.isclose(actual, example["expected"]))}
        except Exception as error:
            return {**identity, "status": "needs work", "message": str(error), "Expected": example["expected"]}
    checked("fixture-score", _try)
    return


# workshop-cell: solar_autoresearch/display/65
@app.cell(hide_code=True)
def _(digest, fixture_error, fixture_inside, get_feedback, get_step, image_metric_editor, mo, ui):
    mo.stop(get_step() != "images")
    _result = get_feedback().get("fixture-score", {})
    _fresh = _result.get("source") == digest(image_metric_editor.value) and _result.get("fixture") == [fixture_error.value, fixture_inside.value]
    _visible = {key: _result[key] for key in ("Your scorer", "Expected", "Matches", "message") if key in _result}
    mo.vstack([mo.Html(ui.result("Your scorer on this example", _visible, status=_result.get("status", "not checked"))), mo.accordion({"Check details": mo.Html(ui.result("Saved local check", _result))})]) if _fresh else mo.md("Click Try my image scorer on these pixels to check the current code and selected example.")
    return


# workshop-cell: solar_autoresearch/action/run_images
@app.cell(hide_code=True)
def _(get_lab, image_editor, image_metric_editor, mo, refresh_saved, run_images, run_training, teaching):
    mo.stop(not run_images.value)
    teaching.check_model(image_editor.value, "image")
    teaching.check_image_metric(image_metric_editor.value)
    _s = get_lab()["session"]
    for _architecture in ("conv", "residual"):
        _config = {"architecture": _architecture, "width": 8, "learning_rate": .001, "steps": 40, "seed": 17, "batch_size": 8}
        run_training(_s, "images/manual-" + _architecture, image_editor.value, get_lab()["images"], _config, get_lab()["dataset"], image_metric_editor.value)
    _s.checkpoint("images")
    refresh_saved()
    return


# workshop-cell: solar_autoresearch/definitions/solar_next_step_13
@app.cell(hide_code=True)
def _(get_feedback, get_lab, get_step, go_to, image_editor, mo, teaching, ui):
    mo.stop(get_step() != "images")
    _s = get_lab().get("session")
    _rows = [] if not _s else [row for row in _s.completed() if row["name"].startswith("images/manual-")]
    _check = get_feedback().get("image-check", {})

    solar_next_step_13 = ui.next_step(mo, "Next: let the researcher propose code changes", "research", go_to)
    mo.vstack([mo.md(teaching.draft_status(_s, "solar/image", image_editor.value, stage_prefix="images/manual-")) if _s else mo.md(""), mo.Html(ui.result("Local image checks", _check, status=_check.get("status", "not checked"))) if _check else mo.md("**Your image results.** Saved runs appear below. If you change the code, check it before training again."), mo.ui.table(teaching.metric_rows({row["config"]["architecture"]: row["result"]["metrics"] for row in _rows}), selection=None), ui.evidence(mo, _s, stage_ids=[row["id"] for row in _rows], question="Pick one forecast where the models differ. Open that model’s files to find weights.pt, then its Agent Lens training span to see the settings and elapsed time. Describe the difference you can see in the error image.") if _s else mo.md(""), solar_next_step_13])
    return (solar_next_step_13,)


# workshop-cell: solar_autoresearch/definitions/comparison_timestamp
@app.cell(hide_code=True)
def _(get_lab, get_step, mo, teaching):
    mo.stop(get_step() not in ("images", "final"))
    _s = get_lab().get("session")
    mo.stop(not _s or not get_lab().get("images"))
    _final = get_step() == "final"
    mo.stop(_final and teaching.saved(_s, "images/final-comparison") is None)
    _split_name = "test" if _final else "validation"
    _split = get_lab()["images"][_split_name]
    _selection_key = "solar/comparison-timestamp/" + get_lab()["dataset"] + "/" + _split_name
    _origins = [str(timestamp) for timestamp in _split["ids"]]
    _selected_origin = _s.get_draft(_selection_key, _origins[0])
    if _selected_origin not in _origins:
        _selected_origin = _origins[0]
    comparison_timestamp = mo.ui.dropdown({origin + " UTC": i for i, origin in enumerate(_origins)}, value=_selected_origin + " UTC", label="Forecast origin · all versions use this timestamp", full_width=True, on_change=lambda value: _s.save_draft(_selection_key, _origins[value]) if value is not None else None)
    mo.vstack([mo.md("### Compare the same image across versions"), mo.md("Choose a timestamp. Persistence copies the current image; the other columns use saved predictions. Every forecast shares one intensity scale, and every error image shares another. The table separates this image’s error from the mean over the full split."), comparison_timestamp])
    return (comparison_timestamp,)


# workshop-cell: solar_autoresearch/display/69
@app.cell(hide_code=True)
def _(comparison_timestamp, get_lab, get_step, mo, teaching, ui, views):
    _s = get_lab()["session"]
    _final = get_step() == "final"
    _split = get_lab()["images"]["test" if _final else "validation"]
    _names = {"Manual": "images/final-manual", "Agent-edited": "images/final-agent"} if _final else {"Direct CNN": "images/manual-conv", "Residual CNN": "images/manual-residual"}
    _comparison = teaching.saved(_s, "images/final-comparison") if _final else None
    _executions = {label: views.comparison_execution(_s, _comparison, version) for label, version in (("Manual", "manual"), ("Agent-edited", "agent"))} if _final else None
    _predictions, _records, _unavailable = views.saved_predictions(_s, _names, _split, executions=_executions)
    _predictions = {"Persistence": _split["persistence"], **_predictions}
    _figure, _rows = views.aligned_images(_predictions, _split, index=comparison_timestamp.value)
    mo.vstack([mo.Html(views.comparison_html(_figure, _split["ids"][comparison_timestamp.value])), mo.ui.table(_rows, selection=None, pagination=False), mo.Html(ui.result("Unavailable versions", _unavailable, status="unavailable")) if _unavailable else mo.md(""), ui.evidence(mo, _s, stage_ids=[row["id"] for row in _records.values()], question="Open a version’s files and find predictions.npy. The selected timestamp has the same row index in every saved prediction array. In EvalTables, find the same forecast origin and compare its prediction, observed future, and disk-masked error images. The image mean is a summary, not the pixel-wise score.")])
    return


# workshop-cell: solar_autoresearch/display/70
@app.cell(hide_code=True)
def _(get_step, mo, ui):
    mo.stop(get_step() not in ("images", "research"))
    mo.vstack([
        mo.callout(mo.vstack([
            mo.md("**Recorded example · a completed rehearsal, separate from your results.**"),
            mo.md("| Frozen image model | Mean error |\n|---|---:|\n| Persistence | 0.12576 |\n| Manual model | 0.12244 |\n| Agent-edited model | 0.11001 |"),
            mo.md("**10.15% lower error than the manual model.** The selected edits zero-initialized the residual output layer and changed training loss to masked L1."),
            mo.md("That rehearsal used one seed and 199 overlapping windows on February 13–14, 2014. The GOES measurement model performed worse than persistence in that rehearsal. A later fixed-recipe check found image error fell for seeds 17 and 29 but rose slightly for seed 43. The mean fell across seeds; the edit did not help every run. The GOES repair above did beat persistence on all three seeds. [Inspect every qualification outcome](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/solar-qualification.md). Your results appear in your own comparison.")
        ]), kind="info"),
        mo.accordion({"Open the recorded evidence": mo.Html(ui.links({
            "Recorded result and limitations": "https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==",
            "Actual diffs and execution records": "https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/solar/public/recorded-study.json",
            "Selected code and weights": "https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/artifacts/workshop-execution/execution-f7550caa1639e8366efbf9d84a782289/v0",
        }))})
    ])
    return


# workshop-cell: solar_autoresearch/definitions/next_research_action
@app.cell
def _(teaching):
    def next_research_action(session):
        # This reads saved decisions. It never launches an action by itself.
        return teaching.next_action(session)

    def choose_adoption(parent, executed):
        # Lower validation error wins. Failed or equal candidates retain the parent.
        if executed.get("metrics", {}).get("validation_error", float("inf")) < parent["metrics"]["validation_error"]:
            return executed
        return parent
    return (choose_adoption, next_research_action,)


# workshop-cell: solar_autoresearch/controls/check_evidence
@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, teaching, ui):
    mo.stop(get_step() != "research")
    _s = get_lab().get("session")
    solar_prerequisite_14 = ui.prerequisite(mo, "Connect to your project first.", "setup", go_to)
    mo.stop(not _s, solar_prerequisite_14)
    evidence_editor = mo.ui.code_editor(value=_s.get_draft("solar/evidence", teaching.EVIDENCE_STARTER), language="python", min_height=180, label="Implement select_validation_evidence", on_change=lambda value: _s.save_draft("solar/evidence", value))
    check_evidence = mo.ui.run_button(label="Check my evidence selection")
    mo.vstack([mo.Html(ui.step("6. Test agent-written changes to the image model", "So far, you chose between model implementations and training settings. The research agent can also write changes to the Python implementation. Complete select_validation_evidence to give it the configuration, validation errors, loss history, and trace links from a training run. Check the function, then use the action button below to request two candidate changes.", "Read each diff before training it. After both candidates finish, ask the agent which changes to keep or combine, then train that version too. The next round uses the new version only if its validation error is lower; otherwise it keeps the previous model.")), mo.md("The research agent keeps the same model weights throughout. It edits Python code; your small forecasting models learn new weights when you train each candidate. The agent can change the model or loss, but the data splits and final scorer stay fixed."), evidence_editor, check_evidence, mo.accordion({"Hint": mo.md("Return the fields listed in the starter. Keep the check that rejects split='test': the agent must choose its edits before seeing final-test scores."), "Worked answer": mo.md("```python\n" + teaching.EVIDENCE_SOLUTION + "\n```")})])
    return (check_evidence, evidence_editor, solar_prerequisite_14,)


# workshop-cell: solar_autoresearch/action/check_evidence
@app.cell(hide_code=True)
def _(check_evidence, checked, digest, evidence_editor, mo, teaching):
    mo.stop(not check_evidence.value)
    checked("evidence-check", lambda: {**teaching.check_evidence(evidence_editor.value), "source_fingerprint": digest(evidence_editor.value)})
    return


# workshop-cell: solar_autoresearch/controls/research_button
@app.cell(hide_code=True)
def _(digest, evidence_editor, get_feedback, get_lab, get_step, go_to, mo, next_research_action, teaching, ui):
    mo.stop(get_step() != "research")
    _s = get_lab().get("session")
    mo.stop(not _s, mo.md("Connect first."))
    _number, _phase, _label = next_research_action(_s)
    _prefix = f"images/round-{_number}/"
    _proposal = teaching.saved(_s, _prefix + "propose")
    _composition = teaching.saved(_s, _prefix + "compose")
    _candidate = None
    if _phase in ("review-0", "probe-result-0") and _proposal:
        _candidate = _proposal["result"]["candidates"][0]
    elif _phase in ("review-1", "probe-result-1") and _proposal:
        _candidate = _proposal["result"]["candidates"][1]
    elif _phase in ("review-composition", "composition-result") and _composition:
        _candidate = _composition["result"]["decision"]
    _prior = teaching.saved(_s, "images/round-1/adopt")
    _parent = get_lab().get("manual") if _number == 1 else _prior["result"]["adopted"] if _prior else None
    research_note = mo.ui.text_area(value=_s.get_draft("solar/review-" + _prefix + _phase, ""), label="My observation or review note", full_width=True, on_change=lambda value: _s.save_draft("solar/review-" + _prefix + _phase, value))
    _evidence_check = get_feedback().get("evidence-check", {})
    _evidence_ready = _evidence_check.get("status") == "complete" and _evidence_check.get("source_fingerprint") == digest(evidence_editor.value)
    research_button = mo.ui.run_button(label=f"Round {_number}: {_label}", disabled=not bool(_parent and get_lab().get("images")) or _phase == "done" or (_phase == "propose" and not _evidence_ready))
    _explain = {"propose": "Ask the research agent for two code changes. It will use your selected model and validation results.", "review-0": "Read Candidate A’s diff. In your note, name the changed line and what you expect it to do.", "probe-result-0": "Run Candidate A with the same training settings as its starting model. Read its validation error or failure below.", "review-1": "Read Candidate B’s diff and write what it tries to change. B is a separate suggestion from the same starting model.", "probe-result-1": "Run Candidate B on the same data as A. Then you can compare the two suggestions.", "probe-done": "Compare A and B below. Write which result you would keep and point to a score, prediction, or failure.", "compose": "Ask the agent to choose, combine, or reject the two suggestions. You’ll review the resulting code next.", "review-composition": "Read the proposed final diff and write what changed. If it retains the previous version, say why that seems reasonable.", "composition-result": "Run the proposed final version on validation data. Even a combination of good edits needs its own test.", "adopt": "Save the tested version and lesson. The notebook keeps the earlier model if the new one fails or does not lower validation error.", "done": "Both rounds are saved. Continue to Final evaluation to test the selected versions on the reserved dates."}[_phase]
    _parts = [mo.Html(ui.result("Evidence-selection check", _evidence_check, status=_evidence_check.get("status", "not checked"))), mo.Html(ui.step(f"Round {_number} · {_label}", _explain, "Read the result below before moving to the next action."))]
    if _phase == "propose" and not _evidence_ready:
        _parts.append(mo.callout(mo.md("Finish select_validation_evidence above and click Check my evidence selection. Then you can request the first two suggestions."), kind="warn"))
    if _candidate:
        _parts += [mo.Html(ui.result(_candidate.get("title", "Proposed change"), {"Decision": "Retain this version" if _candidate["decision"] == "KEEP" else "Change source", "Agent rationale": _candidate["rationale"]}, detail={"Source fingerprint": _candidate.get("fingerprint")})), mo.Html(ui.diff(_parent["source"], _candidate["source"]))]
    _probe_rows = [teaching.saved(_s, _prefix + "probe-result-" + str(index)) for index in (0, 1)]
    if any(_probe_rows):
        _parts.append(mo.ui.table([{"Candidate": "AB"[index], "Status": "failed" if row["result"].get("errors") else "complete", "Validation error": row["result"].get("metrics", {}).get("validation_error"), "Error": "; ".join(row["result"].get("errors", []))} for index, row in enumerate(_probe_rows) if row], selection=None))
    _parts += [research_note, research_button]
    solar_prerequisite_15 = ui.prerequisite(mo, "Compare the two manual image models first.", "images", go_to)
    solar_prerequisite_16 = ui.prerequisite(mo, "Go to Solar data and click Load the solar dataset to put the images back in memory.", "data", go_to)
    if not _parent:
        _parts.append(solar_prerequisite_15)
    elif not get_lab().get("images"):
        _parts.append(solar_prerequisite_16)
    solar_next_step_17 = ui.next_step(mo, "Next: freeze and evaluate", "final", go_to)
    _parts += [ui.evidence(mo, _s, stage_ids=[row["id"] for row in (_proposal, _composition) if row], question="Open the proposal in Agent Lens. Find the validation score and code sent to the agent, then compare its explanation with the changed lines below. What does the edit try to fix?"), ui.branch_workbench(mo, _s, key="solar-research"), solar_next_step_17]
    mo.vstack(_parts)
    return (research_button, research_note, solar_next_step_17, solar_prerequisite_15, solar_prerequisite_16,)


# workshop-cell: solar_autoresearch/action/research_button
@app.cell
def _(choose_adoption, evidence_editor, get_lab, mo, next_research_action, refresh_saved, research, research_button, research_note, run_training, set_feedback, teaching):
    mo.stop(not research_button.value)
    _s = get_lab()["session"]
    _number, _phase, _label = next_research_action(_s)
    _prefix = f"images/round-{_number}/"
    _prior = teaching.saved(_s, "images/round-1/adopt") if _number == 2 else None
    _parent = get_lab()["manual"] if _number == 1 else {**_prior["result"]["adopted"], "lessons": [{"lesson": _prior["result"].get("lesson"), "limits": _prior["result"].get("limits")}]}
    _metric_source = _s.get_draft("solar/image-metric", teaching.IMAGE_METRIC_SOLUTION)
    teaching.check_image_metric(_metric_source)
    if _phase == "propose":
        teaching.check_evidence(evidence_editor.value)
        _evidence = teaching.functions(evidence_editor.value)["select_validation_evidence"](_parent)
        _proposal, _id = research.propose(_s, _number, _parent["source"], _evidence)
        try:
            research.trace_decision(_s, _id)
        except Exception as _error:
            set_feedback(lambda current: {**current, "research-export": str(_error)})
    elif _phase.startswith("review-"):
        mo.stop(not research_note.value.strip(), mo.md("In the review note, name the line that changed and what you expect it to do."))
        _candidate = teaching.saved(_s, _prefix + "compose")["result"]["decision"] if _phase == "review-composition" else teaching.saved(_s, _prefix + "propose")["result"]["candidates"][int(_phase[-1])]
        with _s.stage(_prefix + _phase, sources={"candidate.py": _candidate["source"]}, inputs={"fingerprint": _candidate["fingerprint"]}) as _stage:
            if _stage.needs_run:
                _stage.record({"reviewed_fingerprint": _candidate["fingerprint"], "note": research_note.value})
    elif _phase.startswith("probe-result-") or _phase == "composition-result":
        _is_composition = _phase == "composition-result"
        _index = None if _is_composition else int(_phase[-1])
        _candidate = teaching.saved(_s, _prefix + "compose")["result"]["decision"] if _is_composition else teaching.saved(_s, _prefix + "propose")["result"]["candidates"][_index]
        _review = teaching.saved(_s, _prefix + ("review-composition" if _is_composition else "review-" + str(_index)))
        assert _review["result"]["reviewed_fingerprint"] == _candidate["fingerprint"], "The reviewed source must match the code being executed."
        _name = _prefix + ("composition-test" if _is_composition else "probe-" + str(_index))
        try:
            _executed = run_training(_s, _name, _candidate["source"], get_lab()["images"], _parent["config"], get_lab()["dataset"], _metric_source)
        except Exception as _error:
            _failed = [row for row in _s.read()["stages"].values() if row["name"] == _name]
            _executed = {"stage_id": _failed[-1]["id"] if _failed else None, "source": _candidate["source"], "config": _parent["config"], "split": "validation", "errors": [str(_error)], "metrics": {}}
        with _s.stage(_prefix + _phase, inputs={"candidate_fingerprint": _candidate["fingerprint"]}) as _stage:
            if _stage.needs_run:
                _stage.record({**_executed, "title": _candidate["title"], "rationale": _candidate["rationale"]})
    elif _phase == "probe-done":
        mo.stop(not research_note.value.strip(), mo.md("In the review note, compare A and B using their validation errors or recorded failures."))
        _probes = [teaching.saved(_s, _prefix + "probe-result-" + str(index))["result"] for index in (0, 1)]
        with _s.stage(_prefix + "probe-done", inputs={"probes": _probes}) as _stage:
            if _stage.needs_run:
                _stage.record({"probes": _probes, "participant_comparison": research_note.value})
    elif _phase == "compose":
        _probes = teaching.saved(_s, _prefix + "probe-done")["result"]["probes"]
        _decision, _id = research.compose(_s, _number, _parent["source"], _parent, _probes)
        try:
            research.trace_decision(_s, _id)
        except Exception as _error:
            set_feedback(lambda current: {**current, "research-export": str(_error)})
    elif _phase == "adopt":
        _decision = research.normalize_composition(teaching.saved(_s, _prefix + "compose")["result"]["decision"])
        _executed = teaching.saved(_s, _prefix + "composition-result")["result"]
        _adopted = choose_adoption(_parent, _executed)
        with _s.stage(_prefix + "adopt", inputs={"tested": _executed["stage_id"]}) as _stage:
            if _stage.needs_run:
                _stage.record({"adopted": _adopted, "decision": _decision, "retained_parent": _adopted is _parent, "lesson": _decision.get("lesson"), "limits": _decision.get("limits"), "participant_note": research_note.value, "execution_error": _executed.get("errors")})
    _s.checkpoint("research" if next_research_action(_s)[1] == "done" else _prefix + _phase)
    refresh_saved()
    return


# workshop-cell: solar_autoresearch/controls/final_button
@app.cell(hide_code=True)
def _(get_lab, get_step, go_to, mo, next_research_action, ui):
    mo.stop(get_step() != "final")
    _s = get_lab().get("session")
    _done = bool(_s) and next_research_action(_s)[1] == "done"
    final_button = mo.ui.run_button(label="Freeze versions and evaluate reserved dates", disabled=not (_done and get_lab().get("images") and get_lab().get("goes")))
    conclusion = mo.ui.text_area(value=_s.get_draft("solar/conclusion", "") if _s else "", label="What changed in your forecast? Link one prediction and the code change behind it.", full_width=True, on_change=lambda value: _s.save_draft("solar/conclusion", value) if _s else None)
    report_button = mo.ui.run_button(label="Publish my conclusion", disabled=not bool(get_lab().get("final")))
    retry_publication = mo.ui.run_button(label="Retry saved exports and comparison publication", disabled=not bool(_s))
    solar_prerequisite_18 = ui.prerequisite(mo, "Finish both research rounds before freezing versions.", "research", go_to)
    solar_prerequisite_19 = ui.prerequisite(mo, "Go to Solar data and click Load the solar dataset before evaluating.", "data", go_to)
    mo.vstack([mo.Html(ui.step("7. Evaluate the selected models on reserved dates", "Click Freeze versions and evaluate reserved dates. We’ll use the saved weights to compare persistence, your manual image model, and the agent-edited model on February 13–14. We’ll also score your selected GOES model separately.", "Pick one forecast and explain what changed. Then write your conclusion below and click Publish my conclusion.")), final_button, solar_prerequisite_18 if not _done else solar_prerequisite_19 if not get_lab().get("images") else mo.md("These two test days were held back while you chose changes. One seed and overlapping forecast windows make this a teaching result, not evidence of reliable solar forecasting."), mo.accordion({"A trace or comparison did not upload": mo.vstack([mo.md("Your executions and predictions are saved locally. Use the retry button to upload them again without training or calling the research agent. If native EvalTables is unavailable, use the notebook comparison and the published Weave links. Unavailable results stay marked unavailable."), retry_publication])})])
    return (conclusion, final_button, report_button, retry_publication, solar_prerequisite_18, solar_prerequisite_19,)


# workshop-cell: solar_autoresearch/action/final_button
@app.cell
def _(event, export_trace, final_button, get_lab, instrument_tool, mo, np, plots, publish_comparison, refresh_saved, research, set_feedback, solar, teaching, training):
    mo.stop(not final_button.value)
    mo.output.replace(mo.md("**Evaluating your selected models.** Loading the saved weights and predicting the reserved dates."))
    _s = get_lab()["session"]
    _adopted = teaching.saved(_s, "images/round-2/adopt")["result"]["adopted"]
    _versions = {"manual": get_lab()["manual"], "agent": _adopted}
    _freeze, _freeze_id = research.freeze(_s, _versions, get_lab()["dataset"])
    _test = get_lab()["images"]["test"]
    _predictions = {"persistence": _test["persistence"]}
    _comparison_evidence = {"persistence": {}}
    _results = {"persistence": solar.score(_test["persistence"], _test)}
    for _label, _version in _versions.items():
        _weights = _s.file("outputs/" + _version["stage_id"] + "/weights.pt")
        with _s.stage("images/final-" + _label, config=_version["config"], sources={"candidate.py": _version["source"]}, inputs={"freeze": _freeze_id, "split": "test"}) as _stage:
            if _stage.needs_run:
                (_result, _prediction), _event = event("evaluate_frozen_weights",
                    {"freeze": _freeze_id, "source_fingerprint": _stage.source_fingerprint, "trained_stage": _version["stage_id"], "split": "test"},
                    lambda: training.train(_version["source"], None, _test, _version["config"], _stage.output_dir, weights=_weights),
                    on_error=_stage.record_event)
                _event.update(id=_stage.id + "/evaluate", result=_result["metrics"])
                _result["events"] = [_event]
                _figure = plots.forecast(_prediction, _test, title="Frozen " + _label + " on reserved dates")
                _figure.savefig(_stage.output_dir / "predictions.png", dpi=130)
                _stage.record(_result, files=[_stage.output_dir / "predictions.npy", _stage.output_dir / "predictions.png"])
            _prediction = np.load(_stage.output_dir / "predictions.npy")
            try:
                _trace = export_trace(_s, _stage.id, "Evaluate frozen " + _label + " weights on reserved image dates", _stage.result.get("events", []), tool_writer=instrument_tool) if _stage.result.get("events") else {}
            except Exception as _error:
                _trace = {"status": "unavailable", "error": str(_error)}
            _results[_label] = _stage.result["metrics"]
            _predictions[_label] = _prediction
            _comparison_evidence[_label] = {"stage": _stage.id, "source": _stage.source_fingerprint, "trace": _trace, "training_trace": _version.get("trace", {})}
    with _s.stage("images/final-comparison", inputs={"freeze": _freeze_id}) as _stage:
        if _stage.needs_run:
            _scales = solar.image_display_scales(_predictions, _test)
            _comparisons = {label: solar.evaluation_rows(prediction, _test, evidence=_comparison_evidence[label],
                media_dir=_stage.output_dir / "media", media_root=_s.root, image_scales=_scales)
                for label, prediction in _predictions.items()}
            np.savez_compressed(_stage.output_dir / "comparison-inputs.npz", **_test)
            _stage.record({"metrics_by_version": _results, "rows": _comparisons},
                          files=[_stage.output_dir / "comparison-inputs.npz", *sorted((_stage.output_dir / "media").glob("*.png"))])
    # Measurement selection and scoring remain separate from image prediction.
    _goes_runs = [row for row in _s.completed() if (row["name"].startswith("goes/search-") or row["name"] == "goes/worked-repair") and row["inputs"].get("dataset") == get_lab()["dataset"]]
    if _goes_runs:
        _best = min(_goes_runs, key=lambda row: row["result"]["metrics"]["validation_error"])
        _test = get_lab()["goes"]["test"]
        with _s.stage("goes/final", config=_best["config"], sources=_best["sources"], inputs={"selected_stage": _best["id"], "split": "test"}) as _g:
            if _g.needs_run:
                (_result, _prediction), _event = event("evaluate_frozen_weights",
                    {"trained_stage": _best["id"], "source_fingerprint": _g.source_fingerprint, "split": "test"},
                    lambda: training.train(_best["sources"]["candidate.py"], None, _test, _best["config"], _g.output_dir, weights=_s.file("outputs/" + _best["id"] + "/weights.pt")),
                    on_error=_g.record_event)
                _event.update(id=_g.id + "/evaluate", result=_result["metrics"])
                _result["events"] = [_event]
                _g.record(_result, files=[_g.output_dir / "predictions.npy"])
            _prediction = np.load(_g.output_dir / "predictions.npy")
            try:
                _goes_trace = export_trace(_s, _g.id, "Evaluate the frozen measurement model on reserved dates", _g.result.get("events", []), tool_writer=instrument_tool) if _g.result.get("events") else {}
            except Exception as _error:
                _goes_trace = {"status": "unavailable", "error": str(_error)}
        with _s.stage("goes/final-comparison", inputs={"selected_stage": _best["id"]}) as _comparison:
            if _comparison.needs_run:
                _comparison.record({"rows": {"persistence": solar.evaluation_rows(_test["persistence"], _test), "selected-model": solar.evaluation_rows(_prediction, _test, evidence={"stage": _g.id, "trace": _goes_trace})}, "metrics_by_version": {"persistence": solar.score(_test["persistence"], _test), "selected-model": _g.result["metrics"]}})
    _s.checkpoint("final")
    refresh_saved()
    # Publication uses saved predictions. Failure does not erase the completed evaluation.
    mo.output.replace(mo.md("**Your predictions and scores are saved.** Uploading the comparisons to Weave and EvalTables. This can take a few minutes."))
    for _name, _label in (("images/final-comparison", "solar-images-final"), ("goes/final-comparison", "solar-measurements-final")):
        _saved = teaching.saved(_s, _name)
        if _saved:
            try:
                with mo.status.spinner(title="Publishing " + _label + " from saved predictions"):
                    publish_comparison(_s, _label, _saved["result"]["rows"])
            except Exception as _error:
                set_feedback(lambda current: {**current, "publication": str(_error)})
    refresh_saved()
    mo.output.replace(mo.md("**Your comparison is ready below.** Open the published links, or use the notebook table if a service is unavailable."))
    return


# workshop-cell: solar_autoresearch/action/report_button
@app.cell(hide_code=True)
def _(conclusion, get_lab, mo, publish_report, refresh_saved, report_button, ui):
    mo.stop(not report_button.value)
    _s = get_lab()["session"]
    _links = {**_s.read()["progress"].get("evidence", {}), **ui.stage_links(_s, [row["id"] for row in _s.completed() if row["name"].startswith(("images/final-", "goes/final", "images/round-"))])}
    for _key, _receipt in _s.read()["publications"].items():
        if _key.startswith("comparison/"):
            _links.update(ui.comparison_links(_receipt, suffix=_key.rsplit("/", 1)[-1][:6]))
    _url = publish_report(_s, conclusion.value, _links)
    _s.checkpoint("report", evidence={"Report": _url})
    refresh_saved()
    return


# workshop-cell: solar_autoresearch/action/retry_publication
@app.cell(hide_code=True)
def _(export_trace, get_lab, instrument_tool, mo, publish_comparison, refresh_saved, retry_publication, saved_trace_inputs, set_feedback, teaching):
    mo.stop(not retry_publication.value)
    _s = get_lab()["session"]
    _status = _s.retry_publication()
    for _row in _s.read()["stages"].values():
        try:
            _trace_inputs = saved_trace_inputs(_s, _row)
            if _trace_inputs["events"] or _trace_inputs["requests"]:
                export_trace(_s, **_trace_inputs, tool_writer=instrument_tool)
        except Exception as _error:
            _status[_row["name"]] = str(_error)
    for _name, _label in (("images/final-comparison", "solar-images-final"), ("goes/final-comparison", "solar-measurements-final")):
        _saved = teaching.saved(_s, _name)
        if _saved:
            try:
                _status[_label] = publish_comparison(_s, _label, _saved["result"]["rows"])
            except Exception as _error:
                _status[_label] = str(_error)
    set_feedback(lambda current: {**current, "publication_retry": _status})
    refresh_saved()
    return


# workshop-cell: solar_autoresearch/display/80
@app.cell(hide_code=True)
def _(get_lab, get_step, mo, teaching, ui):
    mo.stop(get_step() != "final")
    _s = get_lab().get("session")
    mo.stop(not _s, mo.md("Connect first."))
    _image = teaching.saved(_s, "images/final-comparison")
    _measurement = teaching.saved(_s, "goes/final-comparison")
    _parts = [mo.md("### Final image errors")]
    if _image:
        _parts.append(mo.ui.table(teaching.metric_rows(_image["result"]["metrics_by_version"]), selection=None))
    else:
        _parts.append(mo.md("Run the frozen comparison above to see your final image scores."))
    _parts.append(mo.md("### Final measurement errors"))
    if _measurement:
        _parts.append(mo.ui.table(teaching.metric_rows(_measurement["result"]["metrics_by_version"]), selection=None))
    elif get_lab().get("goes_final"):
        _parts.append(mo.Html(ui.result("Restored measurement evaluation", get_lab()["goes_final"])))
    else:
        _parts.append(mo.md("Your final GOES scores will appear here. We keep them separate because measurement and image errors use different units."))
    _parts += [ui.evidence(mo, _s, stage_ids=[row["id"] for row in _s.completed() if row["name"] in ("images/final-manual", "images/final-agent", "images/final-comparison", "goes/final", "goes/final-comparison")], extra=_s.read()["progress"].get("evidence", {}), question="Choose the same forecast timestamp in each version. Compare its predicted image and error, then follow the code and trace links. Which visible difference supports your conclusion?"), ui.publication(mo, _s)]
    mo.vstack(_parts)
    return


# workshop-cell: solar_autoresearch/display/81
@app.cell(hide_code=True)
def _(get_lab, get_step, mo, np, teaching, ui, views):
    mo.stop(get_step() != "final")
    _s = get_lab().get("session")
    _comparison = teaching.saved(_s, "goes/final-comparison") if _s else None
    mo.stop(not _comparison or not get_lab().get("goes"))
    _row = views.comparison_execution(_s, _comparison, "selected-model")
    mo.stop(not _row, mo.md("The GOES execution referenced by the saved final comparison is unavailable locally. Restore its Artifact; a newer attempt will not be substituted."))
    _path = _s.file("outputs/" + _row["id"] + "/predictions.npy")
    mo.stop(not _path.exists(), mo.md("Restore the final GOES prediction Artifact to inspect this saved result."))
    _selected_training_id = _row.get("inputs", {}).get("selected_stage")
    _training = next((row for row in _s.completed() if row["id"] == _selected_training_id), None)
    mo.vstack([mo.md("### Does the selected measurement model beat persistence?"), mo.md("These are predictions from saved weights on the reserved dates. The loss curve belongs to its earlier training run. A falling training loss alone does not establish better forecasting."), mo.Html(ui.result("Selected settings", _row["config"])), mo.md("The exact selected training record is unavailable locally. Restore its Artifact to inspect the loss curve; no other run is substituted.") if not _training else mo.md(""), views.goes_investigation(np.load(_path, allow_pickle=False), get_lab()["goes"]["test"], losses=_training["result"].get("losses", []) if _training else [], title="Frozen GOES model"), ui.evidence(mo, _s, stage_ids=[_row["id"]] + ([_training["id"]] if _training else []), question="Compare the saved training and final-evaluation calls. Which one updates weights? Which one loads weights.pt and only predicts?")])
    return


# workshop-cell: solar_autoresearch/aria/conclusion
@app.cell(hide_code=True)
def _(aria, conclusion, get_lab, get_step, mo):
    mo.stop(get_step() != "final")
    _s=get_lab().get("session")
    solar_aria_conclusion=aria.investigation(mo,_s,"conclusion",interpretation=conclusion.value,workshop="solar-autoresearch")
    mo.vstack([mo.md("### Write your interpretation before asking ARIA"),conclusion,solar_aria_conclusion])
    return (solar_aria_conclusion,)


# workshop-cell: solar_autoresearch/aria_response/conclusion
@app.cell(hide_code=True)
def _(aria, mo, report_button, solar_aria_conclusion):
    mo.vstack([aria.response(mo,solar_aria_conclusion),report_button])
    return

if __name__ == "__main__":
    app.run()
