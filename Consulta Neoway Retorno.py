# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:14:57 2018
@author: fernando.barontini
"""

import os
import json
import pandas as pd

def trata_arquivos():
	
	FOLDER = './json/'
	JSON = []
	#df = pd.DataFrame()
	
	
	# leio todos os arquivos e armazeno na variável JSON
	for file in os.listdir(FOLDER):
		
		if file.endswith('txt'):
			
			if len(file) != 15:
				arq = FOLDER + file 
				with open(arq,'rb') as f:
					JSON.append(json.loads(f.read()))
		else:
			continue
	
	print('Consegui ler {} arquivos'.format(len(JSON)))
	
	# pego todos os itens da lista JSON e armazeno em uma variável
	# que vai guardar as chaves dos dicionários.
	KEYS = []
	for j in JSON:
		for key in j.keys():
			if key not in KEYS:
				KEYS.append(key)
	
	print('Foram encontradas {} chaves'.format(len(KEYS)))
	
	
	# Verifico o tipo de cada variavel que o json retorna
	# geralmente vai ser list ou dict
	TYPES = []
	for js in JSON:
	    for key in KEYS:
	        if key in js.keys():
	            d = key + ': {}'.format(type(js[key]))
	            if d in TYPES:
	                pass
	            else:
	                TYPES.append(d)
	        else:
	            pass

	return True


#-#----------------------------------------------------------------

def trata_json_pj(js):
	
	QUAN, CNAE, EMPR, TELS = [], [], [], []
	INPI, IMOV, CNDS, ENDE = [], [], [], []
	SINT, DOAC, FILI, SOCI = [], [], [], []
	BENE, ARTS, FUNC, SITE = [], [], [], []
	BALP, EBIT, FINA, DEBT = [], [], [], []
	VEIC, MULT, UNIV 	   = [], [], []
	
	d = {}
	cnae = {}
	
	# - - - -
	# tratamento das colunas que são string
	col_str = ['_id','cnpj','dataAbertura','nivelAtividade',
			  'porte','razaoSocial','fantasia']
	
	for col in col_str:
		if col in js.keys():
			d[col] = js[col]
		else:
			d[col] = None
	
	del col_str
	
	# - - - -
	# tratamento das colunas que são dict
	col_dic = ['_id','_metadata','antt','arts',
			'beneficiarios','beneficiariosJunta','calc','cnaePrincipal',
			'cnaes','cnpj','crescimentoPorAnoRais','dataAbertura',
			'detran','doacaoEleitoral','empresasColigadas',
			'empresasSimilares','endereco','exfuncionarios',
			'expectativaVidaEmpresas','faturamentoPresumido','filiais',
			'funcionarios','ibge','importacao','info','inpiMarcas',
			'matriz','mteCnd','natureza','nivelAtividade','novoPat',
			'porte','potencialConsumo','potencialConsumoRamo',
			'processoJudicialTotalizadores','qsaUnificado',
			'razaoSocial','simplesNacional','sintegra','situacao',
			'socios','sociosJunta','telefones','totalFuncionarios',
			'totalVeiculos','tributaryHealth','veiculosPesados',
			'fantasia','cafir','autoInfracao','debitosPgfnDau',
			'dominios','pontosAbastecimento','pontosAbastecimentoTanque',
			'foodEstabCategories','bancoCentral','empresaBalancoFinanceiro',
			'cnes','ibamaCtf','imoveis','inpiProgramas','capitalAberto',
			'cvm','aeronaves','atividadeFinanceira','postosCombustiveis',
			'ibamaEmbargos','ceis','mteTrabalhoEscravo','escolas','cfc',
			'ibamaCnd','empresaCepim','faculdades']
	
	for col in col_dic:
		if col in js.keys():
			
			# tratamento da chave CALC
			if col == 'calc':
				chaves = ['totalExFuncionarios',
						  'totalObras',
						  'totalVeiculosPesados']
				# valido se há alguma chave dentro do dicionario
				# que ainda não foi mapeada.
				# --- Validação
				for chave in js[col].keys():
					if chave not in chaves:
						print('A coluna "{}" não foi mapeada'.format(chave))
				# ---
				for k in chaves:
					# total de funcionarios
					if k in js[col].keys() and k =='totalExFuncionarios':
						for i in js[col][k]['porAno']:
							q = {}
							q['cnpj'] = d['cnpj']
							q['tipo'] = k
							q['ano'] = i['ano']
							q['qtd'] = i['quantidade']
							QUAN.append(q)
					# total de obras
					elif k in js[col].keys() and k == 'totalObras':
						if 'concluidas' in js[col][k].keys():
							for i in js[col][k]['concluidas']:
								q = {}
								q['cnpj'] = d['cnpj']
								q['tipo'] = k
								q['ano'] = i['ano']
								q['qtd'] = i['quantidade']
								q['descricao'] = 'concluidas'
								QUAN.append(q)
						
						if 'iniciadas' in js[col][k].keys():
							for i in js[col][k]['iniciadas']:
								q = {}
								q['cnpj'] = d['cnpj']
								q['tipo'] = k
								q['ano'] = i['ano']
								q['qtd'] = i['quantidade']
								q['descricao'] = 'iniciadas'
								QUAN.append(q)
			
			# Cnae Principal
			elif col == 'cnaePrincipal':
				cnae['cnpj'] = d['cnpj']
				cnae['codigo'] = js[col]['codigo']
				cnae['descricao'] = js[col]['descricao']
				cnae['ramoAtividade'] = js[col]['ramoAtividade']
				cnae['setor'] = js[col]['setor']
				cnae['principal'] = True
				CNAE.append(cnae)
			
			# Outros CNAES
			elif col == 'cnaes':
				for cnaes in js[col]:
					cnae['cnpj'] = d['cnpj']
					cnae['codigo'] = cnaes['codigo']
					cnae['descricao'] = cnaes['descricao']
					cnae['ramoAtividade'] = None
					cnae['setor'] = None
					cnae['principal'] = False
					CNAE.append(cnae)
			
			# Crescimento RAIS
			elif col == 'crescimentoPorAnoRais':
				for cresc in js[col]:
					# Percentual
					q = {}
					q['cnpj'] = d['cnpj']
					q['tipo'] = col
					q['ano'] = cresc['ano']
					q['qtd'] = cresc['percentual']
					q['descricao'] = 'percentual'
					QUAN.append(q)
					# Quantidade de funcionarios
					q = {}
					q['cnpj'] = d['cnpj']
					q['tipo'] = col
					q['ano'] = cresc['ano']
					q['qtd'] = cresc['qtdFuncionarios']
					q['descricao'] = 'qtdFuncionarios'
					QUAN.append(q)
			
			# Infos adicionais
			elif col == 'info':
				for k,v in js[col].items():
					d[k] = v
			
			# Empresas similares
			elif col == 'empresasSimilares':
				for emp in js[col]:
					e = {}
					e['cnpj'] = d['cnpj']
					e['cnae'] = emp['cnae']
					e['cnpj_sim_col'] = emp['cnpj']
					e['naturezaJuridica'] = emp['naturezaJuridica']
					e['quantidadeFunc'] = emp['quantidadeFunc']
					e['razaoSocial'] = emp['razaoSocial']
					e['uf'] = emp['uf']
					e['tipo'] = col
					
					EMPR.append(e)
					
			# Empresas coligadas
			elif col == 'empresasColigadas':
				for emp in js[col]:
					e = {}
					e['cnpj'] = d['cnpj']
					e['cnae'] = emp['cnae']
					e['cnpj_sim_col'] = emp['cnpj']
					e['municipio'] = emp['municipio']
					e['razaoSocial'] = emp['razaoSocial']
					e['dataAbertura'] = emp['dataAbertura']
					e['uf'] = emp['uf']
					e['tipo'] = col
					
					EMPR.append(e)
				
			
			# Telefones
			elif col == 'telefones':
				for tel in js[col]:
					t = {}
					t['cnpj'] = d['cnpj']
					t['fonteInformacao'] = tel['fonteInformacao']
					t['numero'] = tel['numero']
					
					TELS.append(t)
			
			# Registro de patentes
			elif col == 'inpiMarcas':
				for value in range(len(js[col])):
					js[col][value]['cnpj'] = d['cnpj']
					INPI.append(js[col][value])
			
			# Imoveis CAFIR
			elif col == 'cafir':
				for value in range(len(js[col]['imoveis'])):
					js[col]['imoveis'][value]['cnpj'] = d['cnpj']
					IMOV.append(js[col]['imoveis'][value])
			
			# IBGE
			elif col == 'ibge':
				d['faixaRendaPopulacao'] = js[col]['faixaRendaPopulacao']
			
			# CND
			elif col == 'tributaryHealth':
				for value in range(len(js[col]['cnds'])):
					js[col]['cnds'][value]['cnpj'] = d['cnpj']
					js[col]['cnds'][value]['tipo'] = 'tributaryHealth'
					js[col]['cnds'][value]['saudeTributaria'] = js[col]['saudeTributaria']
					CNDS.append(js[col]['cnds'][value])
			
			# Optante pelo simples
			elif col == 'simplesNacional':
				d['optanteSimei'] = js[col]['optanteSimei']
				d['optanteSimples'] = js[col]['optanteSimples']
				d['simplesIrregular'] = js[col]['simplesIrregular']
			
			# Situacao da empresa
			elif col == 'situacao':
				d['data'] = js[col]['data']
				d['situacao'] = js[col]['descricao']
			
			# Natureza da empresa
			elif col == 'natureza':
				d['classificacao'] = js[col]['classificacao']
				d['natureza'] = js[col]['descricao']
			
			# Faturamento presumido
			elif col == 'faturamentoPresumido':
				d['faixaGrupo'] = js[col]['faixaGrupo']
				d['faixaIndividual'] = js[col]['faixaIndividual']
			
			# Endereco
			elif col == 'endereco':
				js[col]['cnpj'] = d['cnpj']
				ENDE.append(js[col])
			
			# Funcionarios
			elif col == 'totalFuncionarios':
				 d['qtdFuncionarios'] = js[col]['quantidade']
				 d['qtdFuncionariosGrupo'] = js[col]['quantidadeGrupo']
			
			# Sintegra
			elif col == 'sintegra':
				for line in js[col]:
					line['cnpj'] = d['cnpj']
					SINT.append(line)
			
			# Doações
			elif col == 'doacaoEleitoral':
				for doa in js[col]['doacoes']:
					doa['cnpj'] = d['cnpj']
					DOAC.append(doa)
					
			# Consumo
			elif col == 'potencialConsumo':
				d['capitalSocial'] = js[col]['valorCapitalSocial']
			
			# Consumo Ramo
			elif col == 'potencialConsumoRamo':
				d['potencialConsumoCml'] = js[col]['potencialConsumoRamo']['comercial']
				d['potencialConsumoRes'] = js[col]['potencialConsumoRamo']['residencial']
			
			# Expectativa
			elif col == 'expectativaVidaEmpresas':
				d['faixaExpectativa'] = js[col]['faixaExpectativa']
				d['idade'] = js[col]['idade']
				d['idadeAcimaExpectativa'] = js[col]['idadeAcimaExpectativa']
			
			# Dados Matriz
			elif col == 'matriz':
				d['empresaMatriz'] = js[col]['empresaMatriz']
				d['quantidadeFilial'] = js[col]['quantidadeFilial']
			
			# Dados Filiais
			elif col == 'filiais':
				for filial in js[col]:
					fili = {}
					fili['cnpj'] = d['cnpj']
					fili['cnpjFilial'] = filial['cnpj']
					fili['dataAbertura'] = filial['dataAbertura']
					fili['municipio'] = filial['municipio']
					fili['razaoSocial'] = filial['razaoSocial']
					fili['situacao'] = filial['situacao']
					fili['uf'] = filial['uf']
				
					FILI.append(fili)
			
			# Socios
			elif col == 'sociosJunta':
				for socio in js[col]:
					socio['cnpj'] = d['cnpj']
					socio['fonte'] = 'Junta Comercial'
					SOCI.append(socio)
			
			# Socios v2
			elif col == 'socios':
				for socio in js[col]:
					socio['cnpj'] = d['cnpj']
					socio['fonte'] = 'Outros'
					SOCI.append(socio)
			
			# Beneficiário Final Junta
			elif col == 'beneficiariosJunta':
				for socio in js[col]:
					socio['cnpj'] = d['cnpj']
					socio['fonte'] = 'Junta Comercial'
					BENE.append(socio)
			
			# Beneficiário Final
			elif col == 'beneficiarios':
				for socio in js[col]:
					socio['cnpj'] = d['cnpj']
					socio['fonte'] = 'Outros'
					BENE.append(socio)
			
			# ART
			elif col == 'arts':
				for art in js[col]:
					art['cnpjContrato'] = art['cnpj']
					art['cnpj'] = d['cnpj']
					
					ARTS.append(art)
			
			# Funcionario
			elif col == 'funcionarios':
				for func in js[col]:
					func['cnpj'] = d['cnpj']
					func['ativo'] = True
					FUNC.append(func)
					
			# Ex-Funcionario
			elif col == 'exfuncionarios':
				for func in js[col]:
					func['cnpj'] = d['cnpj']
					func['ativo'] = False
					FUNC.append(func)
			
			# Importação
			elif col == 'importacao':
				for imp in js[col]:
					q = {}
					q['cnpj'] = d['cnpj']
					q['tipo'] = col
					q['ano'] = imp['ano']
					q['qtd'] = imp['valor']
					
					QUAN.append(q)
			
			# Dominios
			elif col == 'dominios':
				for dom in js[col]:
					dom['cnpj'] = d['cnpj']
					SITE.append(dom)
			
			# Balanço Financeiro
			elif col == 'empresaBalancoFinanceiro':
				if 'balancosPatrimoniais' in js[col].keys():
					for balanco in js[col]['balancosPatrimoniais']:
						balanco['cnpj'] = d['cnpj']
						BALP.append(balanco)
				
				if 'demonstracoesResultados' in js[col].keys():
					for ebit in js[col]['demonstracoesResultados']:
						ebit['cnpj'] = d['cnpj']
						EBIT.append(ebit)
				
				if 'indicadoresFinanceiros' in js[col].keys():
					for finan in js[col]['indicadoresFinanceiros']:
						finan['cnpj'] = d['cnpj']
						FINA.append(finan)
			
			# Debitos PGFN
			elif col == 'debitosPgfnDau':
				for deb in js[col]:
					#deb['cnpj'] = d['cnpj']
					DEBT.append(deb)
					
			# Veiculos pesados
			elif col == 'veiculosPesados':
				for vei in js[col]:
					vei['cnpj'] = d['cnpj']
					VEIC.append(vei)
			
			# Infracoes
			elif col == 'autoInfracao':
				for multa in js[col]['infracoes']:
					multa['cnpj'] = d['cnpj']
					multa['tipo'] = 'autoInfracao'
					MULT.append(multa)
			
			# Atividade Financeira
			elif col == 'atividadeFinanceira':
				d['situacaoHabilitacao'] = js[col]['situacaoHabilitacao']
			
			# Imoveis
			elif col == 'imoveis':
				for imov in js[col]:
					imov['cnpj'] = d['cnpj']
					IMOV.append(imov)
			
			# Embargos Ibama
			elif col == 'ibamaEmbargos':
				for ibama in js[col]:
					
					infr = {}
					infr['cnpj'] = d['cnpj']
					infr['dataInfracao'] = ibama['dataInsercao']
					infr['infracao'] = ibama['descricaoInfracao']
					infr['logradouro'] = ibama['logradouro']
					infr['numeroProcesso'] = ibama['numeroInfracao']
					infr['numeroTad'] = ibama['numeroTad']
					infr['uf'] = ibama['uf']
					infr['tipo'] = 'ibamaEmbargos'
					
					MULT.append(infr)
			
			# Embargos Bacen
			elif col == 'bancoCentral':
				for embargo in js[col]['acordaos']:
					
					bacen = {}
					bacen['cnpj'] = d['cnpj']
					bacen['numeroProcesso'] = embargo['numeroProcesso']
					bacen['numeroRecurso'] = embargo['numeroRecurso']
					bacen['numeroAcordaoCRSFN'] = embargo['numeroAcordaoCRSFN']
					bacen['parte'] = embargo['parte']
					bacen['recurso'] = embargo['recurso']
					bacen['tipo'] = 'bancoCentral'
					
					MULT.append(bacen)
					
			# Aeronaves
			elif col == 'aeronaves':
				for aviao in js[col]:
					
					aero = {}
					aero['cnpj'] = d['cnpj']
					aero['anoFabricacao'] = aviao['ano']
					marca = aviao['fabricante'] + ' ' + aviao['modelo']
					aero['marcaModelo'] = marca
					aero['placa'] = aviao['matricula']
					aero['proprietario'] = aviao['proprietario']
					aero['operador'] = aviao['operador']
					aero['tipo'] = 'AERONAVE'
					
					VEIC.append(aero)
			
			# Universidades
			elif col == 'faculdades':
				for univ in js[col]:
					
					univ['cnpj'] = d['cnpj']
					
					UNIV.append(univ)
			
			# CEIS
			elif col == 'ceis':
				for emb in js[col]:
					
					debt = {}
					debt['cnpj'] = d['cnpj']
					debt['dataInfracao'] = emb['dataInicioSancao']
					debt['dataFimSancao'] = emb['dataFimSancao']
					debt['sancoesAplicadas'] = emb['fundamentacaoLegal']
					debt['uf'] = emb['ufOrgaoSancionador']
					debt['numeroProcesso'] = emb['numeroProcesso']
					debt['statusDebito'] = emb['tipoSancao']
					debt['origem'] = emb['orgaoSancionador']
					
					MULT.append(debt)
			
			# Postos de Combustiveis
			elif col == 'postosCombustiveis':
				pass
			
			# Empresas de Capital Aberto
			elif col == 'capitalAberto':
				if 'atividadePrincipal' in js[col].keys():
					pass
				
				if 'balancoPatrimonial' in js[col].keys():
					pass
				
				if 'cdNegociacao' in js[col].keys():
					d['codigoBolsa'] = js[col]['cdNegociacao']
				
				if 'cdPregao' in js[col].keys():
					pass
				
				if 'classificacaoSetorial' in js[col].keys():
					pass
				
				if 'demonstracaoResultado' in js[col].keys():
					pass
				
				if 'posicaoAcionaria' in js[col].keys():
					pass
				
				if 'site' in js[col].keys():
					d['site'] = js[col]['site']
					
			# Infos da CVM
			# Verificar um caso que tenha.
			elif col == 'cvm':											############
				print('Verificar essa entrada!\nEla não está mapeada')	## AJUSTAR##
																		############
			# Infos da CVM
			# Verificar um caso que tenha.
			elif col == 'cfc':											############
				print('Verificar essa entrada!\nEla não está mapeada')	## AJUSTAR##
																		############
			# CND Ibama
			elif col == 'ibamaCnd':
				for registro in js[col]:
					cnd={}
					cnd['cnpj'] = d['cnpj']
					cnd['dataEmissao'] = registro['emissao']
					cnd['dataValidade'] = registro['validade']
					cnd['descricaoSituacao'] = registro['situacao']
					cnd['numeroCertificacao'] = registro['certidao']
					cnd['tipo'] = 'ibama'
					CNDS.append(cnd)
			
			# Trabalho escravo
			elif col == 'mteTrabalhoEscravo':
				if js[col]['estabelecimentos'] is not None:
					d['trabalhoEscravo'] = True

	
	arquivo = './json/{}.xlsx'.format(d['cnpj'])
	writer = pd.ExcelWriter(arquivo)
	
	if d:
		df = pd.DataFrame([d])
		df.to_excel(excel_writer=writer, sheet_name='CADASTRAL',
					  header=True, index=False)
		
	if QUAN:
		df = pd.DataFrame(QUAN)
		df.to_excel(excel_writer=writer, sheet_name='QUANTITATIVO',
					  header=True, index=False)
		
	if CNAE:
		df = pd.DataFrame(CNAE)
		df.to_excel(excel_writer=writer,
					  sheet_name='CNAES',
					  header=True,
					  index=False)
		
	if EMPR:
		df = pd.DataFrame(EMPR)
		df.to_excel(excel_writer=writer,
					  sheet_name='EMPRESAS_RELACIONADAS',
					  header=True,
					  index=False)
		
	if TELS:
		df = pd.DataFrame(TELS)
		df.to_excel(excel_writer=writer,
				  sheet_name='TELEFONES',
				  header=True,
				  index=False)
		
	if INPI:
		df = pd.DataFrame(INPI)
		df.to_excel(excel_writer=writer,
					  sheet_name='PATENTES',
					  header=True,
					  index=False)
		
	if IMOV:
		df = pd.DataFrame(IMOV)
		df.to_excel(excel_writer=writer,
					  sheet_name='IMOVEIS',
					  header=True,
					  index=False)
		
	if CNDS:
		df = pd.DataFrame(CNDS)
		df.to_excel(excel_writer=writer,
					  sheet_name='CNDS_CERTIDOES',
					  header=True,
					  index=False)
		
	if ENDE:
		df = pd.DataFrame(ENDE)
		df.to_excel(excel_writer=writer,
					  sheet_name='ENDERECOS',
					  header=True,
					  index=False)
		
	if SINT:
		df = pd.DataFrame(SINT)
		df.to_excel(excel_writer=writer,
					  sheet_name='SINTEGRA',
					  header=True,
					  index=False)
		
	if DOAC:
		df = pd.DataFrame(DOAC)
		df.to_excel(excel_writer=writer,
					  sheet_name='DOACOES',
					  header=True,
					  index=False)
		
	if FILI:
		df = pd.DataFrame(FILI)
		df.to_excel(excel_writer=writer,
					  sheet_name='FILIAIS',
					  header=True,
					  index=False)
		
	if SOCI:
		df = pd.DataFrame(SOCI)
		df.to_excel(excel_writer=writer,
					  sheet_name='SOCIOS',
					  header=True, index=False)
		
	if BENE:
		df = pd.DataFrame(BENE)
		df.to_excel(excel_writer=writer,
					  sheet_name='BENEFICIARIOS',
					  header=True,
					  index=False)
		
	if ARTS:
		df = pd.DataFrame(ARTS)
		df.to_excel(excel_writer=writer,
					  sheet_name='ARTS',
					  header=True,
					  index=False)
		
	if FUNC:
		df = pd.DataFrame(FUNC)
		df.to_excel(excel_writer=writer,
					  sheet_name='FUNCIONARIOS',
					  header=True,
					  index=False)
		
	if SITE:
		df = pd.DataFrame(SITE)
		df.to_excel(excel_writer=writer,
					  sheet_name='DOMINIOS',
					  header=True,
					  index=False)
		
	if BALP:
		df = pd.DataFrame(BALP)
		df.to_excel(excel_writer=writer,
					  sheet_name='BALANCO',
					  header=True,
					  index=False)
		
	if EBIT:
		df = pd.DataFrame(EBIT)
		df.to_excel(excel_writer=writer,
					  sheet_name='EBITDA',
					  header=True,
					  index=False)
		
	if FINA:
		df = pd.DataFrame(FINA)
		df.to_excel(excel_writer=writer,
					  sheet_name='INFO_FINANCEIRA',
					  header=True,
					  index=False)
		
	if DEBT:
		df = pd.DataFrame(DEBT)
		df.to_excel(excel_writer=writer,
					  sheet_name='DEBITOS',
					  header=True,
					  index=False)
		
	if VEIC:
		df = pd.DataFrame(VEIC)
		df.to_excel(excel_writer=writer,
					  sheet_name='VEICULOS',
					  header=True,
					  index=False)
		
	if MULT:
		df = pd.DataFrame(MULT)
		df.to_excel(excel_writer=writer,
					  sheet_name='INFRACOES',
					  header=True,
					  index=False)
		
	if UNIV:
		df = pd.DataFrame(UNIV)
		df.to_excel(excel_writer=writer,
					  sheet_name='UNIVERSIDADES',
					  header=True,
					  index=False)
		

	del col_dic
	
	writer.save()
	
	
	return True


def trata_json_pf(js):
	
	d = {}
	
	IMOV = []
	ENDE = []
	TELS = []
	EMPR = []
	#JOBS = []
	NJOB = []
	IRPF = []
	TRAB = []
	PROC = []
	DOAC = []
	VEIC = []
	MULT = []
	DEBT = []
	
	# - - - -
	# tratamento das colunas que são string
	col_str = ['_id','cpf','cpfDataInscricao','dataNascimento','sexo',
				'situacaoCpf','idade','nome','nomeMae','falecido',
				  'falecidoConfirmado','servidorPublico']
	
	for col in col_str:
		if col in js.keys():
			d[col] = js[col]
		else:
			d[col] = None

	
	col_dic = ['nis','pis','cfo','cns','cfc','cfm','antt',
				'email','cpfMae','imoveis','endereco','cafir',
				'planosSaude','bolsaFamilia','qtdVeiculosPesados',
				'bancoCentral','ibamaEmbargos''transparencia',
				'susepCorretor','infoEleitorais','enderecoOutros',
				'debitosPgfnDau','anoFalecimento','doacaoEleitoral',
				'irpfRestituicao','profissaoNeoway','veiculosPesados',
				'incomePrediction','seguroDesemprego','telefones',
				'historicoFuncional','estabilidadeEmprego','autoInfracao',
				'participacaoSocietaria','enderecoEmpregoRaisNovo',
				'participacaoSocietariaRF','participacaoSocietariaUnico',
				'processoJudicialTotalizadores']
	
	# Checo se todas as colunas do json foram
	# contempladas no array de dados acima
	keys = js.keys()
	check = []
	
	for k in keys:
		if k not in col_dic:
			if k not in col_str:
				check.append(k)
	
	if check:
		print('os segiuntes campos não foram mapeados:\nFavor verificar\n\n')
		for k in check:
			print(k)
	
	
	for col in col_dic:
		if col in js.keys():
			
			
			# Imoveis CAFIR
			if col == 'cafir':
				if 'imoveis' in js[col].keys():
					for value in range(len(js[col]['imoveis'])):
						js[col]['imoveis'][value]['cpf'] = d['cpf']
						IMOV.append(js[col]['imoveis'][value])
			
			# Endereco
			elif col == 'endereco':
				js[col]['cpf'] = d['cpf']
				ENDE.append(js[col])
			
			# Endereco
			elif col == 'enderecoOutros':
				for end in js[col]:
					end['cpf'] = d['cpf']
					ENDE.append(end)
			
			# Telefones
			elif col == 'telefones':
				for tel in js[col]:
					tel['cpf'] = d['cpf']
					TELS.append(tel)
			
			# Eleitoral
			elif col == 'infoEleitorais':
				
				if 'enderecoVotacao' in js[col].keys():
					d['eleiEnderecoVotacao'] = js[col]['enderecoVotacao']
				
				if 'localVotacao' in js[col].keys():
					d['eleiLocalVotacao'] = js[col]['localVotacao']
					
				if 'municipio' in js[col].keys():
					d['eleiMunicipio'] = js[col]['municipio']
				
				if 'secao' in js[col].keys():
					d['eleiSecao'] = js[col]['secao']
					
				if 'titulo' in js[col].keys():
					d['eleiTitulo'] = js[col]['titulo']
					
				if 'uf' in js[col].keys():
					d['eleiUf'] = js[col]['uf']
					
				if 'zona' in js[col].keys():
					d['eleiZona'] = js[col]['zona']
			
			# Participacao Societaria RF
			elif col == 'participacaoSocietariaRF':
				for emp in js[col]:
					emp['cpf'] = d['cpf']
					emp['tipo'] = 'participacaoSocietariaRF'
					EMPR.append(emp)
			
			# Participacao Societaria
			elif col == 'participacaoSocietariaUnico':
				for emp in js[col]:
					emp['cpf'] = d['cpf']
					emp['tipo'] = 'participacaoSocietariaUnico'
					EMPR.append(emp)
			
			# Quantidade Processos
			elif col == 'processoJudicialTotalizadores':
				
				quan = {}
				quan['cpf'] = d['cpf']
				quan['valorTotal'] = js[col]['valorTotal']
				quan['valorTotalAtiva'] = js[col]['valorTotalAtiva']
				quan['valorTotalOutrasPartes'] = js[col]['valorTotalOutrasPartes']
				quan['valorTotalPassiva'] = js[col]['valorTotalPassiva']
				 
				for qt in js[col]['quantidades']:
					if qt['tipo'] == 'NUMERO DE PROCESSOS':
					
						quan['qtdAtivos'] = qt['qtdAtivos']
						quan['qtdOutrasPartes'] = qt['qtdOutrasPartes']
						quan['qtdParteAtiva'] = qt['qtdParteAtiva']
						quan['qtdPartePassiva'] = qt['qtdPartePassiva']
						quan['qtdTotal'] = qt['qtdTotal']
						
					PROC.append(quan)
			
			# Veiculos Pesados
			elif col == 'qtdVeiculosPesados':
				print('variavel não tratada!\nFavor verificar! '+col)
		
			# Cpf da Mãe
			elif col == 'cpfMae':
				d['cpfMae'] = js[col]
			
			# PIS
			elif col == 'pis':
				d['pis'] = js[col]
			
			# Historico Funcional
			elif col == 'historicoFuncional':
				
				for emprego in js[col]:
					emprego['cpf'] = d['cpf']
					TRAB.append(emprego)
			
			# Estabilidade emprego
			elif col == 'estabilidadeEmprego':
				d['estabilidadeEmprego'] = js[col]['faixa']
			
			# Estimativa receita
			elif col == 'incomePrediction':
				d['rendaEstimada'] = js[col]['incomeInterval']
			
			# Estimativa receita
			elif col == 'irpfRestituicao':
				for rest in js[col]['exercicios']:
					rest['cpf'] = d['cpf']
					IRPF.append(rest)
			
			# Seguro Desemprego
			elif col == 'seguroDesemprego':
				for desemp in js[col]:
					desemp['cpf'] = d['cpf']
					NJOB.append(desemp)
			
			# Endereço do trabalho
			elif col == 'enderecoEmpregoRaisNovo':
				print('variavel não tratada!\nFavor verificar! '+col)
			
			# Email
			elif col == 'email':
				d['email'] = js[col]
			
			# CFM
			elif col == 'cfm':
				d['cfmNro'] = js[col]['numero']
				d['cfmOrgao'] = js[col]['orgao']
				d['cfmSituacao'] = js[col]['situacao']
			
			# Conselho nacional de saude
			elif col == 'cns':
				print('variavel não tratada!\nFavor verificar! '+col)
			
			# Conselho nacional de saude
			elif col == 'planosSaude':
				if len(js[col])>0:
					d['planosSaude'] = True
			
			# Imoveis
			elif col == 'imoveis':
				for imov in js[col]:
					imov['cpf'] = d['cpf']
					IMOV.append(imov)
			
			# Doações
			elif col == 'doacaoEleitoral':
				for doa in js[col]['doacoes']:
					doa['cpf'] = d['cpf']
					DOAC.append(doa)
			
			# Veiculos pesados
			elif col == 'veiculosPesados':
				for vei in js[col]:
					vei['cpf'] = d['cpf']
					VEIC.append(vei)
			
			# ANTT
			elif col == 'antt':
				print('variavel não tratada!\nFavor verificar! '+col)
		
			# Profissao
			elif col == 'profissaoNeoway':
				d['profissao'] = js[col]
			
			# Participação societaria
			elif col == 'participacaoSocietaria':
				for emp in js[col]:
					emp['cpf'] = d['cpf']
					emp['tipo'] = 'participacaoSocietaria'
					EMPR.append(emp)
			
			# Infracoes
			elif col == 'autoInfracao':
				for multa in js[col]['infracoes']:
					multa['cpf'] = d['cpf']
					multa['tipo'] = 'autoInfracao'
					MULT.append(multa)
					
			# CFC
			elif col == 'cfc':
				print('variavel não tratada!\nFavor verificar! '+col)
			
			# NIS
			elif col == 'nis':
				d['nis'] = js[col]
			
			# Bolsa Familia
			elif col == 'bolsaFamilia':
				print('variavel não tratada!\nFavor verificar! '+col)
			
			# CFO
			elif col == 'cfo':
				print('variavel não tratada!\nFavor verificar! '+col)
			
			# ANo Falecimento
			elif col == 'anoFalecimento':
				d['anoFalecimento'] = js[col]
			
			# Embargos Bacen
			elif col == 'bancoCentral':
				for embargo in js[col]['acordaos']:
					
					bacen = {}
					bacen['cpf'] = d['cpf']
					bacen['numeroProcesso'] = embargo['numeroProcesso']
					bacen['numeroRecurso'] = embargo['numeroRecurso']
					bacen['numeroAcordaoCRSFN'] = embargo['numeroAcordaoCRSFN']
					bacen['parte'] = embargo['parte']
					bacen['recurso'] = embargo['recurso']
					bacen['tipo'] = 'bancoCentral'
					
					MULT.append(bacen)
			
			# Susep
			elif col == 'susepCorretor':
				print('variavel não tratada!\nFavor verificar! '+col)
			
			# Debitos PGFN
			elif col == 'debitosPgfnDau':
				for deb in js[col]:
					#deb['cnpj'] = d['cnpj']
					DEBT.append(deb)
			
			# Embargos Ibama
			elif col == 'ibamaEmbargos':
				for ibama in js[col]:
					
					infr = {}
					infr['cpf'] = d['cpf']
					infr['dataInfracao'] = ibama['dataInsercao']
					infr['infracao'] = ibama['descricaoInfracao']
					infr['logradouro'] = ibama['logradouro']
					infr['numeroProcesso'] = ibama['numeroInfracao']
					infr['numeroTad'] = ibama['numeroTad']
					infr['uf'] = ibama['uf']
					infr['tipo'] = 'ibamaEmbargos'
					
					MULT.append(infr)
			
			# Transparencia
			elif col == 'transparencia':
				print('variavel não tratada!\nFavor verificar! '+col)
			
			# Servidor Publico
			elif col == 'servidorPublico':
				d['servidorPublico'] = js[col]
		
	
	arquivo = './json/{}.xlsx'.format(d['cpf'])
	writer = pd.ExcelWriter(arquivo)
	
	if d:
		df = pd.DataFrame([d])
		df.to_excel(excel_writer=writer, sheet_name='CADASTRAL',
					  header=True, index=False)
		
	if IRPF:
		df = pd.DataFrame(IRPF)
		df.to_excel(excel_writer=writer, sheet_name='IRPF',
					  header=True, index=False)
		
	if EMPR:
		df = pd.DataFrame(EMPR)
		df.to_excel(excel_writer=writer,
					  sheet_name='SOCIEDADE',
					  header=True,
					  index=False)
		
	if TELS:
		df = pd.DataFrame(TELS)
		df.to_excel(excel_writer=writer,
				  sheet_name='TELEFONES',
				  header=True,
				  index=False)
		
	if IMOV:
		df = pd.DataFrame(IMOV)
		df.to_excel(excel_writer=writer,
					  sheet_name='IMOVEIS',
					  header=True,
					  index=False)
		
	if ENDE:
		df = pd.DataFrame(ENDE)
		df.to_excel(excel_writer=writer,
					  sheet_name='ENDERECOS',
					  header=True,
					  index=False)
		
	if DOAC:
		df = pd.DataFrame(DOAC)
		df.to_excel(excel_writer=writer,
					  sheet_name='DOACOES',
					  header=True,
					  index=False)
		
	if DEBT:
		df = pd.DataFrame(DEBT)
		df.to_excel(excel_writer=writer,
					  sheet_name='DEBITOS',
					  header=True,
					  index=False)
		
	if VEIC:
		df = pd.DataFrame(VEIC)
		df.to_excel(excel_writer=writer,
					  sheet_name='VEICULOS',
					  header=True,
					  index=False)
		
	if MULT:
		df = pd.DataFrame(MULT)
		df.to_excel(excel_writer=writer,
					  sheet_name='INFRACOES',
					  header=True,
					  index=False)

		
	if NJOB:
		df = pd.DataFrame(NJOB)
		df.to_excel(excel_writer=writer,
					  sheet_name='SEGURO_DESEMPREGO',
					  header=True,
					  index=False)
		
	if TRAB:
		df = pd.DataFrame(TRAB)
		df.to_excel(excel_writer=writer,
					  sheet_name='EMPREGOS',
					  header=True,
					  index=False)
					  
	if PROC:
		df = pd.DataFrame(PROC)
		df.to_excel(excel_writer=writer,
					  sheet_name='PROCESSOS',
					  header=True,
					  index=False)
	
	del col_dic
	
	writer.save()
	
	return False