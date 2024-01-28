
from requests import Session

from core.Interfaces.Iplugins import IPluging



class Plugin(IPluging):

    @property
    def nombre(self):
        return 'Bzhelp'

    def execute(self,question,consola):

        objeto={
                   "correo": "bryan.mino@baeztrosoft.com",
                   "pass": "e5915fef0a018a60398ac730406c81f57e1deef5e92779610e223fdf91a217a1",
                   "tipo": 2
                }

        request:Session= Session()

        response=request.get('https://bzhelp.com.ec/Home')

        request.post('https://bzhelp.com.ec/Home',data)




        print(f'response {response} cookie {response.cookies}')