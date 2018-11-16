# Validador de email via expressao regular.
"""
Created on Thu Mar 29 10:58:07 2018
@author: fbarontini
"""
import re, time, csv, requests
import pandas as pd

LINK_DO_ARQUIVO = 'emails_2.txt'
DOMINIOS_VALIDOS = pd.read_csv('Email_validator_dominios_validos.csv',encoding = 'latin-1')
DOMINIOS_INVALIDOS = pd.read_csv('Email_validator_dominios_invalidos.csv',encoding = 'latin-1')
VALIDOS, INVALIDOS = [], []


# ------------------------------------------------
def sleep(t = 0.25):
    time.sleep(t)


# ------------------------------------------------
# REGEX para validar se o email eh valido
# Apenas verifica se possui '@', '.com', etc.
def valida_email(email):
    
    if email:
        try:
            check = bool(re.search(r"^[\wa-zA-Z\.\+\-]+\@[\wa-zA-Z]+\.[a-zA-Z]{2,3}[\w]+\.[a-zA-Z]{2}$", email))
            if not check:
                check = bool(re.search(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))
        
        except:
            check = False
    else:
        check = False
    return check


# ------------------------------------------------
def length(s):
    return len(str(s))


# ------------------------------------------------
def substituir(s):

    s = str(s).strip()
    s = s.replace('\ ' , '')
    s = s.replace('\n','')
    s = s.replace(' ', '')
    s = s.replace('\t', '')
    s = s.replace(';','')
    s = s.replace(',','')
    s = s.replace('(','')
    s = s.replace(')','')
    s = s.replace('[','')
    s = s.replace(']','')
    s = s.replace('{','')
    s = s.replace('}','')
    
    return s.lower()


# ------------------------------------------------
def dominio(s):

    try:
        s = s.split('@')[1]
    except:
        s = 'Erro na localizacao'
    return s


# ------------------------------------------------
def r(url):
    # Para uma visão mais detalhada de cada código,
    # consulte as informações disponiveis em
    # https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status
    u = url
    url = 'http://www.' + url
    try:
        scode = requests.get(url).status_code
    except:
        scode = 404
    
    '''
    if scode == 200:
        dicionario = {}
        dicionario['Dominio'] = u
        # ERRO aqui
        DOMINIOS_VALIDOS['Dominio'].append(pd.DataFrame(dicionario))
    else:
        #insere nos invalidos
        DOMINIOS_INVALIDOS['Dominio'].append(pd.DataFrame({'Dominio':u}))
    '''
    
    # print("Consulta ao site {} deu status code {}".format(url, scode))
    return scode


# ------------------------------------------------
def checa_dominio(dominio):
    
    if not dominio or dominio == '':
        check = False
    # se o dominio já existe na base de dominios validos, True
    elif DOMINIOS_VALIDOS['Dominio'].str.contains(dominio).any():
        check = True
    # se o dominio já existe na base de dominios invalidos, False
    elif DOMINIOS_INVALIDOS['Dominio'].str.contains(dominio).any():
        check = False
    # se nao tenho o dominio em nenhuma base, consulto na hora
    #elif r(dominio) == 200:
    #    check = True
    #    VALIDOS.append(dominio)
    #    #cadastraNovosValidos(dominio)
    #    print('Dominio consultado: {}'.format(dominio))
    else:
        check = False
        INVALIDOS.append(dominio)
        #cadastraNovosInvalidos(dominio)
    
    return check


# ------------------------------------------------
def cadastraNovosValidos(lista):
    
    with open('dominios_validos.csv','a') as f:
    
        csvfile = csv.writer(f,lineterminator = '\n')
        for data in lista:
            csvfile.writerow([data])
        #while len(lista) > 0:
        #    csvfile.writerow([lista.pop()])


# ------------------------------------------------
def cadastraNovosInvalidos(lista):
    
    with open('dominios_invalidos.csv','a') as f:
    
        csvfile = csv.writer(f,lineterminator = '\n')
        for data in lista:
            csvfile.writerow([data])
        #while len(lista) > 0:
        #    csvfile.writerow([lista.pop()])
            
        


if __name__ == '__main_9_':
    
    # abro o arquivo de emails
    email = pd.read_csv(LINK_DO_ARQUIVO, sep=';', error_bad_lines = False, \
                        warn_bad_lines = False, encoding = 'latin-1', \
                        quoting = csv.QUOTE_NONE) # nrows = 50000)
    
    # aplico a função 'substituir' e salvo o retorno na coluna vchMail
    email['vchMail'] = email['vchMail'].apply(substituir)
    # aplico a função 'dominio' e salvo o retorno na coluna Dominio
    email['Dominio'] = email['vchMail'].apply(dominio)
    # aplico a função 'valida_email' e salvo o retorno na coluna EmailValido
    email['EmailValido'] = email['vchMail'].apply(valida_email)
    
    # crio uma serie com os dominios agrupados pela quantidade
    # absoluta de aparições
    #d = email.groupby('Dominio')['Dominio'].count()
    # Converto a serie para um dataframe e jogo
    # o index dela como uma coluna
    #d.name = 'Quantidade'
    #d = d.to_frame()
    #d.reset_index(inplace=True)
    #d['Valido'] = d['Dominio'].apply(r)
    #d.to_csv('dominios.csv', sep=';')
    
    
    #d['DominioValido'] = d['Dominio'].apply(checa_dominio)
    '''
    if len(VALIDOS) > 0 :
        cadastraNovosValidos(VALIDOS)
    
    if len(INVALIDOS) > 0 :
        cadastraNovosInvalidos(INVALIDOS)
    
    
    for k, v in d.iterrows():
        checa_dominio(v['Dominio'])
    
    if len(VALIDOS) > 0 :
        cadastraNovosValidos(VALIDOS)
    
    if len(INVALIDOS) > 0 :
        cadastraNovosInvalidos(INVALIDOS)
    '''

    # junto os dois dataframes para 
    #email = email.merge(d[['Dominio','DominioValido']], how='left', on='Dominio')
    
    # Validação dos dominios
    # validos = d[ d['Valido'] == 200 ]
    # invalidos = d[ d['Valido'] != 200 ]
    # validos['Dominio'].to_csv('dominios_validos.csv',index=False,header=True)
    # invalidos['Dominio'].to_csv('dominios_invalidos.csv',index=False,header=True)
    
    #colunas = ['intIdContacto','vchMail', 'EmailValido', 'DominioValido']
    email.to_csv('retorno_emails.csv',  index=False, sep=';') #columns=colunas,
