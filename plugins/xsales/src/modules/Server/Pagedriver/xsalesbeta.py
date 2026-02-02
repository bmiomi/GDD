import json
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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
            candidates = []

            jwt_input = soup.find('input', {'id': 'JWT_TOKEN'})
            if jwt_input and jwt_input.get('value'):
                candidates.append(jwt_input.get('value'))

            jwt_input_name = soup.find('input', {'name': 'JWT_TOKEN'})
            if jwt_input_name and jwt_input_name.get('value'):
                candidates.append(jwt_input_name.get('value'))

            virtual_path_input = soup.find('input', {'id': 'virtualPath'})
            if virtual_path_input:
                self.virtual_path = virtual_path_input.get('value')

            # Buscar en scripts una asignación a JWT_TOKEN
            import re
            match = re.search(r"JWT_TOKEN\s*[:=]\s*['\"]([^'\"]+)['\"]", html)
            if match:
                candidates.append(match.group(1))

            # Priorizar tokens con formato JWT (tres segmentos)
            for candidate in candidates:
                if candidate and candidate.count('.') == 2:
                    return candidate

            # Fallback al primer candidato si no hay JWT clásico
            if candidates:
                return candidates[0]
        except Exception as e:
            print(f"Error extrayendo JWT: {e}")
        return None

    def decrypt_jwt_token(self, encrypted_token: str, key_text: str):
        """Descifra JWT_TOKEN usando AES-CBC con IV fijo (según reactReqMod.js)."""
        try:
            key = key_text.encode('utf-8')
            iv = "8913057a7a02984f".encode('utf-8')
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            import base64
            cipher_bytes = base64.b64decode(encrypted_token)
            decrypted = cipher.decrypt(cipher_bytes)
            return unpad(decrypted, AES.block_size).decode('utf-8')
        except Exception as e:
            print(f"Error descifrando JWT_TOKEN: {e}")
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
            
            raw_token = self.extract_jwt_from_html(r.text)
            if raw_token and raw_token.count('.') != 2:
                decrypted = self.decrypt_jwt_token(raw_token, "6b7b363492e44738913057a7a02984f8")
                if decrypted:
                    self.jwt_token = decrypted
                else:
                    self.jwt_token = raw_token
            else:
                self.jwt_token = raw_token
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
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }
        
        data = {'connectionName': connection_name}
        
        try:
            r = self.session.post(
                url,
                data=data,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            
            if r.status_code == 200:
                try:
                    r.json()
                except Exception:
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }
        
        try:
            r = self.session.post(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            
            if r.status_code == 200:
                try:
                    r.json()
                except Exception:
                    pass
                return True
            else:
                print(f"  ✗ SetLanguage: Status {r.status_code}")
                return False
        except Exception as e:
            print(f"  ✗ Error en SetLanguage: {e}")
            return False

    def server_version(self):
        """Ejecuta serverVersion."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/serverVersion")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }

        try:
            r = self.session.post(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)

    def display_dd_list_connections(self):
        """Ejecuta DisplayDDListConnections."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/DisplayDDListConnections")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
            'Content-Type': 'application/json',
        }

        try:
            r = self.session.post(
                url,
                data='{}',
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)

    def _get_first_connection_name(self, display_list_body: str):
        """Obtiene el primer connectionName desde DisplayDDListConnections."""
        try:
            payload = json.loads(display_list_body)
            data = payload.get("Data") or {}
            connections = data.get("listConnections") or []
            if connections:
                return connections[0].get("connectionName")
        except Exception:
            return None
        return None

    def is_saas(self):
        """Ejecuta IsSaas."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/IsSaas")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }

        try:
            r = self.session.get(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)

    def load_config(self):
        """Ejecuta loadConfig."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/loadConfig")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }

        try:
            r = self.session.post(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)

    def get_culture_information(self):
        """Ejecuta Utils/getCultureInformation."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Utils/Utils/getCultureInformation")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }

        try:
            r = self.session.post(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)

    def get_language_datatable(self):
        """Ejecuta Login/getLanguageDatatable."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/getLanguageDatatable")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }

        try:
            r = self.session.post(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)

    def get_connection_name(self, referer="login"):
        """Ejecuta Login/GetConnectionName."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/GetConnectionName")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'X-Requested-With': 'XMLHttpRequest',
            'Cache-Control': 'no-store',
            'Referer': f'{self.base_url}/{self.tenant}/xsm/{"Main" if referer == "main" else "Login"}/',
        }

        try:
            r = self.session.get(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)

    def get_user_info(self):
        """Ejecuta getUserInfo."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/getUserInfo")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }

        try:
            r = self.session.get(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)
    
    def get_setup_login_external(self):
        """Ejecuta getSetupLoginExternal."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/getSetupLoginExternal")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }
        
        try:
            r = self.session.post(
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }

        data = {
            'username': username,
            'password': password,
        }

        token_preview = (self.jwt_token or "")[:12]
        try:
            r = self.session.post(
                url,
                data=data,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )

            self.last_user_logon_body = r.text
            if r.status_code != 200:
                self.last_user_logon_ok = False
                return False, r.text

            try:
                payload = r.json()
            except Exception:
                payload = {}

            message = (payload.get("Message") or "").strip()
            data_payload = payload.get("Data") or {}
            user_valid = data_payload.get("userValid")
            is_authenticated = message == "Authenticated" or user_valid is True

            self.last_user_logon_ok = is_authenticated

            return is_authenticated, r.text
        except Exception as e:
            self.last_user_logon_ok = False
            self.last_user_logon_body = str(e)
            return False, str(e)
    
    def login(self, connection_name, username=None, password=None):
        """Ejecuta el flujo completo de login."""
        if not self.get_jwt_token():
            return False
        self.get_connection_name("login")
        self.validated_session()
        self.server_version()
        ok_list, list_body = self.display_dd_list_connections()
        if ok_list:
            detected_connection = self._get_first_connection_name(list_body)
            if detected_connection:
                connection_name = detected_connection
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
        self.is_saas()
        self.load_config()
        self.get_culture_information()
        self.get_language_datatable()
        self.is_saas()
        self.get_user_info()
        self.get_connection_name("main")
        return True

    def validated_session(self):
        """Ejecuta validatedSession."""
        url = urljoin(self.base_url, f"/{self.tenant}/xsm/Login/validatedSession")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Authorization': f'Bearer {self.jwt_token}',
            'Cache-Control': 'no-store',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/{self.tenant}/xsm/Login/',
        }

        try:
            r = self.session.post(
                url,
                headers=headers,
                cookies=self.session.cookies,
                timeout=10,
                verify=self.verify_ssl
            )
            return r.status_code == 200, r.text
        except Exception as e:
            return False, str(e)


class Xsales:
    _config = ConfigServer()

    def __init__(self, name: str) -> None:
        self.session = HTMLSession()
        self.base_url = "https://prd1.xsalesmobile.net"
        self.estado = True
        self.xsalesresponse = None
        self.xsalesresponse_json = None
        self.evento = None
        self.login_info = None
        self.virtual_path = None
        self.use_query_api = True
        self.usuari, self.credencial = self._config.CredencialesServer()
        self.name = name.upper()
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
                # Reusar la misma sesión autenticada
                self.session = login_client.session
                self.bearer_token = login_client.jwt_token
                self.session_cookie = login_client.session_cookie
                self.virtual_path = login_client.virtual_path
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
                return self.session_cookie

            self.login_info = {
                "ok": False,
                "tenant": self.name,
                "connection_name": connection_name,
                "jwt_token": None,
                "session_cookie": None,
                "virtual_path": login_client.virtual_path,
            }
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
            return None

    @property
    def get_login_info(self):
        """Retorna el resultado estructurado del login."""
        return self.login_info

    def _get_base_path(self):
        if self.virtual_path:
            return f"https://prd1.xsalesmobile.net{self.virtual_path}"
        return f"https://prd1.xsalesmobile.net/{self.name}/xsm"

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
        try:
            if not self.bearer_token:
                return False

            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Authorization': f'Bearer {self.bearer_token}',
            }

            base_path = self._get_base_path()
            # Validar sesión con Bearer token
            response = self.session.request(
                'post',
                f'{base_path}/Login/validatedSession',
                headers=head,
                cookies=self.cookies_
            )

            if response.status_code == 200:
                return True
            return False
        except Exception as e:
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
        return self._consultar_api(sql)

    def _refresh_login(self) -> bool:
        """Reautentica y refresca sesión/tokens."""
        try:
            connection_name = self.name + '_XSS_441_PRD'
            login_client = XsalesLoginClient(
                base_url=self.base_url,
                verify_ssl=False,
                tenant=self.name
            )

            if login_client.login(connection_name, self.usuari, self.credencial):
                # Reusar la misma sesión autenticada
                self.session = login_client.session
                self.bearer_token = login_client.jwt_token
                self.session_cookie = login_client.session_cookie
                self.virtual_path = login_client.virtual_path
                self.cookies_ = {'ASP.NET_SessionId': self.session_cookie}
                self.login_info = {
                    "ok": True,
                    "tenant": self.name,
                    "connection_name": connection_name,
                    "jwt_token": self.bearer_token,
                    "session_cookie": self.session_cookie,
                    "virtual_path": self.virtual_path,
                    "user_logon_ok": login_client.last_user_logon_ok,
                    "user_logon_body": login_client.last_user_logon_body,
                }
                return True
        except Exception as e:
            print(f"⚠ Error reautenticando: {e}")
        return False

    def _querybd_get_catalog(self):
        base_path = self._get_base_path()
        url = f"{base_path}/QueryBD/GetBDCombo"
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Cache-Control': 'no-store',
        }
        try:
            resp = self.session.get(url, headers=headers, cookies=self.cookies_)
            if resp.status_code != 200:
                return None
            try:
                data = resp.json()
            except Exception:
                content_type = resp.headers.get('Content-Type', '')
                preview = (resp.text or '').strip()[:200]
                print(f"⚠ QueryBD/GetBDCombo no JSON (Content-Type: {content_type})")
                print(f"⚠ Preview: {preview}")
                return None
            items = data.get('Data') if isinstance(data, dict) else None
            if isinstance(items, list) and items:
                item = items[0]
                return item.get('Catalog') or item.get('catalog') or item.get('value') or item.get('id')
        except Exception:
            return None
        return None

    def _consultar_api(self, sql):
        base_path = self._get_base_path()
        url = f"{base_path}/QueryBD/ExecuteConsult"
        catalog = self._querybd_get_catalog() or f"{self.name}_XSS_441_PRD"
        payload = {
            "Catalog": catalog,
            "Query": sql,
            "CultureName": "es-VE",
            "Decimals": ","
        }
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Cache-Control': 'no-store',
        }
        def _post():
            return self.session.post(url, headers=headers, json=payload, cookies=self.cookies_)

        def _refresh_and_retry():
            if not self._refresh_login():
                return None
            new_base = self._get_base_path()
            headers['Authorization'] = f'Bearer {self.bearer_token}'
            return self.session.post(
                f"{new_base}/QueryBD/ExecuteConsult",
                headers=headers,
                json=payload,
                cookies=self.cookies_
            )

        try:
            resp = _post()
            if resp.status_code != 200:
                self.xsalesresponse_json = None
                print(f"⚠ QueryBD/ExecuteConsult status: {resp.status_code}")
                if resp.status_code in (401, 403):
                    resp_retry = _refresh_and_retry()
                    if resp_retry is not None:
                        resp = resp_retry
                    else:
                        return resp
                else:
                    return resp

            try:
                self.xsalesresponse_json = resp.json()
            except Exception:
                self.xsalesresponse_json = None
                content_type = resp.headers.get('Content-Type', '')
                preview = (resp.text or '').strip()[:200]
                print(f"⚠ QueryBD/ExecuteConsult no JSON (Content-Type: {content_type})")
                print(f"⚠ Preview: {preview}")
                if content_type.startswith('text/html'):
                    try:
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        debug_file = f"REPORTES/SERVER/querybd_html_{self.name}_{timestamp}.html"
                        with open(debug_file, 'w', encoding='utf-8') as f:
                            f.write(resp.text)
                        print(f"⚠ HTML guardado en: {debug_file}")
                    except Exception:
                        pass
                # Reintentar una vez tras re-login si parece HTML
                if content_type.startswith('text/html'):
                    resp_retry = _refresh_and_retry()
                    if resp_retry is not None and resp_retry.status_code == 200:
                        try:
                            self.xsalesresponse_json = resp_retry.json()
                            return resp_retry
                        except Exception:
                            pass
            return resp
        except Exception as e:
            print(f"⚠ Error en QueryBD/ExecuteConsult: {e}")
            return None

    def Descargar_excel(self,sql):
        raise RuntimeError("Exportación por WebForms deshabilitada: usar API QueryBD")
