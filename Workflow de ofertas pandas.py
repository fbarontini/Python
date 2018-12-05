# -*- coding: utf-8 -*-
"""
Automatização de ofertas do Alexandre
@creation_date: 13/09/2018
@author: fbarontini
"""

import pandas as pd
import numpy as np
from time import sleep
import pypyodbc as db
import re
# import matplotlib.pyplot as plt

ARQUIVO = 'wf.xlsx'    # Arquivo exportado do SIR
POLITICA = 'politicas.xlsx'
#r'X:/MIS/Relatorios/PCJ/Workflow Ofertas/Calculadora.xlsx'    # Arquivo exportado do SIR
SQL_FILE = 'busca.sql' # link para o arquivo SQL na pasta.



def substitui_score(s):
    # função para trazer apenas a primeira letra do score
    # pois no sir há composição nos nomes cadastrados.
    
    try:
        score = s[0]
    except:
        score = '0'
    return score


def converte_para_numero(x):
    # funcao para converter o valor em um float
    x = x.replace('.','')
    x = x.replace('R$ ','')
    x = x.replace(',','.')
    return float(x)


def strip_strig(s):
    return s.strip()


def conectaDW():
    try:
        c = db.connect(
            Trusted_Connection='yes' #elimina validação de usuario e usa conexão de rede
            ,driver = '{SQL Server}'
            ,server='SDW02,1344'
            ,database='DB_DM1'
        )
        return c
    except:
        sleep(180)
        conectaDW()
        

def get_cpf_cnpj(s):
    # encontro a última ocorrencia de um espaço
    # e trago o cnpj que está a frente da string
    RE_INT = re.compile(r'[0-9]')
    s = s[s.rfind(' '):].strip()
    if RE_INT.match(s):
        return s
    else:
        return '0'


def convert_int(x):
    return int(x)

def trata_parcelas(x):

    if x <= 1:
        p = 'A) A VISTA'
    
    elif 1 < x <= 3:
        p = 'B) 1 A 3'
    
    elif 4 <= x <= 6:
        p = 'C) 4 A 6'
    
    elif 7 <= x <= 12:
        p = 'D) 7 A 12'
    
    elif 13 <= x <= 24:
        p = 'E) 13 A 24'
    
    elif 25 <= x <= 36:
        p = 'F) 25 A 36'
    
    else:
        p = 'G) 37 A 48'
        
    return p


def trata_segmento(s):

    if s == 'VEICULOS':
        return 'VEÍCULOS'
    else:
        return s


def getQuery(path = SQL_FILE):
    
    with open(path, 'r') as f:
        query = f.read()

    return query


def troca_segmento(segmento,rating):
    new_score = rating
    if segmento == 'VEICULOS':
        if rating == 'A':
            new_score = 'K'
        elif rating == 'B':
            new_score = 'L'
        elif rating == 'C':
            new_score = 'M'
        elif rating == 'D':
            new_score = 'N'
        elif rating == 'E':
            new_score = 'O'
        elif rating == 'F':
            new_score = 'P'
        elif rating == 'G':
            new_score = 'Q'
        elif rating == 'H':
            new_score = 'R'
        elif rating == 'I':
            new_score = 'S'
        elif rating == 'J':
            new_score = 'T'
    else:
        new_score = rating
    
    return new_score


def avalia_oferta(segmento, minimo, oferta, per_sop):
    # funcao para avaliar as ofertas
    status = ''
    if segmento not in ['VEICULOS', 'PNJ']:
        if per_sop and oferta:
            status = '{}: {}% do SOP'.format(segmento,per_sop)
    else:
        if oferta >= minimo:
            status = 'Aprovar'
        else:
            status = 'Contra: {}'.format(minimo)
        
    return status



if __name__ == '__main__':
    
    # abro o arquivo na pasta raiz
    df_arquivo = pd.read_excel(ARQUIVO)
    
    # substituo as colunas para deixá-las todas minúsculas
    colunas = [x.lower().replace(' ','') for x in df_arquivo.columns]
    df_arquivo.columns = colunas
    
    # chamo as helper functions para ajustar a base do Ale.
    df_arquivo.scoring = df_arquivo.scoring.apply(substitui_score)
    df_arquivo.valoroferecido = df_arquivo.valoroferecido.apply(converte_para_numero)
    df_arquivo.rol = df_arquivo.rol.apply(strip_strig)
    df_arquivo['documento'] = df_arquivo.referência.apply(get_cpf_cnpj)
    df_arquivo['fx_parcelas'] = df_arquivo.parcelas.apply(trata_parcelas)
    
    # crio uma string com uma lista de todos os documentos para consultar
    slistacpf = ','.join(df_arquivo.documento.values)
    
    df_arquivo['documento'] = df_arquivo.documento.apply(convert_int)
    # adiciono essa lista na minha query
    query = getQuery().replace('[CPF]',slistacpf)
    # crio uma conexão com o banco de dados para poder executar
    # a query e salvar num dataframe.
    conn = conectaDW()
    df_sql = pd.read_sql_query(query, conn)
    
    # uno os dois dataframes
    df_arquivo = pd.merge(df_arquivo, df_sql, on=['carteira','documento'], how='left')
    # ajusto os segmentos de veiculos
    df_arquivo['scoring'] = np.vectorize(troca_segmento)(df_arquivo['segmento'],df_arquivo['scoring'])
    
    # abro o arquivo de politicas
    #df_politica = pd.read_excel(POLITICA, sheet_name='DADOS')
    df_politica = pd.read_excel(POLITICA, sheet_name='Sheet1')

    # junto os arquivos de politica com o original
    df_arquivo = pd.merge(df_arquivo, df_politica, on = ['scoring','segmento','carteira','fx_atraso','fx_parcelas'], how='left')
    
    df_arquivo['minimo'] = np.round(df_arquivo['desconto'] * df_arquivo['vlsop'],2)
    df_arquivo['per_sop'] = np.round(100*df_arquivo['valoroferecido']/df_arquivo['vlsop'],0)
    
    df_arquivo['status'] = np.vectorize(avalia_oferta)(df_arquivo['segmento'],df_arquivo['minimo'], df_arquivo['valoroferecido'], df_arquivo['per_sop'])
    
    writer = pd.ExcelWriter('wf_retorno.xlsx')
    df_arquivo.to_excel(excel_writer=writer, sheet_name='base', header=True, index=False)
    writer.save()
