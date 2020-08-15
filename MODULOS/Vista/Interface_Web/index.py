from flask import Flask,request
from flask.templating import render_template
from flask_json import FlaskJSON, as_json
import  datetime
from MODULOS.Modelo.FtpXsales import FtpXsales

class ErrorB(Exception):

    def __str__(self):
        return 'el error es que es igua la 3 el valor proporcionado'

app=Flask(__name__)
FlaskJSON(app)

def valor():
    if  datetime.date.strftime(datetime.datetime.now(),'%A') != 'Saturday': 
         return [
        {
        'N':'TECNICO 3-AM',
        'ListaDz':['PRONACA','CENACOP','DAPROMACH','DISPROALZA','MADELI',
        'PAULFLORENCIA','POSSOCUEVA','DISPROVALLE','ORIENTAL']
        },
        {
        'N':'TECNICO(1) 4-AM',
        'ListaDz':
        ['JUDISPRO','ALMABI','PRONAIM','GRAMPIR',
        'GARVELPRODUCT','DISANAHISA','ALSODI'],
        'rutas':'100'
        },
        {
        'N':'TECNICO(2) 4-AM',
        'ListaDz':['DIMMIA','SKANDINAR','PRONACNOR','APRONAM',
        'DISCARNICO','ECOAL','H_M','PATRICIOCEVALLOS']
        }
    ]
    return [
        {
        'N':'TECNICO 3-AM',
        'ListaDz':['PRONACA','CENACOP','DAPROMACH','DISPROALZA','MADELI',
        'PAULFLORENCIA','POSSOCUEVA','DISPROVALLE','ORIENTAL','APRONAM','H_M','DISCARNICOS']
        },

        {
        'N':'TECNICO 4-AM',
        'ListaDz':
        ['JUDISPRO','ALMABI','PRONAIM','GRAMPIR',
        'GARVELPRODUCT','DISANAHISA','ALSODI','DIMMIA','SKANDINAR','PRONACNOR','ECOAL','PATRICIOCEVALLOS']
        }
    ]

@app.route('/')
def hello_world():
    return render_template('index.html',valor=valor())

@app.route('/rutas',methods=["POST"])
@as_json
def rutas():
    try:
        Ob=FtpXsales()
        response=request.get_json()['name']
        Ob.configuracion.setterUSER=Ob.configuracion.config.get(response,'USER')
        Ob.configuracion.settPASS=Ob.configuracion.config.get(response,'PASS')
        Ob.Login()
        Ob.folderDownloadXsales()
        if len(Ob._rutas)==0:
            raise ErrorB ('base no creadas')
        else:
            for i in Ob._rutas:
                Ob.DESCARGA(i)
                Ob.descomprimir(i)
                Ob.procesarInfo(i)
            return dict({"status":'OK',"message": "Los Modulos para GDD se encuentran Activos."})
    except ErrorB as e:
        return dict({"status":"Info","message":'Las Base de las rutas no se encuentran disponibles por el momento.'})
    except Exception as e:
        return dict({"status":"ERROR","message":'Error existen rutas con modulos bloqueados'})
    finally:
        print('Fin de proceso.')
