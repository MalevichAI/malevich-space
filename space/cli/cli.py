import logging

import typer

from .commands import env, component, ci


logging.basicConfig(level=logging.INFO)


app = typer.Typer()
app.add_typer(env, name="env")
app.add_typer(component, name="component")
app.add_typer(ci, name="ci")


def main():
    app()
