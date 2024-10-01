#alicia albornos
from datetime import date, timedelta

ahora = date.today()
ayer = ahora -timedelta(days=2) if ahora.weekday() == 0  else ahora -timedelta(days=1)

class consultas:

    NDISTRIBUIDOR=None;
    __CONSULTA={}
 
    @classmethod
    def consulta(cls,value):
        __CONSULTA={
        'REVICION_MADRUGADA':consultas.revisionmadrugada,
        'DESC.DIURNOS':consultas.Descuentos_Demadrugada,
        'Total_Pedidos':consultas.totalPedidos,
        'VALIDAR_ClIENTE':consultas.cliente,
        'DESC.NOCTURNOS':consultas.Descuentos_Nocturno,
        }
        return __CONSULTA[value]

    @classmethod
    def Descuentos_Demadrugada(cls):

        distribuidor={

            'almabi' :    "When company.comName = 'Almabi' Then '360'",
            'alsodi' :    "When company.comName = 'Alsodi' Then '314'",
            'apronam':    "When company.comName = 'Apronam' Then '162'", 
            'cenacop':    "When company.comName = 'Cenacop' Then '325'",
            'dimmia' :    "When company.comName = 'Dimmia' Then '111'",
            'discarnicos' : "When company.comName = 'Discarnicos' Then '261'"       ,
            'disanahisa'  : "When company.comName = 'Disanahisa' Then '323'"       , 
            'disproalza'  : "When company.comName = 'Disproalza' Then '247'"        , 
            'disprovalles': "When company.comName = 'Disprovalles' Then '210'"      , 
            'disprolop'   : "When company.comName = 'Disprolop' Then '331'"         ,
            'ecoal'       : "When company.comName = 'Ecoal' Then '373'     "        ,
            'grampir'     : "When company.comName = 'Granpir' Then '234'"           ,
            'garvelproduct' :  "When company.comName = 'Garvel Product' Then '517'",
            'h_m'  :   "When company.comName = 'DISTMANA' Then '324'"               ,
            'judispro'  :   "When company.comName = 'Judispro' Then '239'   "       , 
            'madeli'   :    "When company.comName = 'Madeli' Then '128'    "        ,
            'patricio_cevallos'   :    "When company.comName = 'Patricio_Cevallos' Then '254'" ,
            'paul_florencia'   :    "When company.comName = 'Paul_Florencia' Then '168'"    ,
            'posso_cueva'   :    "When company.comName = 'Posso&Cueva' Then '253'"       , 
            'prooriente'   :    "When company.comName = 'Prooriente' Then '140' "       ,
            'dismag'  :   "When company.comName = 'Dismag' Then '215'",
            'pronaca' :  "When company.comName = 'Pronaca' Then '202'",
            'pronacnor': "When company.comName = 'Pronacnor' Then '303'", 
            'skandinar'   :   "When company.comName = 'Skandinar' Then '121'", 

            }
        
        distribuidor=distribuidor.get( cls.NDISTRIBUIDOR.lower())

        return f"""declare @inicio VARCHAR(255), @fin VARCHAR(255) 
                set @inicio = '{ayer} 00:00:00.000' set @fin = '{ayer} 23:59:00.000' 
                
                Select Top 1000000 LTRIM(RTRIM(Emp_Codigo)) AS Emp_Codigo,
                LTRIM(RTRIM(Id_Negociacion)) AS Id_Negociacion,
                LTRIM(RTRIM(Tipo)) AS Tipo,
                LTRIM(RTRIM(Codigo_Cliente)) AS Codigo_Cliente,
                LTRIM(RTRIM(Dia_Negociacion)) AS Dia_Negociacion,
                LTRIM(RTRIM(Mes_Negociacion)) AS Mes_Negociacion,
                LTRIM(RTRIM(Anio_Negociacion)) AS Anio_Negociacion,
                LTRIM(RTRIM(Cod_Vendedor)) AS Cod_Vendedor,
                LTRIM(RTRIM(Descuento_Negociado)) AS Descuento_Negociado,
                LTRIM(RTRIM(Descuento_Realizado)) AS Descuento_Realizado,
                LTRIM(RTRIM(Descuento_Status)) AS Descuento_Status,
                LTRIM(RTRIM(Desc_Prev_Pedido)) AS Desc_Prev_Pedido,
                LTRIM(RTRIM(Descuento_Procesado_XSales)) AS Descuento_Procesado_XSales,
                LTRIM(RTRIM(Pedido_Realizado)) AS Pedido_Realizado
                from ( select top 1000000 case 
                 {distribuidor}
                Else '#' end Emp_Codigo,                 
                Descu.didCode as Id_Negociacion, 
                Descu.Tipo,
                Descu.Cliente as Codigo_Cliente, 
                Day(Descu.Fecha) as Dia_Negociacion, 
                Month(Descu.Fecha) as Mes_Negociacion, 
                Year(Descu.Fecha) as Anio_Negociacion, 
                Ruta as Cod_Vendedor, Porcentaje as Descuento_Negociado,
                'Si' as Descuento_Realizado, Descu.Status as Descuento_Status,
                Case When Descu.Fecha< Ped2.Fecha Then'Si' Else'No' End as Desc_Prev_Pedido,Descu.Procesado as Descuento_Procesado_XSales,
                Case When len(Ped2.Fecha)> 4 Then'Si' Else'No' End as Pedido_Realizado From 
                (Select  D.didCode,D.cusCode CLIENTE,Convert(Varchar,D.didSystemDate,25) FECHA, D.rotCode RUTA,
                Replace(I.dlpMinDiscount1,',','.') PORCENTAJE, 
                Case When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%RECHAZ%' Then'Rechazado'
                When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"SI%' ESCAPE':' Then'Aprobado'
                When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"No%' ESCAPE':' Then'Rechazado'
                When D.ApvCode IS NULL Then'Aprobado'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:null%' ESCAPE':' Then'Pendiente'
                When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"EXCEPCION%' ESCAPE':' Then'Pendiente'
                When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) IS NULL Then'Pendiente'END As STATUS, 
                Case When D.didProcess='1' Then'Si' Else'No' End As PROCESADO, 
                case when apvcode is NULL then'RANGO' else'FUERA RANGO' end as TIPO From DiscountDetailUp D 
                Inner Join DiscountDetailProductUp I On D.didCode=I.didCode 
                Where D.didCanceled='0' And D.didProcess='1' And D.DidSystemDate Between @inicio And @fin And D.didCode Not In (Select T.didCode From demandTeamProductDiscount T 
                Inner Join Demand P On T.dmdCode=P.dmdCode Where P.dmdCancelOrder='1' And P.dmdProcess IS NULL) ) Descu 
                Left Join Company On 1=1 
                Left Join (Select  D.rotCode, D.cusCode,Max(D.dmdDate) as Fecha From Demand D Left Join DemandProduct DP On D.dmdCode= DP.dmdCode 
                Where D.dmdDate Between @inicio And @fin And docCode='ped' and D.rotCode in (Select rotCode From route Where chaCode='V01') And D.dmdCancelOrder= 0 And DP.proCode in (Select proCode From product Where cl4Code='IDGDD001') Group By D.rotCode, D.cusCode) Ped2 On Descu.cliente= Ped2.cuscode and Descu.Ruta= Ped2.rotcode 
                order by Descu.Ruta ) Todos"""

    @classmethod
    def Descuentos_Nocturno(cls)->str:
        return f""" SELECT TOP 100000 *  FROM (SELECT TOP 10000 D.DIDCODE, D.CUSCODE CLIENTE, CONVERT(VARCHAR,D.DIDSYSTEMDATE,25) FECHA,D.ROTCODE RUTA, REPLACE(I.dlpMinDiscount1,',','.') PORCENTAJE,
        CASE WHEN (SELECT A.APVRESPONSEDETAIL FROM APPROVAL A WHERE A.apvcode=D.apvcode) LIKE'%RECHAZ%' THEN'Rechazado' WHEN
        (SELECT A.APVRESPONSEDETAIL FROM APPROVAL A WHERE A.apvcode=D.apvcode) LIKE'%Respuesta"%:"SI%' ESCAPE':' THEN'Aprobado'WHEN
        (SELECT A.APVRESPONSEDETAIL FROM APPROVAL A WHERE A.apvcode=D.apvcode) LIKE'%Respuesta"%:"NO%' ESCAPE':' THEN'Rechazado'WHEN
        D.APVCODE IS NULL THEN'Aprobado'WHEN (SELECT A.APVRESPONSEDETAIL FROM APPROVAL A WHERE A.apvcode=D.apvcode) LIKE'%Respuesta"%:null%' ESCAPE':' THEN'Pendiente'WHEN 
        (SELECT A.APVRESPONSEDETAIL FROM APPROVAL A WHERE A.apvcode=D.apvcode) LIKE'%Respuesta"%:"EXCEPCION%' ESCAPE':' THEN'Pendiente'WHEN
        (SELECT A.APVRESPONSEDETAIL FROM APPROVAL A WHERE A.apvcode=D.apvcode) IS NULL THEN'Pendiente'END AS STATUS,
        CASE WHEN D.DIDPROCESS='1' THEN'Si' ELSE'No' END AS PROCESADO,D.APVCODE FROM DISCOUNTDETAILUP D INNER JOIN DISCOUNTDETAILPRODUCTUP I ON D.DIDCODE=I.DIDCODE WHERE D.DIDCANCELED='0' AND D.DIDSYSTEMDATE BETWEEN'{ahora} 00:00:00.000' AND'{ahora} 23:59:00.000' 
        AND D.DIDCODE NOT IN (SELECT T.DIDCODE FROM demandteamproductdiscount   T INNER JOIN DEMAND P ON T.DMDCODE=P.DMDCODE WHERE P.DMDCANCELORDER='1' AND P.DMDPROCESS IS NULL)) DESCU WHERE DESCU.STATUS NOT LIKE'%RECHAZ%' AND DESCU.PROCESADO='NO'
        """ 

    @classmethod
    def revisionmadrugada(cls)->str:
        "se revisa consultas en la madrugada"
        return """declare @customerxss int, @cusdelete int, @customerroute int, @cusst int, @customerstatus int, @customerroute1 int,@product int, @catalog int, @promotion int, @promotiond int, @promotiondp int, @genericou int, @genericog int, @genericoc int, @genericom int,@PreventastockD1  varchar(255),@DespachostockD1  varchar(255),@horainicioD01 varchar(255),@horafinD01 varchar(255),@horainicioD02 varchar(255),@horafinD02 varchar(255),@horainicioD04 varchar(255),@horafinD04 varchar(255),@horainicioD05 varchar(255),@horafinD05 varchar(255),@PreventastockD2 varchar(255),@DespachostockD2  varchar(255),@PreventastockD4 varchar(255),@DespachostockD4  varchar(255),@PreventastockD5 varchar(255), @DespachostockD5  varchar(255)select @customerxss= (select count(*) from customer)select @cusdelete=(select count(*) from customer where _Deleted='0' )select @customerroute=(select count(distinct cuscode) from customerroute where ctrvisittoday='1' and rotcode not like'%t%')select @customerroute1=(select count(distinct cuscode) from customerroute)select @cusst=(select count(*) from customerstatus where cuscode in(select cusCode from customerroute where ctrVisitToday='1' and rotcode not like'%t%'))select @customerstatus=(select count(*) from customerstatus WHERE CUSCODE IN (SELECT CUSCODE FROM CUSTOMERROUTE))select @product=(select count(*) from product where _Deleted='0')Select @catalog=(select count(*) From CatalogDetail)select @promotion=(select count(*) from promotion)select @promotiond=(select count(*) from promotiondetail)select @promotiondp=(select count(*) from promotiondetailproduct)select @genericou=(select count(*) from customerstatus where cusCode like'%199998%')select @genericog=(select count(*) from customerstatus where cusCode like'%299998%')select @genericoc=(select count(*) from customerstatus where cusCode like'%488888%')select @genericom=(select count(*) from customerstatus where cusCode like'%588888%')select @horainicioD01=(SELECT max(Trndate) FROM[TRANSACTION] WHERE TRNSCRIPTS LIKE'%CALCULATE%' and  TRNSCRIPTS  like'%D01%')select  @horafinD01=(SELECT max(trnLastDate) FROM[TRANSACTION]WHERE TRNSCRIPTS LIKE'%CALCULATE%'and TRNSCRIPTS like'%D01%')select @horainicioD02=(SELECT max(Trndate) FROM[TRANSACTION] WHERE TRNSCRIPTS LIKE'%CALCULATE%' and TRNSCRIPTS like'%D02%')select @horafinD02=(SELECT max(trnLastDate) FROM[TRANSACTION]WHERE TRNSCRIPTS LIKE'%CALCULATE%'and TRNSCRIPTS like'%D02%')select @horainicioD04=(SELECT max(Trndate) FROM[TRANSACTION] WHERE TRNSCRIPTS LIKE'%CALCULATE%' and TRNSCRIPTS like'%D04%')select @horafinD04=(SELECT max(trnLastDate) FROM[TRANSACTION]WHERE TRNSCRIPTS LIKE'%CALCULATE%'and TRNSCRIPTS like'%D04%')select @horainicioD05=(SELECT max(Trndate) FROM[TRANSACTION] WHERE TRNSCRIPTS LIKE'%CALCULATE%' and TRNSCRIPTS like'%D05%')select @horafinD05=(SELECT max(trnLastDate) FROM[TRANSACTION]WHERE TRNSCRIPTS LIKE'%CALCULATE%'and TRNSCRIPTS like'%D05%')select @PreventastockD1= (select  distinct top 1 convert(varchar,aptTransactionDate,103) from areaproduct where areCode='D01')select @DespachostockD1= (select  distinct top 1 convert(varchar,aptServerLastUpdate,103) from areaproduct where areCode='D01')select @PreventastockD2= (select  distinct top 1 convert(varchar,aptTransactionDate,103) from areaproduct where areCode='D02')select @DespachostockD2= (select  distinct top 1 convert(varchar,aptServerLastUpdate,103) from areaproduct where areCode='D02')select @PreventastockD4= (select  distinct top 1 convert(varchar,aptTransactionDate,103) from areaproduct where areCode='D04')select @DespachostockD4= (select  distinct top 1 convert(varchar,aptServerLastUpdate,103) from areaproduct where areCode='D04')select @PreventastockD5= (select  distinct top 1 convert(varchar,aptTransactionDate,103) from areaproduct where areCode='D05')select @DespachostockD5= (select  distinct top 1 convert(varchar,aptServerLastUpdate,103) from areaproduct where areCode='D05')select @PreventastockD1 as preventaQuito, @DespachostockD1 as DespachoQuito, dateadd (hh,-1,@horainicioD01) as INICIOHoraUIO,@horafinD01 as FINHoraUIO,@PreventastockD2 as preventaGYE, @DespachostockD2 as DespachoGYE,dateadd (hh,-1,@horainicioD02) as INICIOHORAGYE,@horafinD02 as FINHORAGYE,@PreventastockD4 as preventaCuenca, @DespachostockD4 as DespachoCuenca, dateadd (hh,-1,@horainicioD04)   as INICIOHORACUENCA,@horafinD04 as FINHORACUENCA,@PreventastockD5 as preventaMontecristi, @DespachostockD5 as DespachoMontecristi,dateadd (hh,-1,@horainicioD05) as INICIOHORAMONTEC,@horafinD05 as FINHORAMONTEC,@customerxss as CUSTOMER_XSS, @cusdelete as CUSTOMER_DELETE_0,@customerroute1 as CUSROUT_TOTAL,@customerroute as CUSROUTE_VISIT_TODAY,@cusst as CUSSTATUS_VISIT_TODAY,@customerstatus as CUSSTATUS_TOTAL,@product as PRODUCT, @catalog as CATALOG, @promotion as PROMOTION,@promotiond as PROMOTIOND, @promotiondp as PROMOTIONDP, @genericou as GENUIO, @genericog as GENGYE, @genericoc as GENCUE, @genericom as GENMON""" if cls.NDISTRIBUIDOR =='PRONACA' else """declare @preventa varchar(25), @despacho varchar(25), @customerxss int, @cusdelete int, @customerroute int, @cusst int, @customerstatus int, @customerroute1 int, @product int, @promotion int, @promotiond int, @promotiondp int, @generico int, @horainicio datetime,@horafin datetime select @preventa= (select top 1 convert(varchar,aptTransactionDate,103)  from areaproduct group by aptTransactionDate) select @despacho= (select top 1 convert(varchar,aptServerLastUpdate,103)  from areaproduct  group by aptServerLastUpdate) select @customerxss= (select count(*) from customer)  select @cusdelete=(select count(*) from customer where _Deleted='0' ) select @customerroute=(select count(distinct cuscode) from customerroute  where ctrvisittoday='1' and rotcode not like'%t%') select @customerstatus=(select count(*) from customerstatus WHERE CUSCODE IN (SELECT CUSCODE FROM CUSTOMERROUTE))  select @cusst=(select count(*) from customerstatus where cuscode in(select cusCode from customerroute where ctrVisitToday='1' and rotcode not like'%t%')) select @customerroute1=(select count(distinct cuscode) from customerroute) select @product=(select count(*) from product where _Deleted='0') select @promotion=(select count(*) from promotion) select @promotiond=(select count(*) from promotiondetail) select @promotiondp=(select count(*) from promotiondetailproduct) select @generico=(select count(*) from customer where cusCode like'%099999999%' or cuscode like'%3030000074%' and cuscode in ( select cuscode from customerstatus ))  select @horainicio=(SELECT max(Trndate) FROM [TRANSACTION] WHERE TRNSCRIPTS LIKE'%CALCULATE%') select  @horafin=(SELECT max(trnLastDate) FROM[TRANSACTION] WHERE TRNSCRIPTS LIKE'%CALCULATE%') select  DB_NAME() as  DZ_Regional,  @preventa as preventa, @despacho as despacho, dateadd(hh,-1,@horainicio) as HoraECUInicioStock,dateadd(hh,-1,@horafin) as HoraECUFinStock, @customerxss as CUSTOMER_XSS, @cusdelete as CUSTOMER_DELETE_0,  @customerroute1 as CUSROUT_TOTAL,@customerroute as CUSROUTE_VISIT_TODAY,@cusst as CUSSTATUS_VISIT_TODAY, @customerstatus as CUSSTATUS_TOTAL, @product as PRODUCT, @promotion as PROMOTION, @promotiond as PROMOTIOND, @promotiondp as PROMOTIONDP, @generico as GENERICO"""

    @classmethod
    def totalPedidos(cls)->str:
         return f""" declare @dia integer, @mes integer, @anio integer, @tr int, @er int, @soap int, @exi int, @ex int, @pr int, @npr int, @erp int,@total int set @dia={str(ahora)[8:11]} ;set @mes={str(ahora)[5:7]};set @anio={str(ahora)[:4]} select top(100) @tr= (select count(*) from extendedtablevalue1 where exttablename='demand' and exvpkcode1 in ( select dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdcancelorder=0 ) and exvCharValue like'%TRANSITO%' and exffieldname='x_processMessage') select @er= (select count(*) from extendedtablevalue1 where exttablename='demand' and exvpkcode1 in ( select dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdcancelorder=0 ) and exvCharValue like'%ERROR%' and exffieldname='x_processMessage') select @soap= (select count(*) from extendedtablevalue1 where exttablename='demand' and exvpkcode1 in ( select dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdcancelorder=0 ) and exvCharValue like'%soap%' and exffieldname='x_processMessage') select @exi= (select count(*) from extendedtablevalue1 where exttablename='demand' and exvpkcode1 in ( select dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdcancelorder=0 ) and exvCharValue like'%existente%' and exffieldname='x_processMessage') select @ex=(select count(*) dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdcancelorder=0 and dmdcode NOT in (select exvpkcode1 from extendedtablevalue1 where exttablename='demand' and exffieldname='x_processMessage')) select @pr=(select count(*) dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdCancelOrder='0' and dmdprocess='1') select @npr=(select count(*) dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdCancelOrder='0' and dmdprocess='0') select @total=(select count(*) dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdCancelOrder='0') select @erp= (select count(*) from extendedtablevalue1 where exttablename='demand' and exvpkcode1 in ( select dmdcode from demand where day(dmddate)= @dia and month(dmddate)= @mes and year(dmddate)= @anio and dmdcancelorder=0 ) and (exvCharValue like'%EXITO%' and exffieldname='x_processMessage' OR exvCharValue like'%-0%' and exffieldname='x_processMessage')) select DB_NAME() as  DZ_Regional, @tr as DMD_TRANSITO, @er as DMD_ERROR, @soap as DMD_ERRSOAP, @exi as DMD_EXISTENTE, @ex as DMD_EXTENDIDAS, @pr as DMD_PROCESADOS,  @npr as DMD_NOPROCESADOS, @erp as ERP_EXITO, @total as DMD_TOTAL """

    @classmethod
    def  cliente(cls,valor)->str:
        return f"select top 1000 cuscode,cusTaxID1,cusName,cusBusinessName from customer where custaxid1 like '%{valor}%'"