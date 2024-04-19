"""Smartrack entry point script."""
# smartrack_pi/cli/__init__.py

from smartrack_pi.cli import cli
from smartrack_pi import __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
