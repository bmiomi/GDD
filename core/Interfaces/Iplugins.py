<<<<<<< HEAD
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
=======
from typing import Protocol,List,Dict

class IPluging(Protocol):

    question: List[Dict] = None

    @property
    def nombre(self):
        raise NotImplementedError

    def execute(self, *args, **kargs):
        raise NotImplementedError
>>>>>>> 8be410330e0e34aa49b9dec88801aabcfc683771
