# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 15:44:11 2018
@author: fernando.barontini
"""
# Imports
from time import sleep
from datetime import datetime
import requests, json, sys, re
import pandas as pd
import MySQLdb as sql
import sqlalchemy
#-#---------------------------------------------------------------------
# Doc specs
URL = 'https://www.receitaws.com.br/v1/cnpj/{}'
COLS = ['atividade_principal','qsa','extra','atividades_secundarias', 'billing']
CNAE, QSA = [], []
RETORNO = []
ERROS = []
engine = sqlalchemy.create_engine("mysql+mysqldb://fbarontini:"+'barontini01'+"@localhost/receita_federal")
#-#---------------------------------------------------------------------
# Code functions
def get_url(cnpj):
	# função para montar a URL dado um CNPJ
	return URL.format(cnpj)


def trata_cpf(s):
	s = re.sub('[^0-9]','',s)
	return s


def adiciona_cnae(cnae):
	# salvo o cnae na lista de CNAES
	# para exportá-los depois
	global CNAE
	CNAE.append(cnae)
	return True


def adiciona_qsa(qsa):
	# salvo o cnae na lista de CNAES
	# para exportá-los depois
	global QSA
	QSA.append(qsa)
	return True


def salva_arquivos():
	
	agora = datetime.now().strftime('%Y%m%d_%H%M%S')
	
	# Arquivo de Erros
	if len(ERROS) > 0:
		
		agora = datetime.now().strftime('%Y%m%d_%H%M%S')
		arquivo_erros = './Consultas/Erros_{}.xlsx'.format(agora)
		writer = pd.ExcelWriter(arquivo_erros)
		
		# crio o arquivo excel de erros
		edf = pd.DataFrame(ERROS)
		edf.to_excel(excel_writer=writer, sheet_name='erros', header=True, index=False)
		writer.save()
		
		print('Arquivo salvo na pasta de consultas.')
		print('Nome: {}'.format(arquivo_erros))
	
	if len(RETORNO) > 0:
		agora = datetime.now().strftime('%Y%m%d_%H%M%S')
		arquivo_retorno = './Consultas/Consultas_{}.xlsx'.format(agora)
		writer = pd.ExcelWriter(arquivo_retorno)
		
		# crio o arquivo excel de erros
		ret = pd.DataFrame(RETORNO)
		ret.to_excel(excel_writer=writer, sheet_name='consulta',
					   header=True, index=False)
		
		if len(CNAE) > 0:
		
			# crio o arquivo excel de erros
			ret_cnae = pd.DataFrame(CNAE)
			ret_cnae.to_excel(excel_writer=writer, sheet_name='cnaes',
								 header=True, index=False)
		
		if len(QSA) > 0:
		
			# crio o arquivo excel de erros
			ret_qsa = pd.DataFrame(QSA)
			ret_qsa.to_excel(excel_writer=writer, sheet_name='qsa',
								 header=True, index=False)
		
		# por fim, salvo o arquivo.
		writer.save()
		print('Arquivo salvo na pasta de consultas.')
		print('Nome: {}'.format(arquivo_retorno))
	
	return True

#def salva_mysql(js):
#	
#	conn = sql.Connect(
#            host='localhost',
#            database='receita_federal',
#            user='fbarontini',
#            password='barontini01')
#	
#	curs = conn.cursor()
#	
#	return False

#-#---------------------------------------------------------------------
# Função de consulta e tratamento dos dados
def consulta(cnpj):
	
	# função de consulta ao site com tratamento das colunas que
	# possuem retorno em lista ou em dicionários.
	
	url = get_url(cnpj)
	print('Pesquisando o cnpj {}. Aguarde'.format(cnpj))
	r = requests.get(url)
	sleep(12)
	
	if r.status_code == 200:
		
		j = json.loads(r.text)
		j['documento'] = cnpj
		
		if 'atividade_principal' in j.keys():
			# Salvo a atividade Principal e o quadro societario
			# CNAE PRIMARIO
			cnae = {}
			cnae['documento'] = cnpj
			cnae['codigo'] = j['atividade_principal'][0]['code']
			cnae['descricao'] = j['atividade_principal'][0]['text']
			adiciona_cnae(cnae)
		
		# CNAE SECUNDARIO
		if 'atividades_secundarias' in j.keys():
			for ativ in j['atividades_secundarias']:
				cnae = {}
				cnae['documento'] = cnpj
				cnae['codigo'] = ativ['code']
				cnae['descricao'] = ativ['text']
				adiciona_cnae(cnae)
		
		# QUADRO SOCIETARIO
		if 'qsa' in j.keys():
			for socio in j['qsa']:
				qsa = {}
				qsa['documento'] = cnpj
				qsa['qualificacao'] = socio['qual']
				qsa['nome'] = socio['nome']
				adiciona_qsa(qsa)
		
		
		#função para excluir as colunas mencionadas na def da função
		[j.pop(c) for c in COLS if c in j.keys()];
		
		# insiro as informações consultadas na lista
		
		global RETORNO
		RETORNO.append(j)
		
	
	else:
		# insiro o erro na lista ERROS para mapear o que precisa rodar novamente
		erro = {}
		erro['documento'] = cnpj
		erro['data_pesquisa'] = datetime.now()
		erro['codigo'] = r.status_code
		erro['descricao'] = r.text
		
		global ERROS
		ERROS.append(erro)
		
		

	
	#df = pd.DataFrame(retorno)
	#df.to_sql(	name='consultas_log',
	#			con=engine,
	#			index=False,
	#			if_exists='append')
	return True


#-#---------------------------------------------------------------------
# Função para consulta individual
def main():
	
	#documento = '36588524889'
	cnpj = input('Digite o documento a pesquisar: ')
	cnpj = trata_cpf(cnpj)
	
	consulta(cnpj)
	
	salva_arquivos()
	
	
	return True

#-#---------------------------------------------------------------------
# Função para consulta massiva
def massivo():
	print('Entrando no Módulo Massivo')
	CONSULTAS = []
	try:
		with open('CONSULTAR.txt', 'r') as f:
			linhas = f.readlines()
	    
		for linha in linhas:
			CONSULTAS.append(trata_cpf(linha))
	except:
		print('Arquivo CONSULTAR.TXT nao localizado no diretorio.')
		sys.exit()
	
	
	for documento in CONSULTAS:
		consulta(documento)
		sleep(2)
	
	
	salva_arquivos()
	
	return True

#-#---------------------------------------------------------------------
# Main function
if __name__ == '__main__':
	
	# para ler arquivo direto do prompt de comando
	if len(sys.argv) > 1 and sys.argv[1] == '-m':
		massivo()
	else:
		main()