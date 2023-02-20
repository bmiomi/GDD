from os import path,sep
import pandas as pd
import requests
from questionary import prompt
from bs4 import BeautifulSoup
import yaml

file = path.join(f'plugins{sep}NUO{sep}config.yaml')
Url2=yaml.load(open(file, 'r'), Loader=yaml.FullLoader)
question=[
  {

  'type': 'path',
  'name': 'file',
  'message': 'Seleccione la ubicacion del archivo', 
  },
]

headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': Url2,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': f'{Url2}/inicio',
        'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

credenciales = {
      'ingUsuario': 'bmiomi',
      'ingPassword': 'rous199305'
    }


def data(dataset) -> list[dict]:
  return [  dict(zip(list(dataset.to_dict()),i))  for i in dataset.values.tolist() ]

def post_login(session, url:str, headers:dict, cookie:dict, credenciales:dict): 
    session.post(f'{url}inicio', 
                      headers=headers, cookies=cookie, data=credenciales, 
                      verify=False)

def menu_ticket(session, url:str,headers:dict, cookie:dict) -> None: 
    page=session.get(f'{url}tickets',headers=headers, cookies=cookie)
    soup = BeautifulSoup(page.text, "html.parser")
    #obtenemos el ultimo id para seguir
    titletag = soup.html.body.table.tbody.td.string
    print(f'id del Sistema: {titletag} ,  Id a usar {int(titletag[1:])+1}' )

def enviartickets( url:str, headers:dict, cookie:dict, tikets:list[dict] ) -> None:    
    import time
    contador=0
    for i in tikets:
        response = requests.post( f"{url}tickets", headers=headers, cookies=cookie, data=i, verify=False)
        time.sleep(3)
        contador+=1
        print(contador,'=>',response)

def editartickets( url:str, headers:dict, cookie:dict, tikets:list[dict] ):
    for i in tikets:
        response=requests.put(f"{url}", data=i)

def main(curdir:str):
    #lee  ruta archivo excel
    dataset=pd.read_excel(curdir)
    # genera una lista de diccionarios donde cada diccionario es un registro a enviar
    tickets=data(dataset)
    # se estable una session
    session=requests.session()
    #se obtiene un response de la paguina a la cual se envio la peticion.
    r =session.get(f"{Url}")

    # se obtiene la cabecera de la session
    # header_=requests.head(Url)

    #se  obtiene las cookies
    cookie=session.cookies.get_dict()

    # se estable una conexion post donde se envia los datos para logearse a la paguina
    post_login( session, Url, headers, cookie, credenciales)
    # se  tiene  la  pantalla principal del sistema.
    menu_ticket( session, Url, headers, cookie)
    # se envia la data 
    enviartickets(Url, headers, cookie,  tickets)

if __name__=='__main__':
    
  try:
    answer=prompt(question)
    curdir=answer.get('file')
    main(curdir)
  except Exception as e:
    print( f'Se produjo un error {e} contactar al admistrador')
