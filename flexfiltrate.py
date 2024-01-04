"""
CLI interface for the exfiltrator.
"""
import typer

from interactive_shell.interactive_shell import InteractiveShell

cli = typer.Typer()


# noinspection PyUnusedFunction
@cli.command()
def shell(ip: str) -> None:
    try:
        InteractiveShell.interactive(ip)
    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    cli()
