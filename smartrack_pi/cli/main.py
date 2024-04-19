import typer
from smartrack_pi.display import change_display
from typing import Annotated, Optional
app = typer.Typer()

@app.command()
def display(command: Annotated[str, typer.Argument()], stats: bool = False):
    print(f"Hello {command}")
    change_display.stats_status(stats)

@app.command()
def goodbye(name: Annotated[str, typer.Argument()], formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

if __name__ == "__main__":
    app()