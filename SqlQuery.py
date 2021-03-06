
import sys
import cx_Oracle, datetime
import con



def firstQuery():
    sql = """select DOCCLIENTES.DCCLIENTE, CLIENTES.CNOME, CLIENTES.CGRUPO, GRUPOS.GNOME, DOCCLIENTES.DCDOCUMENTO, DOCCLIENTES.DCDATAEMISSAO, DOCCLIENTES.DCDATAVENCIMENTO,
        DOCCLIENTES.DCVALOR, DOCCLIENTES.DCSEMANA
        from 
        DOCCLIENTES
        inner join CLIENTES on CLIENTES.CCODIGO = DOCCLIENTES.DCCLIENTE
        inner join GRUPOS on GRUPOS.GCODIGO = CLIENTES.CGRUPO
        where
        DOCCLIENTES.DCDULTPAGAMENTO is null
        order by
        DOCCLIENTES.DCDATAVENCIMENTO desc"""
    connection = cx_Oracle.connect(con.__user,con.__password,con.__HostService)
    cursor = connection.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    connection.close()
    return result

def is_number(s):
    try:
        float(s)
        if s == "":
            return False
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def isPago(dcdocumento):
    b = False
    if is_number(dcdocumento):
        sql= """ SELECT DCDULTPAGAMENTO FROM DOCCLIENTES where dcdocumento = """+dcdocumento
        connection = cx_Oracle.connect(con.__user,con.__password,con.__HostService)
        cursor = connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        for a in result:
            if a[0] is None:
                b = False
            else:
                b = True
            print(str(datetime.datetime.now())+" Retorno metodo isPago:"+str(b)+", documento:"+dcdocumento+"  "+str(a[0]))
        return b
        connection.close()
    return False

def desbloqueio(codigo):
    sql = """ update dradba.clientes set cbloqueadosn = 'N' where ccodigo = """+codigo
    connection = cx_Oracle.connect(con.__duser,con.__dpassword,con.__dHostService)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()