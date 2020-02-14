#!/usr/bin/python3
import cx_Oracle
import shutil
import sys, os , copy
import csv
import datetime
import SqlQuery,SendEmail




#___diretorioSem = "semana-"+datetime.datetime.now().strftime("%Y%V")+'/'
___diretorioSem = "semana-"+datetime.datetime.now().strftime("%Y")+str(int(datetime.datetime.now().strftime("%V")))+'/'
___diretorioSemList = "semana-"+datetime.datetime.now().strftime("%Y")+str(int(datetime.datetime.now().strftime("%V"))+1)+'/'
___arquivoListSeman = "ListSemana"+str(int(datetime.datetime.now().strftime("%V"))+1)+".csv"
___arquivoListSemanL = "ListSemana"+str(int(datetime.datetime.now().strftime("%V")))+".csv"
___arquivoDesbloqueioSemana = "DesbloqueioSemana"+str(datetime.datetime.now().strftime("%Y-%m-%d"))+".csv"
def main(argv):
        if (argv[1] == 'firstList'):
                firstList()
        elif (argv[1] == 'consultPag'):
                consultPag()
        elif (argv[1] == 'sendFinal'):
                sendFinal()
        elif (argv[1] == 'consultPagSabado'):
                consultPagSabado()
def firstList(): 
        result = SqlQuery.firstQuery()
        if not os.path.exists(___diretorioSemList):
                os.makedirs(___diretorioSemList)
        if not os.path.isfile(___diretorioSemList+___arquivoListSeman):
                print(str(datetime.datetime.now())+" Gerando lista de documentos em abertos da "+___diretorioSemList)
                with open(___diretorioSemList+___arquivoListSeman,"w") as f:
                        c = csv.writer(f,delimiter =';',quotechar =',',quoting=csv.QUOTE_MINIMAL)
                        c.writerow(["DCCLIENTE","CNOME","CGRUPO","GNOME","DCDOCUMENTO","DCDATAEMISSAO","DCDATAVENCIMENTO","DCVALOR","DCSEMANA","ATRASO",str(datetime.datetime.now().strftime("%Y-%m-%d"))])
                        for DCCLIENTE,CNOME,CGRUPO,GNOME,DCDOCUMENTO,DCDATAEMISSAO,DCDATAVENCIMENTO,DCVALOR,DCSEMANA in result:
                                if(((datetime.datetime.now()-DCDATAVENCIMENTO).days >= 1) and ((datetime.datetime.now()-DCDATAVENCIMENTO).days <= 30) and (DCVALOR > 0) ):
                                        c.writerow((DCCLIENTE,CNOME.strip(' '),CGRUPO,GNOME.strip(' '),DCDOCUMENTO,DCDATAEMISSAO.strftime("%Y-%m-%d"),DCDATAVENCIMENTO.strftime("%Y-%m-%d"),DCVALOR,DCSEMANA,str((datetime.datetime.now()-DCDATAVENCIMENTO).days)+" Dias"))
                shutil.copyfile((___diretorioSemList+___arquivoListSeman),(___diretorioSemList+___arquivoListSeman+".bkp"))

                SendEmail.sendFirtList(___diretorioSemList,___arquivoListSeman)
        else:
                print(str(datetime.datetime.now())+" A Lista da "+___diretorioSemList+" ja existe!")

def consultPag():
        if not os.path.exists(___diretorioSem):
                print(str(datetime.datetime.now())+" O direitorio da semana nem existe, "+___diretorioSem+" rodar metodo firstList")
        elif os.path.isfile(___diretorioSem+___arquivoDesbloqueioSemana):
                print(str(datetime.datetime.now())+" Arquivo de DesbloqueioSemana"+str(datetime.datetime.now().strftime("%Y-%m-%d"))+".csv ja foi gerado.")
        elif not os.path.isfile(___diretorioSem+___arquivoListSemanL):
                print(str(datetime.datetime.now())+" Arquivo de Lista da Semana/Dia, nao gerado ou nao encontrado!  "+___diretorioSem+___arquivoListSeman)
        else:
                print(str(datetime.datetime.now())+" Gerando consulta dos documentos do dia")
                fl = open(___diretorioSem+___arquivoDesbloqueioSemana,"w")
                c = csv.writer(fl, delimiter=';',quotechar=',',quoting=csv.QUOTE_MINIMAL)
                c.writerow([str(datetime.datetime.now().strftime("%Y-%m-%d"))])
                c.writerow(["CCLIENTE","CNOME","CGRUPO","GNOME"])    
                f =  open(___diretorioSem+___arquivoListSemanL)
                reader = csv.reader(f, delimiter = ';', quotechar= ',',quoting=csv.QUOTE_MINIMAL)
                listDocs = list(reader)
                f.close()
                f =  open(___diretorioSem+___arquivoListSemanL)
                reader2 = csv.reader(f, delimiter = ';', quotechar= ',',quoting=csv.QUOTE_MINIMAL)
                for idx,value in enumerate(reader2):
                        if SqlQuery.isPago(value[4]):
                                c.writerow((value[0],value[1],value[2],value[3]))
                                listDocs.remove(value)
                fl.close()
                f.close()
                with open(___diretorioSem+___arquivoListSemanL,'w') as f:
                        wr = csv.writer(f, delimiter = ';', quotechar = ',', quoting=csv.QUOTE_MINIMAL)
                        for row in listDocs:
                                wr.writerow(row)
                        f.close()
                desCodigo()
                print(str(datetime.datetime.now())+" Consulta Finalizada")
                print(str(datetime.datetime.now())+" Enviando email da consulta")
                SendEmail.sendConsPag(___diretorioSem,___arquivoDesbloqueioSemana)
                print(str(datetime.datetime.now())+" Email enviado")

def consultPagSabado():
        if not os.path.exists(___diretorioSemList):
                print(str(datetime.datetime.now())+" O direitorio da semana nem existe, "+___diretorioSem+" rodar metodo firstList")
        elif os.path.isfile(___diretorioSemList+___arquivoDesbloqueioSemana):
                print(str(datetime.datetime.now())+" Arquivo de DesbloqueioSemana"+str(datetime.datetime.now().strftime("%Y-%m-%d"))+".csv ja foi gerado.")
        elif not os.path.isfile(___diretorioSemList+___arquivoListSeman):
                print(str(datetime.datetime.now())+" Arquivo de Lista da Semana/Dia, nao gerado ou nao encontrado!  "+___diretorioSemList+___arquivoListSeman)
        else:
                print(str(datetime.datetime.now())+" Gerando consulta dos documentos do dia")
                fl = open(___diretorioSemList+___arquivoDesbloqueioSemana,"w")
                c = csv.writer(fl, delimiter=';',quotechar=',',quoting=csv.QUOTE_MINIMAL)
                c.writerow([str(datetime.datetime.now().strftime("%Y-%m-%d"))])
                c.writerow(["CCLIENTE","CNOME","CGRUPO","GNOME"])    
                f =  open(___diretorioSemList+___arquivoListSeman)
                reader = csv.reader(f, delimiter = ';', quotechar= ',',quoting=csv.QUOTE_MINIMAL)
                listDocs = list(reader)
                f.close()
                f =  open(___diretorioSemList+___arquivoListSeman)
                reader2 = csv.reader(f, delimiter = ';', quotechar= ',',quoting=csv.QUOTE_MINIMAL)
                for idx,value in enumerate(reader2):
                        if SqlQuery.isPago(value[4]):
                                c.writerow((value[0],value[1],value[2],value[3]))
                                listDocs.remove(value)
                fl.close()
                f.close()
                with open(___diretorioSemList+___arquivoListSeman,'w') as f:
                        wr = csv.writer(f, delimiter = ';', quotechar = ',', quoting=csv.QUOTE_MINIMAL)
                        for row in listDocs:
                                wr.writerow(row)
                        f.close()
                desCodigoSabado()
                print(str(datetime.datetime.now())+" Consulta Finalizada")
                print(str(datetime.datetime.now())+" Enviando email da consulta")
                SendEmail.sendConsPag(___diretorioSemList,___arquivoDesbloqueioSemana)
                print(str(datetime.datetime.now())+" Email enviado")

def sendFinal():
        print(str(datetime.datetime.now())+" Enviando a lista final de documentos em aberto") 
        SendEmail.sendListFinal(___diretorioSem,___arquivoListSemanL) 
        print(str(datetime.datetime.now())+"Email enviado")
def existCodigo(codigo):
        csvList = open(___diretorioSem+___arquivoListSemanL,'r')
        lista = csv.reader(csvList,delimiter = ';', quotechar = ',', quoting=csv.QUOTE_MINIMAL)
        for row in lista:
                if row[0] == codigo:
                        csvList.close()
                        return True
        return False
def desCodigo():
        arq = open(___diretorioSem+___arquivoDesbloqueioSemana,"r")
        desbl = csv.reader(arq,delimiter = ';', quotechar = ',', quoting=csv.QUOTE_MINIMAL)
        for row in desbl:
                if not existCodigo(row[0]):
                        if SqlQuery.is_number(row[0]):
                                print(datetime.datetime.now(),"Fazendo desbloqueio do codigo",row[0])
                                result = SqlQuery.desbloqueio(row[0])
                                print(result)
def existCodigoSabado(codigo):
        csvList = open(___diretorioSemList+___arquivoListSeman,'r')
        lista = csv.reader(csvList,delimiter = ';', quotechar = ',', quoting=csv.QUOTE_MINIMAL)
        for row in lista:
                if row[0] == codigo:
                        csvList.close()
                        return True
        return False

def desCodigoSabado():
        arq = open(___diretorioSemList+___arquivoDesbloqueioSemana,'r')
        desbl = csv.reader(arq,delimiter = ';', quotechar = ',', quoting=csv.QUOTE_MINIMAL)
        for row in desbl:
                if not existCodigoSabado(row[0]):
                        if SqlQuery.is_number(row[0]):
                                print(datetime.datetime.now(),"Fazendo desbloqueio do codigo",row[0])
                                result = SqlQuery.desbloqueio(row[0])
                                print(result)
                
                

main(sys.argv)
