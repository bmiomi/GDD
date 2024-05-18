from unittest import TestCase,main
from plugins.xsales.src.modules.Server import ValidatorSql

preventa='03/12/2023'
despacho='04/12/2023'

revisionMDZ=[
          
          {'DZ_Regional': 'ECOAL_XSS_441_PRD', 
           'preventa': preventa,
           'despacho': despacho, 
           'HoraECUInicioStock': '02/12/2023 4:01:10 p. m.',      
           'HoraECUFinStock': '02/12/2023 10:40:16 a. m.', 
           'CUSTOMER_XSS': "21930", 
           'CUSTOMER_DELETE_0': "21930", 
           'CUSROUT_TOTAL': "2742", 
           'CUSROUTE_VISIT_TODAY':"480", 
           'CUSSTATUS_VISIT_TODAY': "480", 
           'CUSSTATUS_TOTAL': "2741", 
           'PRODUCT': "9148", 
           'PROMOTION': "122",
            'PROMOTIOND': "1281", 
           'PROMOTIONDP': "2786",         
           'GENERICO': "0"
           },
           { 'DZ_Regional': 'PATRICIO_CEVALLOS_XSS_441_PRD', 
             'preventa': preventa,
             'despacho': despacho,
             'HoraECUInicioStock': '17/9/2022 1:47:31 p. m.',    
             'HoraECUFinStock': '17/9/2022 2:03:59 p. m.', 
             'CUSTOMER_XSS': 10804, 
             'CUSTOMER_DELETE_0': 10804, 
             'CUSROUT_TOTAL': 1970, 
             'CUSROUTE_VISIT_TODAY': 398,     
             'CUSSTATUS_VISIT_TODAY': 398, 
             'CUSSTATUS_TOTAL': 1970, 
             'PRODUCT': 9148, 
             'PROMOTION': 122, 
             'PROMOTIOND': 1281, 
             'PROMOTIONDP': 2786, 
             'GENERICO': 1
             } ,
            { 'preventaQuito': preventa, 
              'DespachoQuito': despacho, 
              'INICIOHoraUIO': '2/12/2023 7:00:00 p. m.', 
              'FINHoraUIO': 'Dec 2 2023 10:20PM',
              'preventaGYE': preventa, 
              'DespachoGYE': despacho, 
              'INICIOHORAGYE': '2/12/2023 8:54:00 p. m.',
              'FINHORAGYE': 'Dec 2 2023 11:09PM', 
              'preventaCuenca': preventa,
              'DespachoCuenca': despacho, 
              'INICIOHORACUENCA': '2/12/2023 4:11:00 p. m.', 
              'FINHORACUENCA': 'Dec 2 2023 10:12PM', 
              'preventaMontecristi': preventa, 
              'DespachoMontecristi': preventa, 
              'INICIOHORAMONTEC': '1/12/2023 8:42:00 p. m.', 
              'FINHORAMONTEC': 'Dec 1 2023 11:33PM', 'CUSTOMER_XSS': 42478,
              'CUSTOMER_DELETE_0': 42476, 
              'CUSROUT_TOTAL': 12061, 
              'CUSROUTE_VISIT_TODAY': 0, 
              'CUSSTATUS_VISIT_TODAY': 0, 
              'CUSSTATUS_TOTAL': 13345, 
              'PRODUCT': 10406, 
              'CATALOG': 57399, 
              'PROMOTION': 103, 
              'PROMOTIOND': 8333, 
              'PROMOTIONDP': 18758,
              'GENUIO': 2, 
              'GENGYE': 2, 
              'GENCUE': 1,
              'GENMON': 1}
           ]


class Test_Validator(TestCase):

  def setUp(self) -> None:
   self.validacion=ValidatorSql('REVICION_MADRUGADA' ,revisionMDZ)

  def test_validar_matutina_error(self):
    with self.assertRaises( ValueError) as error:
      self.validacion.vmatutina()
    self.assertIn( '[ERROR] ',error.exception.args[0],'El string no tiene coincidencias')


  def test_stock(self,validador):
    assert len(self.validacion.validador)!=0


if __name__=="__main__":
  main()