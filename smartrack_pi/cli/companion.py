import json
import os
from typing import Annotated

import typer

from smartrack_pi.settings import software

app = typer.Typer()


def _get_config():
    with open(
        "/home/smartrack/smartrack-pi/smartrack_pi/config.json", encoding="utf-8"
    ) as f:
        return json.load(f)


def _set_config(key, value):
    config = _get_config()
    config[key] = value
    with open(
        "/home/smartrack/smartrack-pi/smartrack_pi/config.json", "w", encoding="utf-8"
    ) as f:
        json.dump(config, f)


@app.command()
def backup(
    file_name: Annotated[
        str,
        typer.Argument(
            help="Please enter the file name (Folder Location /home/smartrack/smartrack-pi/companion)"
        ),
    ]
):
    print(f"Backing up file to: /home/smartrack/smartrack-pi/companion/{file_name}")
    software.backup_companion_file(file_name)


@app.command()
def restore(
    file_name: Annotated[
        str,
        typer.Argument(
            help="Please enter the file name (Folder Location /home/smartrack/smartrack-pi/companion)"
        ),
    ]
):
    print(f"Restoring file file: /home/smartrack/smartrack-pi/companion/{file_name}")
    print("Warning: Unit Rebooting!")
    software.restore_companion_file(file_name)


if __name__ == "__main__":
    app()
