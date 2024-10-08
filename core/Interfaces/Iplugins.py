from typing import Protocol,List,Dict

class IPluging(Protocol):

    question: List[Dict] = None

    @property
    def nombre(self):
        raise NotImplementedError

    def execute(self, *args, **kargs):
        raise NotImplementedError
