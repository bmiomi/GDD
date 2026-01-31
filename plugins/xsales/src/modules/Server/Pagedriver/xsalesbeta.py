import json
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin

from plugins.xsales.src.modules.Server.config import ConfigServer

class XsalesLoginClient:
    """Cliente de login automatizado para XSales."""
    def __init__(self, base_url="https://prd1.xsalesmobile.net", verify_ssl=False, tenant=None):
        self.base_url = base_url
        self.verify_ssl = verify_ssl
        self.tenant = tenant
        self.session = requests.Session()
        self.jwt_token = None
        self.session_cookie = None
        self.virtual_path = None
        self.last_user_logon_ok = None
        self.last_user_logon_body = None
        
        if not verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def extract_jwt_from_html(self, html):
        """Extrae JWT_TOKEN del HTML del login."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            jwt_input = soup.find('input', {'id': 'JWT_TOKEN'})
            
            if jwt_input and jwt_input.get('value'):
                jwt_value = jwt_input.get('value')
                
                virtual_path_input = soup.find('input', {'id': 'virtualPath'})
                if virtual_path_input:
                    self.virtual_path = virtual_path_input.get('value')
                
                return jwt_value
        except Exception as e:
            print(f"Error extrayendo JWT: {e}")
        return None
    
    def get_jwt_token(self):
        """Descarga el HTML del login y extrae el JWT_TOKEN."""
        login_url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/")
        
        try:
            r = self.session.get(login_url, timeout=10, verify=self.verify_ssl)
            
            if r.status_code != 200:
                return False
            
            for cookie in self.session.cookies:
                if cookie.name == 'ASP.NET_SessionId':
                    self.session_cookie = cookie.value
            
            self.jwt_token = self.extract_jwt_from_html(r.text)
            return self.jwt_token is not None
        except Exception as e:
            print(f"Error obteniendo JWT: {e}")
            return False
    
    def set_connection(self, connection_name):
        """Ejecuta setConnection."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/setConnection")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://prd1.xsalesmobile.net',
            'Referer': f'https://prd1.xsalesmobile.net/{self.tenant}/xsm/Login',
        }
        
        data = {'connectionName': connection_name}
        
        try:
            r = requests.post(
                url,
                data=data,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            
            if r.status_code == 200:
                try:
                    resp_data = r.json()
                    msg = resp_data.get('Message', '(sin mensaje)')
                    print(f"  → setConnection: {msg}")
                except:
                    pass
                return True
            else:
                print(f"  ✗ setConnection: Status {r.status_code}")
                return False
        except Exception as e:
            print(f"  ✗ Error en setConnection: {e}")
            return False
    
    def set_language(self):
        """Ejecuta SetLanguage."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/SetLanguage")
        
        headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        try:
            r = requests.post(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            
            if r.status_code == 200:
                try:
                    resp_data = r.json()
                    msg = resp_data.get('Message', '(sin mensaje)')
                    print(f"  → SetLanguage: {msg}")
                except:
                    print(f"  → SetLanguage: OK ({len(r.text)} bytes)")
                return True
            else:
                print(f"  ✗ SetLanguage: Status {r.status_code}")
                return False
        except Exception as e:
            print(f"  ✗ Error en SetLanguage: {e}")
            return False
    
    def get_setup_login_external(self):
        """Ejecuta getSetupLoginExternal."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/getSetupLoginExternal")
        
        headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        try:
            r = requests.post(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            
            if r.status_code == 200:
                try:
                    resp_data = r.json()
                    msg = resp_data.get('Message', '(sin mensaje)')
                    print(f"  → getSetupLoginExternal: {msg}")
                except:
                    print(f"  → getSetupLoginExternal: OK")
                return True
            else:
                print(f"  ✗ getSetupLoginExternal: Status {r.status_code}")
                return False
        except Exception as e:
            print(f"  ✗ Error en getSetupLoginExternal: {e}")
            return False

    def user_logon_server(self, username: str, password: str):
        """Ejecuta userLogonServer con credenciales."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/userLogonServer")

        headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': f'ASP.NET_SessionId={self.session_cookie}',
        }

        data = {
            'username': username,
            'password': password,
        }

        try:
            r = requests.post(
                url,
                data=data,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
           
            if r.status_code == 200:
                self.last_user_logon_ok = True
                self.last_user_logon_body = r.text
                print(f"  → userLogonServer: OK ({r.text})")
                return True, r.text
            self.last_user_logon_ok = False
            self.last_user_logon_body = r.text
            return False, r.text
        except Exception as e:
            self.last_user_logon_ok = False
            self.last_user_logon_body = str(e)
            return False, str(e)
    
    def login(self, connection_name, username=None, password=None):
        """Ejecuta el flujo completo de login."""
        if not self.get_jwt_token():
            return False
        if not self.set_connection(connection_name):
            return False
        if not self.set_language():
            return False
        if not self.get_setup_login_external():
            return False
        if username and password:
            user_ok, _ = self.user_logon_server(username, password)
            if not user_ok:
                return False
        return True


class Xsales:
  

  _config=ConfigServer()

  def __init__(self,name:str) -> None:
    self.session=HTMLSession()
    self.estado=True
    self.xsalesresponse=None 
    self.evento=None
    self.login_info = None
    self.usuari,self.credencial=self._config.CredencialesServer()
    self.name=name.upper()
    self.bearer_token = None
    self.cookies_ = { 'ASP.NET_SessionId': self.__sesssionxsales() }  
    self.__logerarseesion()
    print(f"[DEBUG] Xsales inicializado para tenant: {self.name}")
    print(f"[DEBUG] Usuario: {self.usuari}, Credencial: {'*' * len(self.credencial)}")

  @property
  def config(self):
     return self._config

  @property
  def get_tamanio_paguinacion(self):
    "retorna 1 si se tiene paguinacion caso contario retorna 0"
    return int(self.respuestasXsales()/30)

  def __sesssionxsales(self):
    "obtiene la session de xsales usando el nuevo cliente de login."
    try:
        connection_name = self.name + '_XSS_441_PRD'
        
        # Usar el nuevo cliente de login
        login_client = XsalesLoginClient(
            base_url="https://prd1.xsalesmobile.net",
            verify_ssl=False,
            tenant=self.name
        )
        
        if login_client.login(connection_name, self.usuari, self.credencial):
            self.bearer_token = login_client.jwt_token
            self.session_cookie = login_client.session_cookie
            self.login_info = {
                "ok": True,
                "tenant": self.name,
                "connection_name": connection_name,
                "jwt_token": self.bearer_token,
                "session_cookie": self.session_cookie,
                "virtual_path": login_client.virtual_path,
                "user_logon_ok": login_client.last_user_logon_ok,
                "user_logon_body": login_client.last_user_logon_body,
            }
            print(f"✓ Login exitoso")
            print(f"✓ JWT Token: {self.bearer_token[:50]}...")
            print(f"✓ Session Cookie: {self.session_cookie[:20]}...")
            print(f"✓ Login info: {self.login_info}")
            return self.session_cookie
        else:
            self.login_info = {
                "ok": False,
                "tenant": self.name,
                "connection_name": connection_name,
                "jwt_token": None,
                "session_cookie": None,
                "virtual_path": login_client.virtual_path,
            }
            print("✗ Error en el flujo de login")
            print(f"✗ Login info: {self.login_info}")
            return None
    except Exception as e:
        self.login_info = {
            "ok": False,
            "tenant": self.name,
            "connection_name": None,
            "jwt_token": None,
            "session_cookie": None,
            "virtual_path": None,
            "error": str(e),
        }
        print(f"✗ Exception en __sesssionxsales: {e}")
        print(f"✗ Login info: {self.login_info}")
        return None

  @property
  def get_login_info(self):
    """Retorna el resultado estructurado del login."""
    return self.login_info
  
  def __evento(self):
    """
    Retorna token __EVENTVALIDATION vacío.
    Con Bearer token, este parámetro no es necesario para las consultas modernas.
    """
    return ''

  def __logerarseesion(self):
    """
    Valida la sesión con Bearer token.
    Ya no utiliza usuario/contraseña, ahora usa el JWT_TOKEN obtenido.
    """
    print("\n" + "="*60)
    print("🔐 INICIANDO VALIDACIÓN DE SESIÓN")
    print("="*60)
    
    try:
        if not self.bearer_token:
            print("✗ No hay Bearer token disponible")
            return False
        
        print(f"✓ Bearer token disponible: {self.bearer_token[:20]}...")
        print(f"✓ Distribuidor: {self.name}")
        
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': f'Bearer {self.bearer_token}',
        }
        
        print(f"→ Validando sesión en: https://prd1.xsalesmobile.net/{self.name}/xsm/Login/validatedSession")
        
        # Validar sesión con Bearer token
        response = self.session.request(
            'post',
            f'https://prd1.xsalesmobile.net/{self.name}/xsm/Login/validatedSession',
            headers=head,
            cookies=self.cookies_
        )
        
        print(f"→ Status Code: {response.status_code}")
        print(f"→ Response Length: {len(response.text)} caracteres")
        
        if response.status_code == 200:
            print("✓ Sesión validada correctamente")
            
            # Guardar HTML de respuesta para debug
            try:
                debug_file = f"REPORTES/SERVER/post_login_{self.name}.html"
                print(f"→ Intentando guardar en: {debug_file}")
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✓ HTML guardado en: {debug_file}")
            except Exception as e:
                print(f"⚠ No se pudo guardar HTML: {e}")
            
            # Navegar a la página de consulta de base de datos
            print("→ Navegando a página de consultas...")
            try:
                query_page_url = f'https://prd1.xsalesmobile.net/{self.name}/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx'
                headers_nav = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Authorization': f'Bearer {self.bearer_token}',
                }
                
                nav_response = self.session.get(query_page_url, headers=headers_nav, cookies=self.cookies_)
                
                # Guardar HTML de página de consultas
                debug_nav_file = f"REPORTES/SERVER/query_page_{self.name}.html"
                with open(debug_nav_file, 'w', encoding='utf-8') as f:
                    f.write(nav_response.text)
                print(f"✓ Página de consultas guardada en: {debug_nav_file}")
                
                # Verificar si encontramos la etiqueta esperada
                if 'Consulta Base de Datos' in nav_response.text or 'MuiTypography' in nav_response.text:
                    print("✓ Página de consultas encontrada correctamente")
                else:
                    print("⚠ Advertencia: No se encontró la etiqueta 'Consulta Base de Datos'")
                    
            except Exception as e:
                print(f"⚠ Error navegando a página de consultas: {e}")
            
            return True
        else:
            print(f"✗ Error validando sesión: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Exception en __logerarseesion: {e}")
        return False

 
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
    print(f"[DEBUG] Ejecutando SQL: {sql[:100]}...")
    
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
    
    # Incluir Bearer token si está disponible
    if self.bearer_token:
        headers['Authorization'] = f'Bearer {self.bearer_token}'
    
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

    self.xsalesresponse=self.session.request('post','https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx', headers=headers, data=data, cookies=self.cookies_)

    # Guardar HTML de respuesta para debugging
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_file = f"REPORTES/SERVER/query_response_{self.name}_{timestamp}.html"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(self.xsalesresponse.text)
        print(f"✓ HTML de consulta guardado en: {debug_file}")
    except Exception as e:
        print(f"⚠ No se pudo guardar HTML de consulta: {e}")

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
    
    # Incluir Bearer token si está disponible
    if self.bearer_token:
        headers['Authorization'] = f'Bearer {self.bearer_token}'
      
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

    responsed = self.session.request('post','https://prd1.xsalesmobile.net/'+self.name+'/xsm/app/webForms/webTools/sqlQuery/DBQueryUI.aspx', headers=headers, cookies=self.cookies_, data=data)
    
    with open( f'{self._config.folderexcel()}{self.name}.xlsx','wb') as file:
        file.write(responsed.content )
