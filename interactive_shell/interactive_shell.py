from interactive_shell.command_executor import CommandExecutor
from config import PROMPT


class InteractiveShell:

    @staticmethod
    def interactive(ip: str) -> None:
        while True:
            command = input(PROMPT)

            print(CommandExecutor.execute(ip, command).strip())
