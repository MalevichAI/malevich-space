import logging

import typer

from space.ops import env as env
from space.constants import ACTIVE_SETUP_PATH


app = typer.Typer()


@app.command()
def set(setup_path: str):
    env.set_active(setup_path, ACTIVE_SETUP_PATH)


@app.command()
def get():
    active = env.get_active(ACTIVE_SETUP_PATH)
    logging.info(f">> Active host: {active.space}")
