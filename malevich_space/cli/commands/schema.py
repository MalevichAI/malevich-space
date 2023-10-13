import logging

from typing import Optional

import typer

from malevich_space.ops import local_roller
from malevich_space.constants import SETUP_HELP


app = typer.Typer()


@app.command()
def add(name: str, path: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP),):
    roller = local_roller(setup)
    schema_id = roller.create_scheme(name, path)
    logging.info(f">> Schema '{name}' created ({schema_id})")
