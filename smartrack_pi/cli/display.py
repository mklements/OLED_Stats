import typer
from typing import Annotated

from smartrack_pi.display import stats_status, display_text
app = typer.Typer()


@app.command()
def stats(enable: Annotated[bool, typer.Option(help="Turns Stats Loop on or off")] = True):
    print(f"Setting stats display to {enable}")
    stats_status(enable)


@app.command()
def message(message: Annotated[str, typer.Argument(help="Message to display")]):    
    print(f"Displaying Message: {message}")
    print("Warning:  Stats will be disabled, to re-enable 'smartrack display stats'")
    display_text(message)


if __name__ == "__main__":
    app()