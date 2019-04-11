# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 11:37:57 2019

@author: fernando.barontini
Módulo de Tratamento da String da Serasa - Relato

Funcoes implementadas:
	infere_cnpj
	get_faturamento_presumido
	get_pontuacao
	get_ultimas_consultas
	get_pefin
	get_refin
	get_resumo_concentre
	get_quantidade_consultas
	get_protesto_concentre
	get_judicial_concentre
	get_rj_falencia
	
"""
import re
import numpy as np
import pandas as pd
pd.set_option('max_columns',50)

#s = ['#INI0138IP20RTOKM2        01436521822N            03S  000000000000000                                                                    #BLC3639#L01000002                                                                               014365218 IPRC           P8FP                                1S1  2SITUACAO DO CNPJ EM 06/01/2019: ATIVA                                                      #L010101DUNAS SOLUCOES                                              2019011713:55:03  CNPJ: 14.365.218/0001-5420190113 0022920917820170523#L010102RB FLEX INDUSTRIA DE MAQUINAS LTDA EPP                                014365218                                                            35225676159SOCIEDADE EMPRESARIA LIMITADA                                                             0206#L010103R AMPARO 389 - QTA DA PAINEIRA                                        QTA DA PAINEIRA               R AMPARO 389                                                                    #L010104SAO PAULO                     SP0031510600000000000000000000000                                                                                                                                                #L0101052011061320110713IND MECANICA LEVE                                     I11030000000000000000000000286910020190112#L300201020190113014365218000154RB FLEX INDUSTRIA DE MAQUINAS LTDA EPP                                                    20190117135503#L300202020190117+000001100027802410280#L300203020190117FATURAMENTO ANUAL ESTIMADO DA EMPRESA NO ULTIMO EXERCICIO SOCIAL, CALCULADO POR                     #L300203020190117MEIO DAS MAIS AVANCADAS TECNICAS DE MODELAGEM MATEMATICA.                                           #L02010200100000000000000000   000420190117#L0201030-6 MESES:    000000020190117#L0201036MES-1ANO:    000300020190117#L0201031-3ANOS:      000600020190117#L0201033-5ANOS:      000100020190117#L0201035-10ANOS:     000000020190117#L020103+10ANOS:      000000020190117#L020103INAT.:        000000020190117#L0301011901JAN000000A               #L0301011812DEZ003000A               #L0301011811NOV010000A               #L0301011810OUT005000A               #L0301011809SET003000A               #L0301011808AGO007000A               #L0301011807JUL005000A               #L0301011806JUN006000A               #L0301011805MAI002000A               #L0301011804ABR002000A               #L0301011803MAR006000A               #L0301011802FEV008000A               #L0301011801JAN001000A               #L0301011712DEZ008000A               #L03010220181205APEX LATIN AMERICA IND MAQ EQUIPAME0001013677173 S#L03010220181203ETIRAMA INDUSTRIA DE MAQUINAS LTDA 0001001400742 S#L03010220181203RNX FACTORING LTDA                 0001006696071 S#L03010220181127IBRAM INDUSTRIA BRASILEIRA DE MAQUI0001047665559 S#L03010220181123KAPITAL FACTORING SOCIEDADE DE FOME0002060202843 S#L020105PONTUAL       1810OUT0000000000000000000020190117#L0201058-15          1810OUT0000000000000000000020190117#L02010516-30         1810OUT0000000000000000000020190117#L02010531-60         1810OUT0000000000000000000020190117#L020105+60           1810OUT0000000000000000000020190117#L020105PMA           1810OUT0000000000000000000020190117#L020105A VISTA       1810OUT0000000000388000000020190117#L020105PONTUAL       1806JUN0000000000496016000020190117#L0201058-15          1806JUN0000000000000000000020190117#L02010516-30         1806JUN0000000000000000000020190117#L02010531-60         1806JUN0000000000000000000020190117#L020105+60           1806JUN0000000002691084000020190117#L020105PMA           1806JUN0000000000000063300020190117#L020105A VISTA       1806JUN0000000000000000000020190117#L020105PONTUAL       1804ABR0000000000000000000020190117#L0201058-15          1804ABR0000000000000000000020190117#BLC3807#L02010516-30         1804ABR0000000002026100000020190117#L02010531-60         1804ABR0000000000000000000020190117#L020105+60           1804ABR0000000000000000000020190117#L020105PMA           1804ABR0000000000000026500020190117#L020105A VISTA       1804ABR0000000000000000000020190117#L020105PONTUAL       1802FEV0000000000000000000020190117#L0201058-15          1802FEV0000000000000000000020190117#L02010516-30         1802FEV0000000000628029000020190117#L02010531-60         1802FEV0000000001570071000020190117#L020105+60           1802FEV0000000000000000000020190117#L020105PMA           1802FEV0000000000000037700020190117#L020105A VISTA       1802FEV0000000000000000000020190117#L020105PONTUAL       1801JAN0000000000000000000020190117#L0201058-15          1801JAN0000000000720077000020190117#L02010516-30         1801JAN0000000000221023000020190117#L02010531-60         1801JAN0000000000000000000020190117#L020105+60           1801JAN0000000000000000000020190117#L020105PMA           1801JAN0000000000000011200020190117#L020105A VISTA       1801JAN0000000000000000000020190117#L020105PONTUAL       1712DEZ0000000000669021000020190117#L0201058-15          1712DEZ0000000002562079000020190117#L02010516-30         1712DEZ0000000000000000000020190117#L02010531-60         1712DEZ0000000000000000000020190117#L020105+60           1712DEZ0000000000000000000020190117#L020105PMA           1712DEZ0000000000000008100020190117#L020105A VISTA       1712DEZ0000000000000000000020190117#L020405PONTUAL       00000000011650000000#L0204058-15          00000000032820000000#L02040516-30         00000000028750000000#L02040531-60         00000000015700000000#L020405+60           00000000026910000000#L020405A VISTA       00000000003880000000#L0201061805MAI0000000000000000000000049600020190117#L0201061804ABR0000000000000000000000000000020190117#L0201061803MAR0000000000000000000000166300020190117#L0201061802FEV0000000000000000000000305400020190117#L0201061801JAN0000000000000000000000202600020190117#L0201061712DEZ0000000000000000000000134800020190117#L020108PONTUAL       000002001720190117#L0201088-15          000003002520190117#L02010816-30         000004003320190117#L02010831-60         000001000820190117#L020108+60           000002001720190117#L020108A VISTA       000001000020190117#L020107ULTIMA COMPRA 201805100000000000496000000000122600020190117#L020107MAIOR FATURA  201801190000000002026000000000146900020190117#L020107MAIOR ACUMULO 201801190000000002026000000000137300020190117#L04010100000000100000000120181105NOTA FISCAL N0000000000346202461          IGUS                                                    NF IPZ0V0487431432014365218                                                                            0000000000346A#L040201RD FLEX INDUSTRIA DE MAQUINAS                                         #L040201RB FLEX INDUSTRIA DE MAQUINA                                          #L040201RB FLEX INDUSTRIA DE MAQUINAS LTDA                                    #L040201RB FLEX IND DE MAQUINAS LTDA                                          #L040201OUTRAS                                                                #L040202000000001DIVIDA VENCIDA             OUT1018OUT1018R$ 0000000001500TRANSPORTADORA          000000000150007 #L040202000000051PROTESTO                   JUL0718JAN0119R$ 0000000001644SAO PAULO           SPO 000000015776303 #L04070100000000120181024DEV            R$ 000000000150015769187399    TRANSPORTADORA    DS IPZ050476250535014365218                                                                                                            A#L04030100000005120181226R$ 000000000164409SAO PAULO                     SP                                Z1 IPZ0A0277373004014365218                                                                                      #BLC3614#L04030100000005120181223R$ 000000000076006SAO PAULO                     SP                                Z1 IPZ0A0277228965014365218                                                                                      #L04030100000005120181210R$ 000000000265506SAO PAULO                     SP                                Z1 IPZ0A0276494391014365218                                                                                      #L04030100000005120181123R$ 000000000744005SAO PAULO                     SP                                Z1 IPZ0A0276071741014365218                                                                                      #L04030100000005120181114R$ 000000000018708SAO PAULO                     SP                                Z1 IPZ0A0275428013014365218                                                                                      #L041099=== NADA CONSTA PARA O CNPJ CONSULTADO ===                                     #L02011300050003000300030000028000420190117#L0201140-6 MESES:    0000028    20190117#L0201146MES-1ANO:    0002028    20190117#L0201141-3ANOS:      0003028    20190117#L0201143-5ANOS:      0000028    20190117#L0201145-10ANOS:     0000028    20190117#L020114+10ANOS:      0000028    20190117#L020114INAT.:        0000028    20190117#L020115PONTUAL       1806JUN0000000000496100002820190117#L0201158-15          1806JUN0000000000000000002820190117#L02011516-30         1806JUN0000000000000000002820190117#L02011531-60         1806JUN0000000000000000002820190117#L020115+60           1806JUN0000000000000000002820190117#L020115PMA           1806JUN0000000000000000002820190117#L020115A VISTA       1806JUN0000000000000000002820190117#L020115PONTUAL       1804ABR0000000000000000002820190117#L0201158-15          1804ABR0000000000000000002820190117#L02011516-30         1804ABR0000000002026100002820190117#L02011531-60         1804ABR0000000000000000002820190117#L020115+60           1804ABR0000000000000000002820190117#L020115PMA           1804ABR0000000000000026502820190117#L020115A VISTA       1804ABR0000000000000000002820190117#L020115PONTUAL       1801JAN0000000000000000002820190117#L0201158-15          1801JAN0000000000720100002820190117#L02011516-30         1801JAN0000000000000000002820190117#L02011531-60         1801JAN0000000000000000002820190117#L020115+60           1801JAN0000000000000000002820190117#L020115PMA           1801JAN0000000000000008002820190117#L020115A VISTA       1801JAN0000000000000000002820190117#L020115PONTUAL       1712DEZ0000000000669040002820190117#L0201158-15          1712DEZ0000000000992060002820190117#L02011516-30         1712DEZ0000000000000000002820190117#L02011531-60         1712DEZ0000000000000000002820190117#L020115+60           1712DEZ0000000000000000002820190117#L020115PMA           1712DEZ0000000000000008302820190117#L020115A VISTA       1712DEZ0000000000000000002820190117#L020415PONTUAL       00000000011650280000#L0204158-15          00000000017120280000#L02041516-30         00000000020260280000#L02041531-60         00000000000000280000#L020415+60           00000000000000280000#L020415A VISTA       00000000000000280000#L0201161805MAI0000000000000000000000049602820190117#L0201161803MAR0000000000000000000000000002820190117#L0201161802FEV0000000000000000000000202602820190117#L0201161801JAN0000000000000000000000202602820190117#L0201161712DEZ0000000000000000000000072002820190117#L020117ULTIMA COMPRA 201805100000000000496000000000108002820190117#L020117MAIOR FATURA  201801190000000002026000000000137302820190117#L020117MAIOR ACUMULO 201801190000000002026000000000137302820190117#BLC3656#L020125PONTUAL       1901JAN00000000496080740000        #L0201258-15          1901JAN00000000165000250000        #L02012516-30         1901JAN00000000007600010000        #L02012531-60         1901JAN00000000000000000000        #L020125+60           1901JAN00000000000000000000        #L020125PMA           1901JAN00000000000000031000        #L020125A VISTA       1901JAN00000000000000000000        #L020125PONTUAL       1812DEZ00000001219080980000        #L0201258-15          1812DEZ00000000021400020000        #L02012516-30         1812DEZ00000000005310000000        #L02012531-60         1812DEZ00000000000000000000        #L020125+60           1812DEZ00000000000000000000        #L020125PMA           1812DEZ00000000000000003000        #L020125A VISTA       1812DEZ00000000000000000000        #L020125PONTUAL       1811NOV00000001580720980000        #L0201258-15          1811NOV00000000006640000000        #L02012516-30         1811NOV00000000021400020000        #L02012531-60         1811NOV00000000000000000000        #L020125+60           1811NOV00000000000000000000        #L020125PMA           1811NOV00000000000000002000        #L020125A VISTA       1811NOV00000000057000000000        #L020125PONTUAL       1810OUT00000001574150900000        #L0201258-15          1810OUT00000000000000000000        #L02012516-30         1810OUT00000000173400100000        #L02012531-60         1810OUT00000000000000000000        #L020125+60           1810OUT00000000000000000000        #L020125PMA           1810OUT00000000000000028000        #L020125A VISTA       1810OUT00000000000000000000        #L020125PONTUAL       1809SET00000001292760870000        #L0201258-15          1809SET00000000171900120000        #L02012516-30         1809SET00000000021400010000        #L02012531-60         1809SET00000000000000000000        #L020125+60           1809SET00000000000000000000        #L020125PMA           1809SET00000000000000015000        #L020125A VISTA       1809SET00000000000000000000        #L020125PONTUAL       1808AGO00000000980430980000        #L0201258-15          1808AGO00000000021400020000        #L02012516-30         1808AGO00000000000000000000        #L02012531-60         1808AGO00000000000000000000        #L020125+60           1808AGO00000000000000000000        #L020125PMA           1808AGO00000000000000003000        #L020125A VISTA       1808AGO00000000000000000000        #L020125PONTUAL       1807JUL00000000994270970000        #L0201258-15          1807JUL00000000005040000000        #L02012516-30         1807JUL00000000021400030000        #L02012531-60         1807JUL00000000000000000000        #L020125+60           1807JUL00000000000000000000        #L020125PMA           1807JUL00000000000000004000        #L020125A VISTA       1807JUL00000000000000000000        #L020125PONTUAL       1806JUN00000001178120970000        #L0201258-15          1806JUN00000000000000000000        #L02012516-30         1806JUN00000000030850030000        #L02012531-60         1806JUN00000000000000000000        #L020125+60           1806JUN00000000000000000000        #L020125PMA           1806JUN00000000000000004000        #L020125A VISTA       1806JUN00000000000000000000        #L020125PONTUAL       1805MAI00000000835690950000        #L0201258-15          1805MAI00000000034520040000        #L02012516-30         1805MAI00000000007110010000        #L02012531-60         1805MAI00000000000000000000        #L020125+60           1805MAI00000000000000000000        #L020125PMA           1805MAI00000000000000007000        #L020125A VISTA       1805MAI00000000000000000000        #L020125PONTUAL       1804ABR00000000889320950000        #BLC3127#L0201258-15          1804ABR00000000021400020000        #L02012516-30         1804ABR00000000020810030000        #L02012531-60         1804ABR00000000000000000000        #L020125+60           1804ABR00000000000000000000        #L020125PMA           1804ABR00000000000000007000        #L020125A VISTA       1804ABR00000000000000000000        #L020125PONTUAL       1803MAR00000000735790950000        #L0201258-15          1803MAR00000000011400010000        #L02012516-30         1803MAR00000000027320040000        #L02012531-60         1803MAR00000000000000000000        #L020125+60           1803MAR00000000000000000000        #L020125PMA           1803MAR00000000000000009000        #L020125A VISTA       1803MAR00000000000000000000        #L020125PONTUAL       1802FEV00000000795130950000        #L0201258-15          1802FEV00000000007200010000        #L02012516-30         1802FEV00000000038270040000        #L02012531-60         1802FEV00000000000000000000        #L020125+60           1802FEV00000000000000000000        #L020125PMA           1802FEV00000000000000009000        #L020125A VISTA       1802FEV00000000000000000000        #L020125PONTUAL       1801JAN00000000902270960000        #L0201258-15          1801JAN00000000028600030000        #L02012516-30         1801JAN00000000005470010000        #L02012531-60         1801JAN00000000000000000000        #L020125+60           1801JAN00000000000000000000        #L020125PMA           1801JAN00000000000000005000        #L020125A VISTA       1801JAN00000000000000000000        #L020125PONTUAL       1712DEZ00000000647691000000        #L0201258-15          1712DEZ00000000000000000000        #L02012516-30         1712DEZ00000000000000000000        #L02012531-60         1712DEZ00000000000000000000        #L020125+60           1712DEZ00000000000000000000        #L020125PMA           1712DEZ00000000000000000000        #L020125A VISTA       1712DEZ00000000000000000000        #L020425PONTUAL       00000014121500000000#L0204258-15          00000000494500000000#L02042516-30         00000000380340000000#L02042531-60         00000000000000000000#L020425+60           00000000000000000000#L020425A VISTA       00000000057000000000#L0201261901JAN00000000546840000000499044000        #L0201261812DEZ00000000228050000000565879000        #L0201261811NOV00000000005310000000515183000        #L0201261810OUT00000000000000000000499466000        #L0201261809SET00000000152000000000405724000        #L0201261808AGO00000000014010000000443523000        #L0201261807JUL00000000000000000000441249000        #L0201261806JUN00000000000000000000379342000        #L0201261805MAI00000000000000000000397357000        #L0201261804ABR00000000000000000000439282000        #L0201261803MAR00000000013700000000361953000        #L0201261802FEV00000000017320000000306468000        #L0201261801JAN00000000024070000000296506000        #L0201261712DEZ00000000000000000000311469000        #L020127ULTIMA COMPRA 2019011100000000065000000000007750000        #L020127MAIOR FATURA  2018121700000000882020000000078090000        #L020127MAIOR ACUMULO 2018121700000004714610000000333494000        #FIM9999']

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def to_int(x):
	# converte para inteiro o valor
	x = re.sub('[^0-9]','',x)
	try:
		x = int(x)
	except:
		x = -1
		
	return x

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def to_date(x):
	# converte para inteiro o valor
	x = re.sub('[^0-9]','',x)
	
	if  len(x) == 8:
		x = '{dia}/{mes}/{ano}'.format(	dia=x[6:],
										mes=x[4:6],
										ano=x[0:4])
	elif  len(x) == 6:
		x = '{dia}/{mes}/{ano}'.format(	dia=x[0:2],
										mes=x[2:4],
										ano=x[4:])
	else:
		
		x = None
		
	return x


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def infere_cnpj(cnpj):
	# função para inferir o cnpj
	
	if len(cnpj) == 8:
		cnpj = cnpj + '0001'
		cnpj = np.array([int(x) for x in cnpj])
		
		mult1 = np.array([5,4,3,2,9,8,7,6,5,4,3,2])
		mult2 = np.array([6,5,4,3,2,9,8,7,6,5,4,3,2])
		
		
		soma = np.sum(cnpj*mult1)%11
		dig1 = 0 if soma < 2 else 11-soma
		
		cnpj = np.append(cnpj,dig1)
		soma = np.sum(cnpj*mult2)%11
		dig2 = 0 if soma < 2 else 11-soma
		
		cnpj = np.append(cnpj,dig2)
		
		cnpj = ''.join([str(x) for x in cnpj])
	
	else:
		print('Digite um cnpj válido, com as 8 primeiras posições')
	
	return cnpj


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_faturamento_presumido(s):
	# trago a informação do faturamento
	# presumido do cliente no formato int
	target = '#L300202'
	ini, fim = 18, 26
	i = s.find(target)
	
	if i != -1:
		faturamento = s[i+ini:i+fim]
		faturamento = to_int(faturamento)
	else:
		faturamento = 0
	
	
	return faturamento


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_pontuacao(s):
	# trago a pontuacao do serasa
	target = '#L300202'
	ini, fim = 26, 30
	i = s.find(target)
	
	if i != -1:
		score = s[i+ini:i+fim]
		score = to_int(score)
	else:
		score = -1
	
	return score


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_ultimas_consultas(s):
	# trago a informação das ultimas consultas de outros clientes
	# e fornecedores. Aqui eu consigo extrair o CNPJ da empresa
	# que consultou o mesmo CNPJ que a Exten.
	target = '#L030102'
	i = s.find(target)
	a,b,c,d,fim = 8, 16, 51, 56,64
	consultas = []
	while i != -1:
		dic = {}
		dic['data_consulta'] = to_date(s[i+a:i+b])
		dic['nome_empresa'] = s[i+b:i+c].strip()
		dic['cnpj_empresa'] = s[i+d:i+fim]
		dic['cnpj_inferido'] = infere_cnpj(s[i+d:i+fim])
		
		i = s.find(target,i+1)
		consultas.append(dic)
	
	if len(consultas) > 0:
		consultas = pd.DataFrame(consultas)
	
	return consultas


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_resumo_concentre(s):
	
	target = '#L040202'
	
	a,b,c,d,e =  5,  9, 36, 39, 43
	f,g,h,i,j = 46, 50, 53, 66, 86
	k,l, m = 90, 103, 105
	
	consolidado = []
	t = s.find(target)
	
	while t != -1:
		t += 8
		dic = {}
		dic['quantidade'] = to_int(s[t+a:t+b])
		dic['grupo'] = s[t+b:t+c].strip()
		dic['mes_inicio'] = s[t+c:t+d]
		dic['data_inicio'] = to_date('01'+s[t+d:t+e])
		dic['mes_fim'] = s[t+e:t+f]
		dic['data_fim'] = to_date('01'+s[t+f:t+g])
		dic['moeda'] = s[t+g:t+h].strip()
		dic['valor'] = float(to_int(s[t+h:t+i]))
		dic['origem'] = s[t+i:t+j].strip()
		dic['agencia'] = s[t+j:t+k].strip()
		dic['total'] = float(to_int(s[t+k:t+l]))
		dic['natureza'] = s[t+l:t+m].strip()
				
		t = s.find(target,t+1)
		consolidado.append(dic)
	
	if len(consolidado) > 0:
		consolidado = pd.DataFrame(consolidado)
	
	return consolidado


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_pefin(s):
	
	target = '#L040101'
	consolidado = []
	t = s.find(target)
	
	#localizadores
	a, b, c, d, e =   8,  17,  26,  34,  46
	f, g, h, i, j =  47,  60,  76,  96, 100
	k, l, m, n, o = 132, 135, 159, 235, 248
	
	
	while t != -1:
		
		dic = {}
		
		dic['qtd_ocorrencia'] 			= to_int(s[t+a:t+b])
		dic['qtd_ultima_ocorrencia'] 	= to_int(s[t+b:t+c])
		dic['data_ocorrencia'] 			= to_date(s[t+c:t+d])
		dic['titulo'] 					= s[t+d:t+e].strip()
		dic['avalista'] 				= s[t+e:t+f].strip()
		dic['valor_pefin'] 				= float(to_int(s[t+f:t+g]))
		dic['contrato'] 				= s[t+g:t+h].strip()
		dic['origem'] 					= s[t+h:t+i].strip()
		dic['filial'] 					= s[t+i:t+j].strip()
		dic['msg'] 						= s[t+j:t+k].strip()
		dic['natureza'] 				= s[t+k:t+l].strip()
		dic['reservado'] 				= s[t+l:t+m].strip()
		dic['outros'] 					= s[t+m:t+n].strip()
		dic['valor_total_pefin'] 		= to_int(s[t+n:t+o])

		t = s.find(target, t+1)
		consolidado.append(dic)
	
	if len(consolidado) > 0:
		consolidado = pd.DataFrame(consolidado)
		
	return consolidado



# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_refin(s):
	
	target = '#L040102'
	consolidado = []
	t = s.find(target)
	
	#localizadores
	a, b, c, d, e =   8,  17,  26,  34,  46
	f, g, h, i, j =  47,  60,  76,  96, 100
	k, l, m, n, o = 132, 135, 159, 235, 248
	
	
	while t != -1:
		
		dic = {}
		
		dic['qtd_ocorrencia'] 			= to_int(s[t+a:t+b])
		dic['qtd_ultima_ocorrencia'] 	= to_int(s[t+b:t+c])
		dic['data_ocorrencia'] 			= to_date(s[t+c:t+d])
		dic['titulo'] 					= s[t+d:t+e].strip()
		dic['avalista'] 				= s[t+e:t+f].strip()
		dic['valor_pefin'] 				= float(to_int(s[t+f:t+g]))
		dic['contrato'] 				= s[t+g:t+h].strip()
		dic['origem'] 					= s[t+h:t+i].strip()
		dic['filial'] 					= s[t+i:t+j].strip()
		dic['msg'] 						= s[t+j:t+k].strip()
		dic['natureza'] 				= s[t+k:t+l].strip()
		dic['reservado'] 				= s[t+l:t+m].strip()
		dic['outros'] 					= s[t+m:t+n].strip()
		dic['valor_total_pefin'] 		= to_int(s[t+n:t+o])

		t = s.find(target, t+1)
		consolidado.append(dic)
	
	if len(consolidado) > 0:
		consolidado = pd.DataFrame(consolidado)
		
	return consolidado


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_quantidade_consultas(s):
	
	target = '#L030101'
	t = s.find(target)
	
	consolidado = []
	a, b, c, d =   8, 12, 15, 18
	e, f, g    =  21, 22, 37
	
	while t != -1:
		
		dic = {}
		dic['data_consulta'] = to_date('20'+s[t+a:t+b]+'01')
		dic['mes_consulta']	 = s[t+b:t+c].strip()
		dic['qt_consultas']	 = to_int(s[t+c:t+d])
		dic['qt_consultas_banco'] = to_int(s[t+d:t+e])
		dic['obs']			 = s[t+e:t+f].strip()
		dic['outros']		 = s[t+f:t+g].strip()
	
		t = s.find(target, t+1)
		consolidado.append(dic)
	
	if len(consolidado) > 0:
		consolidado = pd.DataFrame(consolidado)
	
	return consolidado


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_protesto_concentre(s):
	
	target = '#L040301'
	t = s.find(target)
	
	consolidado = []
	a, b, c, d = 8, 17, 25, 28
	e, f, g, h = 41, 43, 73, 75
	i, j = 107, 220

	
	while t != -1:
		
		dic = {}
		dic['qtd_ocorrencias'] 	 = to_int(s[t+a:t+b])
		dic['data_ocorrencia']	 = to_date(s[t+b:t+c])
		dic['moeda']	 		 = s[t+c:t+d].strip()
		dic['valor']		 = float(to_int(s[t+d:t+e]))
		dic['cartorio']		 = s[t+e:t+f].strip()
		dic['cidade']		 = s[t+f:t+g].strip()
		dic['uf']			 = s[t+g:t+h].strip()
		dic['outros']		 = s[t+i:t+j].strip()
		#dic['outros_b']		 = s[t+f:t+g].strip()
		#dic['outros_c']		 = s[t+f:t+g].strip()
	
		t = s.find(target, t+1)
		consolidado.append(dic)
	
	if len(consolidado) > 0:
		consolidado = pd.DataFrame(consolidado)
	
	return consolidado


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_judicial_concentre(s):
	
	target = '#L040401'
	t = s.find(target)
	
	consolidado = []
	a, b, c, d =  8,  17,  25,  46
	e, f, g, h = 49,  62,  64,  68
	i, j, k, l = 98, 100, 132, 236


	
	while t != -1:
		
		dic = {}
		dic['qtd_ocorrencias'] 	 = to_int(s[t+a:t+b])
		dic['data_ocorrencia']	 = to_date(s[t+b:t+c])
		dic['natureza']	 		 = s[t+c:t+d].strip()
		dic['moeda']			 = s[t+d:t+e].strip()
		dic['valor']			 = float(to_int(s[t+e:t+f]))
		dic['distrito']			 = s[t+f:t+g].strip()
		dic['vara_civel']		 = s[t+g:t+h].strip()
		dic['cidade']			 = s[t+i:t+j].strip()
		dic['uf']				 = s[t+j:t+k].strip()
		dic['outros']			 = s[t+k:t+l].strip()
	
		t = s.find(target, t+1)
		consolidado.append(dic)
	
	if len(consolidado) > 0:
		consolidado = pd.DataFrame(consolidado)
	
	return consolidado


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_rj_falencia(s):
	
	target='#L040601'
	t = s.find(target)

	consolidado = []
	a, b, c, d = 13, 17, 25, 46
	e, f, g, h, i = 50, 54, 84, 86, 114

	
	while t != -1:
		
		dic = {}
		dic['qtd_ocorrencias'] 	 = to_int(s[t+a:t+b])
		dic['data_ocorrencia']	 = to_date(s[t+b:t+c])
		dic['tipo']	 			 = s[t+c:t+d].strip()
		dic['origem']			 = s[t+d:t+e].strip()
		dic['vara_civel']		 = s[t+e:t+f].strip()
		dic['cidade']			 = s[t+f:t+g].strip()
		dic['uf']		 		 = s[t+g:t+h].strip()
		dic['outros']			 = s[t+h:t+i].strip()
	
		t = s.find(target, t+1)
		consolidado.append(dic)
	
	if len(consolidado) > 0:
		consolidado = pd.DataFrame(consolidado)
	
	return consolidado


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_antecessores(s):
	# encontro o nome dos antecessores
	target='#L010116'
	t = s.find(target)

	consolidado = []
	a, b, c, d = 8, 78, 79, 87
	
	while t != -1:
		
		dic = {}
		dic['nome'] 			 = s[t+a:t+b].strip()
		dic['data_ocorrencia']	 = to_date(s[t+c:t+d])

		t = s.find(target, t+1)
		consolidado.append(dic)
	
	if len(consolidado) > 0:
		consolidado = pd.DataFrame(consolidado)
	
	return consolidado

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def get_atividade(s):
	
	target='#L010105'
	i = s.find(target)
	if i != -1:
		ativ = s[i:i+120]
	
	
	return ativ
	

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
'''
def validacao():
	ar = []
	
	i = string.find('#')
	while i != -1:
	    
	    if i == -1:
	        pass
	    else:
	        i = string.find('#',i+1)
	        ar.append(string[i:i+8])


def validacao2():
	
	df = pd.read_excel('strings.xlsx')
	
	d = {}
	for _ ,v in df.iterrows():
	    i = v['StringConsulta'].find('#')
	    ar = []
	    while i != -1:
	    
	        if i == -1:
	            pass
	        else:
	            i = v['StringConsulta'].find('#',i+1)
	            ar.append(v['StringConsulta'][i:i+8])
	    
	    ar.pop(ar.index(''))
	    
	    for i in ar:
	        if i in d.keys():
	            d[i] += 1
	        else:
	            d[i] = 1
'''


def varre(s):
	
	print('#','-'*60, '#')
	print('#',28*'-' + 'Inicio' + 26*'-','#')
	print('#','-'*60, '#')
	# ---------------------------------
	print('\nFaturamento presumido:')
	print(get_faturamento_presumido(s))
	# ---------------------------------
	print('\n\nPontuação:')
	print(get_pontuacao(s))
	# ---------------------------------
	print('\n\nUltimas consultas:')
	print(get_ultimas_consultas(s))
	# ---------------------------------
	print('\n\nPefin:')
	print(get_pefin(s))
	# ---------------------------------
	print('\n\nRefin:')
	print(get_refin(s))
	# ---------------------------------
	print('\n\nResumo concentre:')
	print(get_resumo_concentre(s))
	# ---------------------------------
	print('\n\nQuantidade consultas:')
	print(get_quantidade_consultas(s))
	# ---------------------------------
	print('\n\nQuantidade protestos:')
	print(get_protesto_concentre(s))
	# ---------------------------------
	print('\n\nJudicial concentre:')
	print(get_judicial_concentre(s))
	# ---------------------------------
	print('\n\nRJ/Falencia:')
	print(get_rj_falencia(s))
	# ---------------------------------
	print('\n\nAntecessores:')
	print(get_antecessores(s))	
	# ---------------------------------
	print('#','-'*60, '#')
	print('#',29*'-' + 'Fim' + 28*'-','#')
	print('#','-'*60, '#')

	