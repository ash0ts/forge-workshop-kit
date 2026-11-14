# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#   "forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.5.0/forge_workshop_kit-0.5.0-py3-none-any.whl",
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
#   "pillow==12.3.0",
#   "platformdirs==4.14.5",
#   "polyfile-weave==0.5.9",
#   "propcache==0.5.4",
#   "protobuf==6.33.6",
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
app = marimo.App(width="medium", app_title='My Forge workshop')


@app.cell(hide_code=True)
def _():
    import os
    import time
    import marimo as mo
    from forge_workshop_kit import WorkshopSession, setup, ui
    from coreweave.forge.agentlens import tracing
    return (WorkshopSession, mo, os, setup, time, tracing, ui,)


@app.cell(hide_code=True)
def _(mo, setup, ui):
    mo.md("# My workshop\nCopy this notebook to your project, then replace the square calculation below with your own exercise. The tracing scopes show how to send its arguments and result to Agent Lens.")
    _context=setup.project_context()
    project=mo.ui.text(value=_context["project"],label="entity/project",disabled=_context["hosted"] and _context["detected"])
    connect=mo.ui.run_button(label="Check project access")
    mo.vstack([mo.Html(ui.result("Copied notebook project", {"Project": _context["project"]})) if _context["hosted"] and _context["detected"] else project,connect])
    return (connect, project,)


@app.cell
def _(WorkshopSession, connect, mo, project, setup):
    mo.stop(not connect.value)
    session=WorkshopSession.from_environment("starter",project=project.value)
    _access=session.check_access()
    session.restore()
    setup.save_access(session,_access)
    mo.ui.table(setup.capabilities(session), selection=None, pagination=False)
    return (session,)


@app.cell(hide_code=True)
def _(mo):
    run_exercise=mo.ui.run_button(label="Run my instrumented exercise")
    run_exercise
    return (run_exercise,)


@app.cell
def _(mo, run_exercise, session, tracing):
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
    return (result, sdk, span, stage,)

if __name__ == "__main__":
    app.run()
