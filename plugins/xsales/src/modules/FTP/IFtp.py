from typing import Protocol


class IFtp(Protocol):

    def dir(self):
        raise NotImplemented

    def acceso(self, *arg):
        raise NotImplemented

    def change_dir(self, dir: str):
        raise NotImplemented

    def list_dir(self, *arg):
        raise NotImplemented