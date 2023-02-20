import pytest
import datetime
from plugins.xsales.src.modules.Server import ValidatorSql

revisionMDZ=[{'DZ_Regional': 'ECOAL_XSS_441_PRD', 
           'preventa': '20/02/2023',
           'despacho': '20/09/2022', 
           'HoraECUInicioStock': '19/2/2023 4:01:10 p. m.',      
           'HoraECUFinStock': '20/02/2023 10:40:16 a. m.', 
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
           },]
revisionMD=[]

""" 
{'DZ_Regional': 'PATRICIO_CEVALLOS_XSS_441_PRD', 'preventa': '19/09/2022', 'despacho': '20/09/2022', 'HoraECUInicioStock': '17/9/2022 1:47:31 p. m.',    
'HoraECUFinStock': '17/9/2022 2:03:59 p. m.', 'CUSTOMER_XSS': 10804, 'CUSTOMER_DELETE_0': 10804, 'CUSROUT_TOTAL': 1970, 'CUSROUTE_VISIT_TODAY': 398,     
'CUSSTATUS_VISIT_TODAY': 398, 'CUSSTATUS_TOTAL': 1970, 'PRODUCT': 9148, 'PROMOTION': 122, 'PROMOTIOND': 1281, 'PROMOTIONDP': 2786, 'GENERICO': 1} 
"""


@pytest.fixture
def validador() -> ValidatorSql :
    return ValidatorSql('REVICION_MADRUGADA' ,revisionMDZ)

def test_stock(validador):
    assert len(validador.validador[0])!=0
