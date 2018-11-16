from Email import Email;
import pandas as pd
import pypyodbc as db
from time import sleep
import os

SQL_FILE = 'Batimento_de_casos.sql'
ESCOBS = 'controle_emails.xlsx'
HTML = r'Batimento_de_casos_html.txt'
SMTP = 'SMTP_IP'
PATH = r'PATH FOR SAVING FILES'
PORT = 25
FROM = 'FROM EMAIL'
RECOVERY = ['EMAIL LIST WITH PROJECT OWNERS']


def conectaDW():
    try:
        c = db.connect(
            Trusted_Connection='yes' #elimina validação de usuario e usa conexão de rede
            ,driver = '{SQL Server}'
            ,server='SQLServerLink'
            ,database='DatabaseName'
        )
        return c
    except:
        sleep(180)
        conectaDW()


def getQuery(path = SQL_FILE):
    
    with open(path, 'r') as f:
        query = f.read()

    return query


def getHtml(path=HTML):
    # Leio o arquivo HTML que está na pasta raíz.
    # Nele tenho o texto que será enviado no corpo
    # do email aos escobs.
    with open(path, 'r') as f:
        html = f.read()
        
    return html

if __name__ == '__main__':
       
    escob = pd.read_excel(ESCOBS)
    conn = conectaDW()
    #conn.autocommit = True
    df = pd.read_sql_query(getQuery(),conn)
    #sleep(5)
    conn.close()
    
    # realizo uma iteração para cada escritorio, 
    # gerando uma base para cada um
    
    for agencia in df['idagencia'].unique():
    
        if agencia not in [2404,1904,1665,1483,1929,1505,1199,1201,2428,2416,1736,1899,1036,2424,2425]:
            pass
        else:
        
            # separo o nome e o email para envio da agencia.
            nome = escob[ escob['idagencia'] == agencia ]['nome'].iloc[0]
            nome_sir = escob[ escob['idagencia'] == agencia ]['dsagencia'].iloc[0]
            emails = escob[ escob['idagencia'] == agencia]['email'].iloc[0].split(';')
            
            # separo a base por escob
            base = df[ df['idagencia'] == agencia ]
            
            # ddireciono o arquivo a ser salvo na pasta
            arquivo = './arquivos/' + nome + '.xlsx'
            writer = pd.ExcelWriter(arquivo)
            base.to_excel(writer, nome, index=False)
            writer.save()
            
            # crio o objeto email
            message = Email(SMTP, PORT)
            # adiciono o email from
            message.setFrom(FROM)
            #adiciono os responsaveis pelo escob + recovery
            [message.addRecipient(e) for e in emails]
            [message.addRecipient(e) for e in RECOVERY]
            # defino o assunto do email
            assunto = 'Batimento de Carteira Juridica - ' + nome_sir
            message.setSubject(assunto)
            # adiciono o anexo
            #os.chdir('./arquivos/')
            message.addAttachment(os.path.abspath(arquivo))
            # adiciono o texto do email
            message.setHtmlBody(getHtml(HTML))
            message.send()
        
            #os.chdir('../')
        