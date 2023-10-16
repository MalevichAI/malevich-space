import json
import logging

from typing import Optional

import typer

import malevich_space.schema as schema

from malevich_space.constants import SETUP_HELP

from malevich_space.ops.roller import local_roller


app = typer.Typer()


@app.command()
def add(
    comp_dir: str,
    component: str,
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = local_roller(setup, comp_dir)
    comp = roller.comp_provider.get_by_reverse_id(component)
    _ = roller.component(comp, version_mode=schema.VersionMode.MINOR)


@app.command()
def build(component: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP)):
    roller = local_roller(setup, None)
    loaded = roller.space.get_parsed_component_by_reverse_id(reverse_id=component)
    roller.build(loaded)


@app.command()
def ops(component: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP)):
    roller = local_roller(setup, None)
    loaded = roller.space.get_parsed_component_by_reverse_id(reverse_id=component)
    typer.echo(loaded.app.ops)


@app.command()
def boot(
    task_id: str,
    exec_mode: str = "batch",
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = local_roller(setup, None)
    loaded_task = schema.LoadedTaskSchema(uid=task_id)
    roller.boot(core_task=loaded_task, exec_mode=exec_mode)


@app.command()
def run(
    task_id: str,
    payload_path: Optional[str] = None,
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = local_roller(setup, None)
    payload = None
    if payload_path:
        with open(payload_path) as f:
            payload = json.load(f)
    task = schema.LoadedTaskSchema(uid=task_id)
    roller.run_task(task=task, raw=payload)


@app.command()
def stop(task_id: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP)):
    roller = local_roller(setup, None)
    loaded_task = schema.LoadedTaskSchema(uid=task_id)
    roller.change_task_state(task=loaded_task, target_state="stop")


@app.command()
def test(
    comp_dir: str,
    component: str,
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = local_roller(setup, comp_dir)
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


@app.command()
def endpoint(
        task_id: str,
        alias: Optional[str] = typer.Argument(None, help="Endpoint alias"),
        token: Optional[str] = typer.Option(None, help="Name of token to use"),
        setup: Optional[str] = typer.Option(None, help=SETUP_HELP),
):
    roller = local_roller(setup, None)
    created = roller.space.create_endpoint(task_id=task_id, alias=alias, token=token)
    logging.info(f">> Endpoint created - {roller.config.space.api_gateway_url()}/{alias if alias else created}")


@app.command()
def wipe(reverse_id: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP)):
    try:
        roller = local_roller(setup, None)
        roller.space.wipe_component(reverse_id=reverse_id)
        logging.info(f">> {reverse_id} successfully wiped")
    except Exception as e:
        logging.exception(f"Failed to wipe {reverse_id} ({e})")
