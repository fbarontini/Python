"""
Robô de consulta SIGEF.

Método de consulta: 
    1- Abrir o arquivo de nomes e gerar as URLs
    2- Abrir a pagina de consulta do SIGEF e capturar a tabela de imoveis
            Essa etapa pode acontecer ou não, tendo mais de uma página para
            consultar em alguns nomes (ex.: José)
    
"""
import csv
import requests
import time
import logging
import pypyodbc as db
from bs4 import BeautifulSoup

LOCAL_ARQUIVO = r"SIGEF_lista_nomes.txt" # Lista com todos os nomes possiveis no Brasil
LISTA_URL = []
MAX_PAGINA = 1

#Crio um arquivo de LOG para ver os inserts que deram erro.
LOG_FORMAT = "%(levelname)s %(asctime)s;%(message)s"
logging.basicConfig(filename = "SIGEF.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT)
LOGGER = logging.getLogger()


def sleep(value = 1.0):
    time.sleep(value)


def tratarString(linha):

    linha = linha.replace("'","")
    linha = linha.replace("°","")
    
    return linha


#Crio a conexão com o DW para armazenar os dados na tabela
def conectaDW():
    try:
        con = db.connect(
            Trusted_Connection='yes' #elimina validação de usuario e usa conexão de rede
            ,driver = '{SQL Server}'
            ,server='SQLServerLink'
            ,database='DatabaseName'
        )
        return con
    except:
        print("Erro na conexão com o banco de dados!")
        sleep(180)
        LOGGER.info("Erro na conexao com o banco de dados.")
        conectaDW()


def getUrlFromSql():
    #MONTAR ESSA QUERY
    connection = conectaDW()
    cursor = connection.cursor()
    query = "select top 1 dsURL from _corporate.TB_SIGEF_INICIAL"
    cursor.execute(query)
    results = list(cursor.fetchall())
    rowarray_list = []

    for row in results:
        rowarray_list.append(row[0])
    cursor.close()
    connection.close()

    return rowarray_list


def insereSQLinicial(lista):
    
    try:
        connection = conectaDW()
        sql  = "insert into table_identity values("
        sql += "'{}','{}','{}','{}','{}','{}')".format(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5])
        
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.commit()
        cursor.close()
        connection.close()
    
    except:
        print("Erro no insert dos dados no banco de dados")
        LOGGER.warning(sql)
        sleep()

    return


def pegaDadosPaginaInicial(soup):
    
    lista_de_tds = []
    lista_de_registros = []
    lista_de_urls = []
    lista_de_linhas = soup.find('tbody').find_all('tr')
    idxRegistro = 1
    for linha in lista_de_linhas:
        for coluna in linha.find_all('td'):
            if idxRegistro == 1 :
                lista_de_urls.append(coluna.find('a').get('href'))
            lista_de_tds.append(coluna.get_text().strip())
            idxRegistro += 1
        idxRegistro = 1
    
    #Pego o nro de registros e divido em blocos de 6 por conta da tabela
    nr_Registros = int(len(lista_de_tds)/6)
    
    idxRegistro = 0
    idxInicio,idxFim = 0, 5
    
    while idxRegistro < nr_Registros:
        
        nome, area, detentor, cns, matricula = lista_de_tds[idxInicio:idxFim]
        urlRegistro = lista_de_urls[idxRegistro]
        #trato as strings antes de inserir no banco de dados
        nome = tratarString(nome)
        area = tratarString(area)
        detentor = tratarString(detentor)
        cns = tratarString(cns)
        matricula = tratarString(matricula)
        
        insereSQLinicial ([nome, area, detentor, cns, matricula, urlRegistro])
        
        idxInicio += 6
        idxFim += 6
        idxRegistro += 1
    return 


def insereSQLdetalhe(lista):
    
    try:
        connection = conectaDW()
        sql  = "insert into _CORPORATE.TB_SIGEF_DETALHE values("
        sql += "'{}','{}','{}','{}','{}','{}')".format(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5])
        
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.commit()
        cursor.close()
        connection.close()
    
    except:
        print("Erro no insert dos dados no banco de dados\n")
        LOGGER.error(sql)
        sleep()
    
    return


#Pego a lista de nomes do arquivo e monto uma lista para acessá-los
def getListaNomes(filedata):

    lista_Nomes = []
    with open(filedata,'r',encoding='u8') as f:
        dataList = f.readlines()
    
        for line in dataList:
            lista_Nomes.append(line.split('\n')[0])
    
    return lista_Nomes


#Monto a URL para buscar a lista inicial de casos
def getUrl(proprietario, idPagina=1):
    url = "https://sigef.incra.gov.br/consultar/parcelas/?page={}&pesquisa_avancada=True&proprietario={}".format(idPagina, proprietario)
    return url


def navegaPaginaInicial():
    
    lista_Nomes = getListaNomes(LOCAL_ARQUIVO)
                  
    for nome in lista_Nomes:
        #sleep()
        url = getUrl(nome)
        LOGGER.debug("#pesquisa pelo nome {}".format(nome))
        #-----------------------------------------------------
        requisicao = requests.get(url, verify=False)
        soup = BeautifulSoup(requisicao.text, 'html.parser')
        
        
        resultados = soup.find('h3').get_text().strip()
        resultados = int(resultados.replace('Resultados: ','').strip())
        
        if resultados != 0:
            #Busco o item de paginação. Se ele existir, sei que há mais de uma
            #página para consultar
            if soup.find("div", {"class":"pagination"}):
                try:
                    #Possui mais de uma pagina
                    MAX_PAGINA = int(soup.find("div", {"class":"pagination"}).find_all("li")[-2].text)
                except:
                    MAX_PAGINA = 1
            else: 
                #Não possui mais de uma pagina
                MAX_PAGINA = 1
        
            i=1
            print("max_pagina: {}".format(MAX_PAGINA))
            while i <= MAX_PAGINA:
                
                url = getUrl(nome, i)
                print('\n########################################\n')
                print('Nome: {}\nURL: {}\n'.format(nome, url))
                print('\nPagina: {}, Nome: \nSolicitando dados da página\n'.format(i, nome))
                requisicao = requests.get(url, verify=False)
                soup = BeautifulSoup(requisicao.text, 'html.parser')
                
                pegaDadosPaginaInicial(soup)
                i+=1
    return 


if __name__ == '__main__':
    
    navegaPaginaInicial()