from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):

    def __init__(self, ip: str) -> None:
        self.ip = ip

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass
