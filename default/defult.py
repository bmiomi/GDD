from typing import Dict,List
from core.Interfaces.Iplugins import IPluging


class Default(IPluging):

    question: List[Dict] = None

    @property
    def nombre(self):
        return 'Default'

    def execute(self):
        questionary.print('Hello World 🦄"')

    def questi_on(self):
        return[{'name': 'name'}]