from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from tqdm import tqdm

from MODULOS.Modelo.FtpXsales import FtpXsales

def main():
    f=FtpXsales()

    #conexion con el dz
    f.Login()

    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    questions = [
        {
            'type': 'confirm',
            'name': 'Consulta',
            'message': 'Deseas revisar todas las rutas?',
        },

        {
            'type': 'checkbox',
            'name': 'Rutas',
            'message': 'Seleciona las rutas que deseas revisar',
            'choices': f.parseandorutas(),
            'when': lambda answers: not answers['Consulta']
        }
    ]

    answers = prompt(questions)
    if not answers['Consulta']:
        _rutas=answers['Rutas']
    else:
        _rutas=f._rutas

    rutas=tqdm(_rutas)
    if len(rutas)==0:
        print('Han sido borradas las base intenta el dia de mañana')
    else: 
        for i in rutas:
            f.DESCARGA(i)
            rutas.set_description("Descargando ruta: %s" % i)
            f.descomprimir(i)
            rutas.set_description("Descomprimiendo  ruta: %s" % i)
            f.procesarInfo(i)
            rutas.set_description("Obtenido info. ruta: %s" % i)
    print('Proceso Finalizado.')

