"""Workshop names and steps, without importing either lesson's runtime."""

import json
from copy import deepcopy
from functools import cache
from importlib.resources import files


@cache
def _manifest():
    return json.loads(files("forge_workshop_kit").joinpath("workshops.json").read_text())


def list_templates():
    """Return independent copies so callers cannot change shared metadata."""
    return tuple(deepcopy(_manifest()["templates"]))


def list_workshops():
    return tuple(row for row in list_templates() if row["kind"] == "workshop")


def get_workshop(workshop_id):
    for row in list_templates():
        if row["id"] == workshop_id:
            return row
    raise ValueError(f"Unknown workshop: {workshop_id}")


def template(slug):
    for row in list_templates():
        if row["slug"] == slug:
            return row
    raise ValueError(f"Unknown notebook template: {slug}")
