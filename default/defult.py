from typing import Dict,List

import questionary
from core.Interfaces.Iplugins import IPluging


class Default(IPluging):

<<<<<<< HEAD
    question: Dict= {
        'type':'rawlist',
        'name':'ms',
        'message':'este es me modulo principal',
        'choices':["1","2","3","4","5"]
    }

    getsubmodule=None
=======
    question: List[Dict] = None
    estado=False
>>>>>>> 6809dd0e76ee732e8887cd9e0e71a1ea12626e95

    @property
    def nombre(self):
        return 'Default'

<<<<<<< HEAD
    def execute(self,questionary):
        questionary.print('Hello World 🦄"')

    def questions(self):
        return[{'name': 'name'}]
    
=======
    def execute(self,questionary:questionary):

        questionary.print('Hello {} 🦄, este es un programa para realizar distinto tipos de preguntas')
        respuesta=questionary.confirm('Deseas que empecemos:').ask()
     
        if respuesta :
            self.questi_on(questionary)
        respuesta=questionary.confirm('Deseas  ingresar a nuestro menu de opciones:').ask()
        
        if respuesta :
            pass

        questionary.print('Bueno! 😁, no tengo que mas ofrecerte 😎, decite y vuelve a visitarme😜, te espero 😉.')



    def questi_on(self,questionari: questionary) -> List[Dict]:
        
        uno=questionari.rawselect('seleccione una fruta',choices=["🍇","🍑","🍈","🍉","🍊","🍒","🍐","🍍","🍎","🥭"]).ask()

        dos=questionari.rawselect('Selecione un estado de animo',choices=["😎","😜","😁","😉"]).ask()

        tres=questionari.checkbox('Seleccione un animal',choices=["🐪","🦍","🦁","🐅","🐆","🐺","🐒","🐈"]).ask()

        return {'Turno':uno,'Opcion':dos,'ContenedorDZ':tres}
     

>>>>>>> 6809dd0e76ee732e8887cd9e0e71a1ea12626e95
