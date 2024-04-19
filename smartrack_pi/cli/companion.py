import json
import os
from typing import Annotated

import typer

from smartrack_pi.settings import software

app = typer.Typer()


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
    print(f"Restoring file: /home/smartrack/smartrack-pi/companion/{file_name}")
    print("Warning: Unit Rebooting!")
    software.restore_companion_file(file_name)

@app.command()
def delete(
    file_name: Annotated[
        str,
        typer.Argument(
            help="Please enter the file name (Folder Location /home/smartrack/smartrack-pi/companion)"
        ),
    ]
):
    print(f"Deleting file: /home/smartrack/smartrack-pi/companion/{file_name}")
    software.delete_companion_file(file_name)

@app.command()
def pushconfig(
    file_name: Annotated[
        str,
        typer.Argument(
            help="Please enter the file name (Folder Location /home/smartrack/smartrack-pi/companion)"
        ),
    ]
):
    print(f"Pushing user file to system file: /home/smartrack/smartrack-pi/companion/{file_name}")
    software.push_companion_config(file_name)
if __name__ == "__main__":
    app()
