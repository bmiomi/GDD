from typing import Protocol,List,Dict
from rich.console import Console


class IPluging(Protocol):

    question: List[Dict] = None

    console: Console = Console()

    @property
    def nombre(self):
        raise NotImplementedError

    def execute(self, *args, **kargs):
        raise NotImplementedError
