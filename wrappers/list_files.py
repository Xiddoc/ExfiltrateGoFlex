from typing import List

from goflex_shell.command_executor import CommandExecutor
from wrappers.base_wrapper import BaseCommand


class ListFiles(BaseCommand):

    def execute(self, path: str) -> List[str]:
        files = CommandExecutor.execute(self.ip, f"/bin/ls {path}")

        return files.splitlines()
