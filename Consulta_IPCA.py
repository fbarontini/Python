# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 15:29:20 2018
@author: fbarontini

Sistema de coleta dos dados de Inflação do Brasil,
divulgados através do webservice do BACEN
"""
from zeep import Client
import pandas as pd

#-------------------BACEN--------------------
_WSDLFILE = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
_Cliente = None
try:
    _Cliente = Client(_WSDLFILE)
except OSError as err:
    print('Erro na conexão!')


def consultaValor(dtConsulta):
    try:
		# o numero 433 equivale ao indice da serie no bacen
        resposta = _Cliente.service.getValor(433,dtConsulta)
        resposta = resposta['_value_1']
    except:
        resposta = 0.0
    return float(resposta)


if __name__ = '__main__':

	# Abro um arquivo com datas para buscar no ws e aplico a função consultaValor.
	df = pd.read_csv('Consulta_IPCA_datas.txt')
	df['valor'] = df['datas'].apply(consultaValor)

	# Salvo o retorno no arquivo abaixo
	output = 'retorno_ipca.txt'
	df.to_csv(output, index=False)