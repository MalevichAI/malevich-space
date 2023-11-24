import logging

from typing import Optional

import typer

from malevich_space.ops import env as env
from malevich_space.ops.roller import local_roller
from malevich_space.constants import ACTIVE_SETUP_PATH, SETUP_HELP


app = typer.Typer()


@app.command()
def create(
    member: list[str] = typer.Argument(help="List of emails to invite to the team"),
    name: str = typer.Option(help="Team name"),
    reverse_id: Optional[str] = typer.Option(None, help="Team reverse ID"),
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP)
):
    roller = local_roller(setup, None)
    org, status = roller.create_org(name=name, reverse_id=reverse_id, members=member)
    if not org:
        typer.echo(f"Failed to create {name}")
    if status:
        invite_str = "\n - ".join(status)
        typer.echo(f"Created org {name} | {org}\n\nInvited:\n - {invite_str}")


@app.command()
def invite(
    member: list[str] = typer.Argument(help="List of emails to invite to the team"),
    name: str = typer.Option(help="Team name"),
    setup: Optional[str] = typer.Option(None, help=SETUP_HELP)
):
    roller = local_roller(setup, None)
    status = roller.invite_to_org(name=name, members=member)
    invite_str = "\n - ".join(status)
    typer.echo(f"- {invite_str}")
