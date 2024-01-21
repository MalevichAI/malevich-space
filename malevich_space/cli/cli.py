import logging

import typer

from .commands import env, component, ci, schema, team, asset


logging.basicConfig(level=logging.INFO)


app = typer.Typer()
app.add_typer(env, name="env")
app.add_typer(component, name="component")
app.add_typer(ci, name="ci")
app.add_typer(schema, name="schema")
app.add_typer(team, name="team")
app.add_typer(asset, name="asset")


def main():
    app()


if __name__ == '__main__':
    main()
