from typing import Dict,List
from core.Interfaces.Iplugins import IPluging


class Default(IPluging):

    question: List[Dict] = None

    @property
    def nombre(self):
        return 'Default'

    def execute(self,questionary):
        questionary.print('Hello World 🦄, este es un programa para realizar distinto tipos de preguntas\n \
                          que tipo de preguntas quieres realizar"')
    def questi_on(self):
        return[{'name': 'name'}]