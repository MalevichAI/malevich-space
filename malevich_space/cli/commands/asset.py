import json
import logging

from typing import Optional

import typer
import pandas as pd

import malevich_space.schema as schema

from malevich_space.constants import SETUP_HELP

from malevich_space.ops.roller import local_roller


app = typer.Typer()


@app.command()
def upload(local_path: str, core_path: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP)):
    roller = local_roller(setup, None)
    asset_id, upload_url = roller.space.create_asset(core_path=core_path)
    logging.info(f"{core_path} will be linked to asset in space - {asset_id}")


@app.command()
def get(uid: str, setup: Optional[str] = typer.Option(None, help=SETUP_HELP)):
    roller = local_roller(setup, None)
    asset, download_url, upload_url = roller.space.get_asset(uid=uid)
    logging.info(f"Asset ({uid}) - {asset['corePath']} exists")
    logging.info(f"Download: {download_url}")
    logging.info(f"Upload: {upload_url}")
