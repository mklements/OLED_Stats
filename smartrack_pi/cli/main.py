import typer
from display import change_display
from typing import Annotated, Optional
app = typer.Typer()
import sys
import os

# # Get the current script's directory
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # Get the parent directory by going one level up
# parent_dir = os.path.dirname(current_dir)
# # Add the parent directory to sys.path
# sys.path.append(parent_dir)

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