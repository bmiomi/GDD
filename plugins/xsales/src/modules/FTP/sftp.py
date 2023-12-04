from paramiko import Transport,SFTP

from datetime import date, datetime, timedelta

class SFTP_(Transport):

    sftp = None
    files=[]

    def __init__(self):
        super().__init__(('200.31.27.104', 22))

    def acceso(self, *arg):
        self.connect(username=arg[1], password=arg[2])
        self.sftp = SFTP.from_transport(self)

    def change_dir(self, dir):
        self.sftp.chdir(dir)

    def list_dir(self,*args):
        return self.sftp.listdir(*args)

    def mostrarar_achivos(self,excluide=None):

        self.change_dir('PROD')
        
        for i in [i for i in self.list_dir() if  i not in excluide]:
            path=self.sftp.getcwd()
            file_date=self.sftp.stat(path+'/'+i).st_mtime
            last_modified_ts = datetime.fromtimestamp(file_date)
            last_modified_date = datetime.fromtimestamp(file_date).date() 
            last_modified_time = datetime.fromtimestamp(file_date).time()
            day=date.today()-timedelta(days=1)
            if last_modified_date != day and last_modified_time>=datetime.strptime("22:30:00","%H:%M:%S").time()  :
                self.files.append({'file':i,'fecha':last_modified_ts.strftime("%Y-%m-%d %H:%M:%S")})
               