import re
from dataclasses import dataclass
from typing import List

from goflex_shell.command_executor import CommandExecutor
from wrappers.base_wrapper import BaseCommand

LS_OUTPUT_PREFIX = 'total'
LS_FILENAME_REGEX = re.compile(r'"(.*?)"')
DIRECTORY_MARKER = 'd'
LS_COMMAND = '/bin/ls -q -l "{}"'


@dataclass
class PathInfo:
    is_dir: bool
    name: str


class ListPathInfo(BaseCommand):

    def execute(self, path: str) -> List[PathInfo]:
        ls_output = self._remove_ls_header_line(self._execute_ls(path))

        paths = [self._get_path_info_from_entry(entry) for entry in ls_output]

        return paths

    @staticmethod
    def _remove_ls_header_line(ls_output: List[str]) -> List[str]:
        """
        Remove the line at the start that shows up if you are listing a directory:

        > total 160
        """
        return ls_output[1:] if ls_output[0].startswith(LS_OUTPUT_PREFIX) else ls_output

    def _execute_ls(self, path: str) -> List[str]:
        """
        Executes LS, returns the command output in lines of strings.
        """
        return CommandExecutor.execute(self.ip, self._get_ls_command(path)).decode().splitlines()

    @staticmethod
    def _get_ls_command(path: str) -> str:
        return LS_COMMAND.format(path)

    @staticmethod
    def _get_path_info_from_entry(entry: str) -> PathInfo:
        is_dir = entry.startswith(DIRECTORY_MARKER)
        file_name = LS_FILENAME_REGEX.search(entry).group(1)

        return PathInfo(is_dir, file_name)
