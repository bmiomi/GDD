from typing import Dict,List

import questionary
from core.Interfaces.Iplugins import IPluging


class Default(IPluging):

    question: Dict= {
        'type':'rawlist',
        'name':'ms',
        'message':'este es me modulo principal',
        'choices':["1","2","3","4","5"]
    }

    getsubmodule=None

    @property
    def nombre(self):
        return 'Default'

    def execute(self,questionary):
        questionary.print('Hello World 🦄"')

    def questions(self):
        return[{'name': 'name'}]
    
