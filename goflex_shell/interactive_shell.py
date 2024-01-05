from config import PROMPT
from goflex_shell.command_executor import CommandExecutor


class InteractiveShell:

    @staticmethod
    def interactive(ip: str) -> None:
        while True:
            command = input(PROMPT)

            print(CommandExecutor.execute(ip, command).decode())
