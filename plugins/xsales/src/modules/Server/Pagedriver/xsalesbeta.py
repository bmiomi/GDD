import json
from typing import Dict, Optional
from requests import Response
from requests_html import HTMLSession
from ..config import ConfigServer
from ..enums.propertybase import PropertyBase

class Xsales:
  
  session:HTMLSession =HTMLSession()
  _config:ConfigServer =ConfigServer()

  xsalesresponse=None 
  VERSION="XSales® SFA - 4.4.1 AFG"
  URLBASE=PropertyBase.URLBASE.value
  HEADERS = PropertyBase.HEADERS.value

  def __init__(self,name) -> None:
    self.estado=False
    self.name=name
    self.cookies_={}
    self.__sesssionxsales()
    self.logerarseesion(*self.config.CredencialesServer)

  @property
  def config(self) ->ConfigServer:
     return self._config

  @property
  def versionxsales(self)->Optional[str]:
     self.responsexsales.html.render()
     if self.responsexsales.status_code==200:
       return self.responsexsales.html.xpath('//*[@id="loginFooter"]/div/span/sup')[0].text

  @property
  def respuestasXsales(self)-> Optional[int]:
    #AHV revisar esa propieda
      respu=self.xsalesresponse.html.xpath('//*[@id="container-QueryBD"]/div/div[2]/div[3]/div[1]')
      return 0 if "QueryOk" ==self.xsalesresponse.html.xpath('//*[@id="container-QueryBD"]/div/div[2]/div[3]/div[1]').text else 0

  @property
  def responsexsales(self)->Response:
     return self.session.request('get',f"{self.URLBASE}{self.name}/xsm/Login/")

  def __sesssionxsales(self):

    "obtine la session de xsales y se retorna el valor."
    cookiexsales=self.responsexsales.cookies.get('ASP.NET_SessionId')
    self.session.post(self.URLBASE+self.name+'/xsm/Login/validatedSession')
    self.session.post(self.URLBASE+self.name+"/xsm/Login/serverVersion")
    self.session.post(self.URLBASE+self.name+"/xsm/Login/DisplayDDListConnections")
    self.session.post(self.URLBASE+self.name+'/xsm/Login/setConnection',data={'connectionName':self.name+'_XSS_441_PRD'})
    self.session.post(self.URLBASE+self.name+'/xsm/Login/SetLanguage')
    self.cookies_['ASP.NET_SessionId']=cookiexsales
 
  def logerarseesion(self,username:str,password:str):        
 
    try:

      data = { 'connectionName': self.name+'_XSS_441_PRD','password': password,'username': username }

      response=self.session.post(
            f"{self.URLBASE}{self.name}/xsm/Login/userLogonServer",
            headers=self.HEADERS, 
            cookies=self.cookies_, 
            data=data
          )

      if response.status_code==200:
          respuesta=json.loads( response.text)
          if respuesta['Message'] in ("User or Password Incorrect","Usuario o Password Incorrectos"):

             print(f'\n Contraseña defaul Errada..\n Intentando con credenciales Personalizadas')
             self._config.CredencialesServer= self.name
             self.logerarseesion(*self._config.CredencialesServer)
          self.estado=True
    except BaseException as e:
          print(f" ERROR:{e}") 



  def loginsessiondz(self):
       try:
         self._config.CredencialesServer= self.name
         self.logerarseesion(password=self._config.CredencialesServer[0],username=self._config.CredencialesServer[1])
       except BaseException as e:
          print(' '+e)
          
  def consulta_new_version(self,sql) -> Dict:
      self.HEADERS['Referer'] = self.URLBASE + self.name + '/xsm/app/css/global.css?vcss=20191107'
      data={"Catalog":self.name+"_XSS_441_PRD", "Query":sql, "CultureName":"es-VE", "Decimals":" "}
      response=self.session.request('post',self.URLBASE+self.name+'/xsm/QueryBD/ExecuteConsult', headers=self.HEADERS, data=data)
      if response.status_code==200:  
         respuesta=json.loads( response.text)
         if respuesta['Data']['Result']:
          
          return respuesta['Data']['Result']
      else:
         return None
