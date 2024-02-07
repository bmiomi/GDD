from ftplib import FTP_TLS
import ssl


class ImplicitFTPTLS(FTP_TLS):
    files=[]

    """FTP_TLS subclass that automatically wraps sockets in SSL to support implicit FTPS."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is ssl wrapped."""
        if value is not None and not isinstance(value, ssl.SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value

    def change_dir(self, dir: str):
        return self.cwd(dir)

    def list_dir(self, *args):
        return self.dir(*args)

    def acceso(self, *args):
        self.connect(host=args[0], port=990, timeout=18000)
        self.login(args[1], args[2])

    def mostrarar_achivos(self, excluide=None):
        
        from dateutil import parser,tz
        f=[] 
        self.change_dir('/COMUNES')
        self.list_dir(f.append)
        for line in f:
            tokens = line.split(maxsplit = 9)
            time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
            time = parser.parse(time_str,tzinfos =tz.gettz('Quito'))
            latest_name = tokens[8]
            latest_time = time
            print(f"file: {latest_name} fecha {latest_time}" )