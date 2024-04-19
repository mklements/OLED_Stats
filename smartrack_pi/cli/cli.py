"""This module provides the Smartrack CLI."""

# smartrack/cli/cli.py

from typing import Optional

import typer

from smartrack_pi import __app_name__, __version__
from smartrack_pi.cli import companion, display, net
from smartrack_pi.settings import software
app = typer.Typer()
app.add_typer(display.app, name="display")
app.add_typer(net.app, name="net")
app.add_typer(companion.app, name="companion")

@app.command()
def update():
    confirm = typer.confirm("This will update all software to current version, with no changes to companion file. OK?")
    if not confirm:
        print("Aborting...")
        raise typer.Abort()
    print("Updating Software")
    software.update()

@app.command()
def factory():
    confirm = typer.confirm("This will factory reset device you will lose all companion settings, OK?")
    if not confirm:
        print("Aborting...")
        raise typer.Abort()
    print("Factory Resetting Device")
    software.factory_reset()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
