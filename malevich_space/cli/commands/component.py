import json
import logging

from typing import Optional

import typer

import malevich_space.schema as schema

from malevich_space.ops import RollerOps
from malevich_space.ops import env as env

from malevich_space.parser import YAMLParser
from malevich_space.constants import ACTIVE_SETUP_PATH


SETUP_HELP = "Path to space .yaml configuration"


app = typer.Typer()


def _local_roller(setup: str | None, comp_dir: str | str = None) -> RollerOps:
    if setup:
        config = schema.Setup(**YAMLParser.parse_yaml(setup))
    else:
        config = env.get_active(ACTIVE_SETUP_PATH)
    return RollerOps(config, path=comp_dir)


@app.command()
def add(
    comp_dir: str,
    component: str,
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = _local_roller(setup, comp_dir)
    comp = roller.comp_provider.get_by_reverse_id(component)
    _ = roller.component(comp, version_mode=schema.VersionMode.MINOR)


@app.command()
def build(component: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP)):
    roller = _local_roller(setup, None)
    loaded = roller.space.get_parsed_component_by_reverse_id(reverse_id=component)
    roller.build(loaded)


@app.command()
def boot(
    task_id: str,
    exec_mode: str = "batch",
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = _local_roller(setup, None)
    loaded_task = schema.LoadedTaskSchema(uid=task_id)
    roller.boot(core_task=loaded_task, exec_mode=exec_mode)


@app.command()
def run(
    task_id: str,
    payload_path: Optional[str] = None,
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = _local_roller(setup, None)
    payload = None
    if payload_path:
        with open(payload_path) as f:
            payload = json.load(f)
    task = schema.LoadedTaskSchema(uid=task_id)
    roller.run_task(task=task, raw=payload)


@app.command()
def stop(task_id: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP)):
    roller = _local_roller(setup, None)
    loaded_task = schema.LoadedTaskSchema(uid=task_id)
    roller.change_task_state(task=loaded_task, target_state="stop")


@app.command()
def test(
    comp_dir: str,
    component: str,
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = _local_roller(setup, comp_dir)
    comp = roller.comp_provider.get_by_reverse_id(component)
    loaded = roller.component(comp, version_mode=schema.VersionMode.MINOR)
    tasks = roller.build(loaded)
    for task in tasks:
        loaded_task = schema.LoadedTaskSchema(uid=task)
        roller.boot(core_task=loaded_task, exec_mode="batch")
        try:
            roller.run_task(task=loaded_task, raw=None)
        except Exception as e:
            logging.exception(e)
        roller.change_task_state(task=loaded_task, target_state="stop")
