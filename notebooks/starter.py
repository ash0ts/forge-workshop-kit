# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.2.3/forge_workshop_kit-0.2.3-py3-none-any.whl", "torch==2.15.0"]
# [tool.uv.sources]
# torch = [{ index = "pytorch-cpu", marker = "sys_platform != 'darwin'" }]
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title='My Forge workshop')


@app.cell(hide_code=True)
def _():
    import os
    import time
    import marimo as mo
    from forge_workshop_kit import WorkshopSession
    from coreweave.forge.agentlens import tracing
    return (WorkshopSession, mo, os, time, tracing,)


@app.cell(hide_code=True)
def _(mo, os):
    mo.md("# My workshop\nCopy this notebook to your project, then replace the square calculation below with your own exercise. The tracing scopes show how to send its arguments and result to Agent Lens.")
    project=mo.ui.text(value=os.getenv("WORKSHOP_PROJECT") or "/".join(filter(None,[os.getenv("WANDB_ENTITY"),os.getenv("WANDB_PROJECT")])),label="entity/project")
    connect=mo.ui.run_button(label="Check project access")
    mo.vstack([project,connect])
    return (connect, project,)


@app.cell
def _(WorkshopSession, connect, mo, project):
    mo.stop(not connect.value)
    session=WorkshopSession.from_environment("starter",project=project.value)
    session.check_access()
    session.restore()
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
