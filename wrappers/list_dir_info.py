import re
from dataclasses import dataclass
from typing import List, Tuple

from goflex_shell.command_executor import CommandExecutor
from wrappers.base_wrapper import BaseCommand

LS_OUTPUT_PREFIX = 'total'
DIRECTORY_MARKER = 'd'
LS_INFO_COMMAND = '/bin/ls -l "{}"'
LS_FILENAMES_COMMAND = '/bin/ls -1 -q "{}"'
UNICODE_ESCAPED_CHAR = re.compile(r"\?+")
WILDCARD = '"*"'


@dataclass
class PathInfo:
    is_dir: bool
    name: str


class ListPathInfo(BaseCommand):

    def execute(self, path: str) -> List[PathInfo]:
        ls_info_output = self._remove_ls_header_line(self._execute_info_ls(path))
        ls_filenames_output = self._execute_ls_for_filenames(path)

        paths = [self._get_path_info_from_entry(entry) for entry in zip(ls_info_output, ls_filenames_output)]

        return paths

    @staticmethod
    def _remove_ls_header_line(ls_output: List[str]) -> List[str]:
        """
        Remove the line at the start that shows up if you are listing a directory:

        > total 160
        """
        return ls_output[1:] if ls_output[0].startswith(LS_OUTPUT_PREFIX) else ls_output

    def _execute_info_ls(self, path: str) -> List[str]:
        """
        Executes LS, returns the command output in lines of strings.
        """
        return CommandExecutor.execute(self.ip, self._get_ls_info_command(path)).decode().splitlines()

    @staticmethod
    def _get_ls_info_command(path: str) -> str:
        return LS_INFO_COMMAND.format(path)

    def _execute_ls_for_filenames(self, path: str) -> List[str]:
        """
        Executes LS, returns the command output in lines of strings.
        """
        return CommandExecutor.execute(self.ip, self._get_ls_filenames_command(path)).decode().splitlines()

    @staticmethod
    def _get_ls_filenames_command(path: str) -> str:
        escaped_path = UNICODE_ESCAPED_CHAR.sub(WILDCARD, path)

        return LS_FILENAMES_COMMAND.format(escaped_path)

    @staticmethod
    def _get_path_info_from_entry(entry: Tuple[str, str]) -> PathInfo:
        is_dir_entry, filename = entry

        is_dir = is_dir_entry.startswith(DIRECTORY_MARKER)

        return PathInfo(is_dir, filename)
