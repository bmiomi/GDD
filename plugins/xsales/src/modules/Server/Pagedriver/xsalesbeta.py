import json
from requests_html import HTMLSession

from plugins.xsales.src.modules.Server.config import ConfigServer

class Xsales:
  
  _config=None
  
  def __init__(self,name:str) -> None:
    self._config=ConfigServer()
    self.session=HTMLSession()
    self.xsalesresponse=None 
    self.evento=None
    self.usuari,self.credencial=self._config.CredencialesServer()
    self.name=name.upper()
    self.cookies_ = { 'ASP.NET_SessionId': self.__sesssionxsales() }  
    self.__logerarseesion()


  @property
  def config(self):
     return self._config

  @property
  def get_tamanio_paguinacion(self):
    "retorna 1 si se tiene paguinacion caso contario retorna 0"
    return int(self.respuestasXsales()/30)

  def __sesssionxsales(self):
    "obtine la session de xsales y se retorna el valor."
    payload = {'connectionName':self.name+'_XSS_441_PRD'}
    xsaleslogin=self.session.get("https://prd1.xsalesmobile.net/"+self.name+"/xsm/Login")
    cookiexsales=xsaleslogin.cookies.get('ASP.NET_SessionId')
    self.session.post('https://prd1.xsalesmobile.net/'+self.name+'/xsm/Login/validatedSession')
    self.session.post("https://prd1.xsalesmobile.net/"+self.name+"/xsm/Login/serverVersion")
    self.session.post("https://prd1.xsalesmobile.net/"+self.name+"/xsm/Login/DisplayDDListConnections")
    self.session.post('https://prd1.xsalesmobile.net/'+self.name+'/xsm/Login/setConnection',data=payload)
    self.session.post('https://prd1.xsalesmobile.net/'+self.name+'/xsm/Login/SetLanguage')
    return cookiexsales
 
  def __evento(self):

    hea = {
          'Connection': 'keep-alive',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-User': '?1',
          'Sec-Fetch-Dest': 'document',
          'Referer': 'https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/css/global.css?vcss=20191107',
          'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
          'Origin': 'https://prd1.xsalesmobile.net',
      }
    resp=self.session.get('https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx', headers=hea, cookies=self.cookies_)
    fragmentlist=resp.html.xpath("//*[@id='__EVENTVALIDATION']")[0]
    return fragmentlist.attrs.get('value')

  def __logerarseesion(self):
 
    head = {
          'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-User': '?1',
          'Sec-Fetch-Dest': 'empty',
          'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
          'Referer': 'https://prd1.xsalesmobile.net/'+self.name+'/xsm/Login/Index',
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Length': '0',
          'Origin': 'https://prd1.xsalesmobile.net',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
    
    data = { 'connectionName': self.name+'_XSS_441_PRD','username': self.usuari ,'password': self.credencial}

    response=self.session.request('post','https://prd1.xsalesmobile.net/'+self.name+'/xsm/Login/userLogonServer',
    headers=head, 
    cookies=self.cookies_, 
    data=data)
    print(response.content,file=open("ad.txt",'w'))

    resultado=json.loads(response.content.decode('UTF-8'))

    if resultado['Message'] !='Authenticated':

      print('\n Contraseña con clave defaul Errada..')
      print(f'Intentando con con clave {self.name}')
      credencial=self._config.CredencialesServer(self.name)
      data['username']=credencial[0]
      data['password']=credencial[1]

      self.session.request('post',
      f'https://prd1.xsalesmobile.net/{self.name}/xsm/Login/userLogonServer',
      headers=head, 
      cookies=self.cookies_, 
      data=data)
 
  def extraerhtml(self, excelfile) -> list[dict]:
    # -  (fila) # |  (columna)
        return excelfile.recorrer_tabla(self.xsalesresponse.html.xpath('//*[@id="GrwDatatable"]')[0].html)

  def respuestasXsales(self)-> str:
    respuesta=self.xsalesresponse.html.xpath('//*[@id="lblMensajeResultado"]')[0]

    mensaje=respuesta.text
    if "Comando Ejecutado Exitosamente" in  mensaje:
        return int(''.join([m for m in mensaje if m.isdigit()]))

  def status_table(self) -> bool :
    ' retorna true si al verificar posee registros la tabla,limite de registros en  Tabla a mostrar 30'
    return True if self.respuestasXsales() >=1 else False

  def consultar(self,sql):
    
    headers = {
          'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'Origin': 'https://prd1.xsalesmobile.net',
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.197',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-User': '?1',
          'Sec-Fetch-Dest': 'document',
          'Referer': 'https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/css/global.css?vcss=20191107',
          'Accept-Language': 'es-ES,es;q=0.9',
      }
    self.evento=self.__evento()      
    data = {
      '__EVENTTARGET': '',
      '__EVENTARGUMENT': '',
      '__LASTFOCUS': '',
      '__VIEWSTATE': '',
      'Ddl_BaseDatos': self.name+'_XSS_441_PRD',
      'optradio': 'Rb_DecimalCo',
      'TxtSql': sql,
      'lblBtnExecute': 'Ejecutar',
      'ddlExport': '-1',
      '__SCROLLPOSITIONX': '0',
      '__SCROLLPOSITIONY': '0',
      '__EVENTVALIDATION': self.evento
    }

    self.xsalesresponse=self.session.request('post','https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx', headers=headers, cookies=self.cookies_,data=data)

  def Descargar_excel(self,sql):


    headers = {
          'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'Origin': 'https://prd1.xsalesmobile.net',
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.197',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-User': '?1',
          'Sec-Fetch-Dest': 'document',
          'Referer': 'https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/css/global.css?vcss=20191107',
          'Accept-Language': 'es-ES,es;q=0.9',
      }
      
    data = {
        '__EVENTTARGET': 'ddlExport',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '',
        'Ddl_BaseDatos': self.name+'_XSS_441_PRD',
        'optradio': 'Rb_DecimalCo',
        'TxtSql': sql,
        'ddlExport': 'excel',
        'lblBtnExportar': 'Exportar',
        '__SCROLLPOSITIONX': '0',
        '__SCROLLPOSITIONY': '0',
        '__EVENTVALIDATION':self.evento
      }

    responsed = self.session.request('post','https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx', headers=headers, cookies=self.cookies_,data=data)
    
    with open( f'{self._config.folderexcel()}{self.name}.xlsx','wb') as file:
        file.write(responsed.content )
