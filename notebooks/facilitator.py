# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["forge-workshop-kit @ https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.2.0/forge_workshop_kit-0.2.0-py3-none-any.whl", "torch==2.15.0"]
# [tool.uv.sources]
# torch = [{ index = "pytorch-cpu", marker = "sys_platform != 'darwin'" }]
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
import marimo
__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title='Workshop progress')


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from forge_workshop_kit.publication import monitor
    return (mo, monitor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("# Workshop progress\nThis notebook only reads participant projects. Missing updates mean unknown, not failure. It never starts participant work.")
    roster=mo.ui.text_area(label="Public project links: entity/project, one per line",full_width=True)
    workshop=mo.ui.dropdown({"Solar Autoresearch · four hours":"solar-autoresearch","Pending, Inc. · three hours":"pending-direct-teaching"},value="Solar Autoresearch · four hours",label="Workshop")
    auto_refresh=mo.ui.checkbox(label="Refresh every 30 seconds while this notebook is open")
    refresh=mo.ui.run_button(label="Refresh progress")
    mo.vstack([roster,workshop,auto_refresh,refresh])
    return (auto_refresh, refresh, roster, workshop,)


@app.cell(hide_code=True)
def _(auto_refresh, mo):
    timer=mo.ui.refresh(default_interval=30) if auto_refresh.value else None
    timer
    return (timer,)


@app.cell
def _(auto_refresh, mo, monitor, refresh, roster, timer, workshop):
    mo.stop(not roster.value.strip())
    mo.stop(not refresh.value and not auto_refresh.value)
    if timer is not None:
        _tick=timer.value
    rows=monitor(roster.value.splitlines(),workshop.value)
    mo.ui.table(rows,selection=None)
    return (rows,)

if __name__ == "__main__":
    app.run()
