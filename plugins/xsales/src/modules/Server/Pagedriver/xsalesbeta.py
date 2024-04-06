import json
from annotated_types import UpperCase # type: ignore
from requests_html import HTMLSession

from plugins.xsales.src.modules.Server.config import ConfigServer

class Xsales:
  
  session:HTMLSession =HTMLSession()
  _config:ConfigServer =ConfigServer()

  xsalesresponse=None 
  evento=None
  VERSION="XSales® SFA - 4.4.1 AFG"
  URLBASE='https://prd1.xsalesmobile.net/'
  HEADERS = {
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
          'Accept-Language': 'es-ES,es;q=0.9',
      }

  def __init__(self,name:UpperCase) -> None:
    self.name=name
    self.cookies_ = { 'ASP.NET_SessionId': self.__sesssionxsales() }  
    self.logerarseesion()

  @property
  def config(self):
     return self._config

  @property
  def get_tamanio_paguinacion(self):
    "retorna 1 si se tiene paguinacion caso contario retorna 0"
    return int(self.respuestasXsales()/30)

  @property
  def extraerhtml(self,) -> list[dict]:
    # -  (fila) # |  (columna)
      return self.config.excelfile.recorrer_tabla(self.xsalesresponse.html.xpath('//*[@id="GrwDatatable"]')[0].html)

  @property
  def status_table(self) -> bool :
    ' retorna true si al verificar posee registros la tabla,limite de registros en  Tabla a mostrar 30'
    return True if self.respuestasXsales() >=1 else False

  def versionxsales(self):
     valores=self.session.request('get',self.URLBASE +f"/{self.name}/xsm/Login/")
     valores.html.render()
     if valores.status_code==200:
       value=valores.html.xpath('//*[@id="loginFooter"]/div/span/sup')
       return value[0].text

  def __sesssionxsales(self):

    "obtine la session de xsales y se retorna el valor."

    xsaleslogin=self.session.get(url=f"{self.URLBASE}{self.name}/xsm/Login")
    cookiexsales=xsaleslogin.cookies.get('ASP.NET_SessionId')
    self.session.post(self.URLBASE+self.name+'/xsm/Login/validatedSession')
    self.session.post(self.URLBASE+self.name+"/xsm/Login/serverVersion")
    self.session.post(self.URLBASE+self.name+"/xsm/Login/DisplayDDListConnections")
    self.session.post(self.URLBASE+self.name+'/xsm/Login/setConnection',data={'connectionName':self.name+'_XSS_441_PRD'})
    self.session.post(self.URLBASE+self.name+'/xsm/Login/SetLanguage')
    return cookiexsales
 
  def __evento(self):

    resp=self.session.get(self.URLBASE+self.name+'/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx', headers=self.HEADERS, cookies=self.cookies_)

    fragmentlist=resp.html.xpath("//*[@id='__EVENTVALIDATION']")[0]
    print(fragmentlist)
    return fragmentlist.attrs.get('value')

  def logerarseesion(self):        
 
    data = { 'connectionName': self.name+'_XSS_441_PRD',
            'password': self.config.CredencialesServer[0],
            'username': self.config.CredencialesServer[1]
           }

    response=self.session.post(
         self.URLBASE+self.name+'/xsm/Login/userLogonServer',
         headers=self.HEADERS, 
         cookies=self.cookies_, 
         data=data
        )

    resultado=json.loads(response.content.decode('UTF-8'))

    try:
      print('se inprimw el resultado:'+resultado)
      if resultado['Message'] !='Authenticated':
        self._config.CredencialesServer= self.name
        data['password']=self._config.CredencialesServer[0]
        data['username']=self._config.CredencialesServer[1]
        print(f'\n Contraseña defaul Errada..\n Intentando con clave del archivo {self.config.CredencialesServer[0], self.config.CredencialesServer[1]}')
        self.logerarseesion()
    except:

      print('se intento con la clave proporcionaa en el archivo de configuracion sin enbargo no se tubo excito favor validar los datos ingresados')

  def respuestasXsales(self)-> str:

    if self.versionxsales() !='"XSales® SFA - 4.4.1 AFG"':
      respuesta=self.xsalesresponse.html.xpath('//*[@id="lblMensajeResultado"]')[0]
      mensaje=respuesta.text
      if "Comando Ejecutado Exitosamente" in  mensaje:
          return int(''.join([m for m in mensaje if m.isdigit()]))
    else:
      respu=self.xsalesresponse.html.xpath('//*[@id="container-QueryBD"]/div/div[2]/div[3]/div[1]')
      self.xsalesresponse.iter_content
      mensaje=respu.text
      if "QueryOK" == mensaje:
          return 1
      return 0
  
  def consulta_new_version(self,sql):
      self.HEADERS['Referer'] = self.URLBASE + self.name + '/xsm/app/css/global.css?vcss=20191107'
      data={"Catalog":self.name+"_XSS_441_PRD", "Query":sql, "CultureName":"es-VE", "Decimals":" "}
      return self.session.request('post',self.URLBASE+self.name+'/xsm/QueryBD/ExecuteConsult', headers=self.HEADERS, data=data).text

  def consultar(self,sql):

    self.HEADERS['Referer'] = self.URLBASE + self.name + '/xsm/app/css/global.css?vcss=20191107'        

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

    self.xsalesresponse=self.session.request('post','https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx', headers=self.HEADERS, cookies=self.cookies_,data=data)

  def Descargar_excel(self,sql):      
        
    self.HEADERS['Referer']=self.URLBASE+self.xsales.name+'/xsm/app/css/global.css?vcss=20191107'

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

    responsed = self.session.request('post',self.URLBASE+self.name+'/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx', headers=self.HEADERS, cookies=self.cookies_,data=data,stream=True)
 
 
    # for c in responsed.iter_content( chunk_size=8192):
    #    file.write(c)    
 
    with open( f'{self._config.folderexcel}{self.name}.xlsx','wb') as file:
        file.write(responsed.content )
