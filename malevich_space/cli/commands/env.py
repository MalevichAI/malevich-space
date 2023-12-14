import logging

import typer

from malevich_space.ops import env as env_op
from malevich_space.constants import ACTIVE_SETUP_PATH
from malevich_space.ops import SpaceOps


app = typer.Typer()


@app.command()
def set(setup_path: str):
    env_op.set_active(setup_path, ACTIVE_SETUP_PATH)


@app.command()
def get():
    active = env_op.get_active(ACTIVE_SETUP_PATH)
    logging.info(f">> Active host: {active.space}")


@app.command()
def add_secret(key: str, value: str, env: str = "default"):
    active = env_op.get_active(ACTIVE_SETUP_PATH)
    ops = SpaceOps(space_setup=active.space)
    result = ops.add_secret(key=key, value=value, org_id=active.space.org, env_name=env)
    logging.info(f"Added secret to {env}: {key} - {result}")


@app.command()
def secret(key: str,  env: str = "default"):
    active = env_op.get_active(ACTIVE_SETUP_PATH)
    ops = SpaceOps(space_setup=active.space)
    value = ops.get_secret(key=key, org_id=active.space.org, env_name=env)
    logging.info(f"Got secret from {env}: {key} - {value}")
