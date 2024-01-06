from dataclasses import dataclass
from typing import List

from goflex_shell.command_executor import CommandExecutor
from wrappers.base_wrapper import BaseCommand

LS_OUTPUT_PREFIX = 'total'


@dataclass
class PathInfo:
    is_dir: bool
    name: str


class ListPathInfo(BaseCommand):

    def execute(self, path: str) -> List[PathInfo]:
        files = CommandExecutor.execute(self.ip, f'/bin/ls -l "{path}"').decode().splitlines()

        remove_header = files[1:] if files[0].startswith(LS_OUTPUT_PREFIX) else files

        paths = [self._get_path_info_from_entry(entry) for entry in remove_header]

        return paths

    @staticmethod
    def _get_path_info_from_entry(entry: str) -> PathInfo:
        is_dir = entry.startswith('d')
        file_name = entry.split(' ')[-1]

        return PathInfo(is_dir, file_name)
