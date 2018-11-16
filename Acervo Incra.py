from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pypyodbc as db
import time

URL = "http://acervofundiario.incra.gov.br:8080/Conversao01/faces/index.xhtml"
CERTIFICACAO = []
LISTA_RETORNO = []

def sleep(value = 2.5):
    time.sleep(value)

def tratarString(linha):

    linha = linha.replace("'","")
    linha = linha.replace("°","")
    linha = linha.replace("Á","A")
    linha = linha.replace("É","E")
    linha = linha.replace("Í","I")
    linha = linha.replace("Ó","O")
    linha = linha.replace("Ú","U")
    linha = linha.replace("Ç","C")
    linha = linha.replace("Â","A")
    linha = linha.replace("Ê","E")
    linha = linha.replace("Î","I")
    linha = linha.replace("Ô","O")
    linha = linha.replace("Û","U")
    linha = linha.replace("À","A")
    linha = linha.replace("È","E")
    linha = linha.replace("Ì","I")
    linha = linha.replace("Ò","O")
    linha = linha.replace("Ù","U")
    linha = linha.replace("Ã","A")
    linha = linha.replace("Õ","O")
    
    return linha

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
        sleep(180)
        conectaDW()

def getDataFromSql():
    # Busco apenas um registro para pesquisar na pagina do acervo.
    connection = conectaDW()
    cursor = connection.cursor()
    query = "select top 1 nrCertificacao from _corporate.viwAcervoIncra "
    query += "where direita between 60 and 70"
    cursor.execute(query)
    results = list(cursor.fetchall())
    rowarray_list = []
    
    for row in results:
        rowarray_list.append(row[0])
    cursor.close()
    connection.close()
    
    return rowarray_list

def insereSQL(lista):
    
    connection = conectaDW()
    sql  = "insert into table_identity values("
    sql += "'{}','{}','{}','{}','{}','{}','{}','{}')".format(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5],lista[6],lista[7])
    
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.commit()
    cursor.close()
    connection.close()
    
    return

def insereSQLNaoEncontrado(listaErro):
    
    connection = conectaDW()
    sql  = "insert into table_identity (column_name) values("
    sql += "'{}')".format(listaErro)
    
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.commit()
    cursor.close()
    connection.close()
    
    return


#Abro a página do Acervo INCRA
try:
    driver = webdriver.Chrome(executable_path="C:\\temp\\chromedriver.exe")
    #driver = webdriver.Ie(executable_path=r"C:\\temp\\IEDriverServer.exe")
    #driver = webdriver.Firefox(executable_path="C:\\temp\\geckodriver.exe")

except:
    print("Erro ao criar o driver.")

connection = conectaDW()
CERTIFICACAO = getDataFromSql()

while len(CERTIFICACAO) > 0:
    for CERT in CERTIFICACAO:
        #Abro a pagina e insiro o nro de certificacao no inputbox relativo.
        driver.get(URL)
        sleep(0.5)
        elem = driver.find_element_by_id("j_idt5:numcert")
        elem.click()
        elem.clear()
        elem.send_keys(CERT)
        sleep(0.5)
        elem.send_keys(Keys.RETURN)
        sleep(0.5)
        elem = ''
        # Para cada inputbox do retorno, eu dou um
        # getAttribute para salvar a informação
        #---------------------------------------------------
        try:
        #---------------------------------------------------
            elem = driver.find_element_by_id("j_idt5:j_idt20")
            sleep(0.25)
            cod_imov_rural = elem.get_attribute('value')
        #---------------------------------------------------
            elem = driver.find_element_by_id("j_idt5:j_idt22")
            sleep(0.25)
            nr_processo = elem.get_attribute('value')
        #---------------------------------------------------
            elem = driver.find_element_by_id("j_idt5:j_idt24")
            sleep(0.25)
            nome_imovel_rural = elem.get_attribute('value')
        #---------------------------------------------------
            elem = driver.find_element_by_id("j_idt5:j_idt26")
            sleep(0.25)
            nome_interessado = elem.get_attribute('value')
        #---------------------------------------------------
            elem = driver.find_element_by_id("j_idt5:j_idt28")
            sleep(0.25)
            regional_uf = elem.get_attribute('value')
        #---------------------------------------------------
            elem = driver.find_element_by_id("j_idt5:j_idt30")
            sleep(0.25)
            municipio = elem.get_attribute('value')
        #---------------------------------------------------
            elem = driver.find_element_by_id("j_idt5:j_idt32")
            sleep(0.25)
            qtd_area_calculada = elem.get_attribute('value')
        #---------------------------------------------------
            
            if cod_imov_rural != '':
                
                nome_imovel_rural = tratarString(nome_imovel_rural)
                nome_interessado = tratarString(nome_interessado)
                regional_uf = tratarString(regional_uf)
                municipio = tratarString(municipio)
                listaAux = [CERT,cod_imov_rural, nr_processo, nome_imovel_rural, nome_interessado, regional_uf, municipio, qtd_area_calculada]
                LISTA_RETORNO.append(listaAux)
                
                insereSQL(listaAux)
            else:
                insereSQLNaoEncontrado(CERT)
            
            cod_imov_rural = ''
            nr_processo = ''
            nome_imovel_rural = ''
            nome_interessado = ''
            regional_uf = ''
            municipio = ''
            qtd_area_calculada = ''
            elem = ''
        
        except:
        #---------------------------------------------------
            print("Erro na busca: {}".format(CERT))
            #insereSQLNaoEncontrado(CERT)
            #break
        #---------------------------------------------------
        
        CERTIFICACAO = getDataFromSql()
        elem = ''

driver.quit()
connection.close()