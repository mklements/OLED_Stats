import typer
from display import change_display

app = typer.Typer()

@app.command()
def display(command: str, stats: bool = True, *messages):
    print(f"Hello {command}")
    change_display.stats_status(stats)

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

if __name__ == "__main__":
    app()