# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 09:54:24 2019
@author: fernando.barontini
"""
import json
import requests
import time
import re
import os
import numpy as np


# -----------------------------------------------------------------------
TOKEN = '' #variável para armazenar o token
TIME_INI = time.time()
USER = "LOGIN"
PASS = "PASSWORD"
URL_PF = ''
URL_PJ = ''

# -----------------------------------------------------------------------
def get_author_header():
	# funcao auxiliar para montar o dicionario de autenticação
	d = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
	d['Authorization'] = 'Bearer {}'.format(TOKEN)
	return d #{'Authorization': 'Bearer {}'.format(TOKEN)}

# -------------
def autenticar():
	
	URL_TOKEN = 'https://api.neoway.com.br/auth/token'
	header = {"application": USER,"application_secret": PASS}
	
	# chamo a URL para solicitar um token
	req = requests.post(URL_TOKEN,data=json.dumps(header))
	# verifico se a requisição foi realizada com sucesso,
	# senão exibo uma mensagem de erro na tela
	if req.status_code == 200:
		global TOKEN, TIME_INI
		TOKEN = json.loads(req.text)['token']
		TIME_INI = time.time()
		retorno = True
	else:
		print('Erro na conexão!\nVerifique se os dados estão corretos.')
		retorno = False
	
	return retorno

# -------------
def checar_token():
	URL_CHECAGEM = 'https://api.neoway.com.br/auth/token/check'
	header = get_author_header()
	
	req = requests.get(URL_CHECAGEM,headers=header)
	
	if req.status_code == 200:
		retorno = True
	else:
		retorno = False
	
	return retorno

# -------------
def refresh_token():
	URL_REFRESH = 'https://api.neoway.com.br/auth/token/refresh'
	header = {'Authorization': 'Bearer {}'.format(TOKEN)}
	
	req = requests.get(URL_REFRESH,headers=header)
	
	if req.status_code == 200:
		retorno = True
	else:
		retorno = False
		
	return retorno

# -------------
def validaCpf(cpf):
	#Fonte:
	#https://dicasdeprogramacao.com.br/algoritmo-para-validar-cpf/
	vetor = np.array([11,10,9,8,7,6,5,4,3,2])
	raiz = np.array([int(i) for i in cpf][:-2])
	
	# Primeiro digito
	d1 = np.sum((raiz * vetor[1:]))*10%11
	raiz = np.append(raiz, 0 if d1 == 10 else d1)
	# Segundo digito
	d2 = np.sum((raiz * vetor))*10%11
	raiz = np.append(raiz, 0 if d2 == 10 else d2)
	raiz = ''.join([str(i) for i in raiz])
	
	return True if raiz == cpf else False

# -------------
def validaCnpj(cnpj):
	#Fonte:
	#https://www.geradorcnpj.com/algoritmo_do_cnpj.htm
	vetor = np.array([6,5,4,3,2,9,8,7,6,5,4,3,2])
	raiz = np.array([int(i) for i in cnpj][:-2])
	
	# Primeiro digito
	d1 = 11 - np.sum((raiz * vetor[1:]))%11
	raiz = np.append(raiz, 0 if d1 >= 10 else d1)
	# Segundo digito
	d2 = 11 - np.sum(raiz * vetor)%11
	raiz = np.append(raiz, 0 if d2 >= 10 else d2)
	raiz = ''.join([str(i) for i in raiz])
	
	return True if raiz == cnpj else False

# -------------
def to_file(doc, data):
	
	filePathNameWExt = './Json/' + doc + '.txt'
	with open(filePathNameWExt, 'w') as fp:
		json.dump(data, fp=fp, indent=2,)

# -------------
def trata_cpf(s):
	s = re.sub('[^0-9]','',s)
	return s
# -------------
def existe_arquivo(arquivo):

	arquivo = './Json/{}.txt'.format(arquivo)
	existe = os.path.isfile(arquivo)
	if existe:
		retorno = True
	else:
		retorno = False
	
	return retorno

# -------------
# -------------
# -------------
def consultaPF(cpf):
	# chamada à API PF
	header = get_author_header()
	URL = 'https://api.neoway.com.br:/v1/data/pessoas/{}?fields=nome,cpf,situacaoCpf,cpfDataInscricao,idade,dataNascimento,falecido,falecidoConfirmado,anoFalecimento,sexo,nomeMae,cpfMae,cns,nis,pis,telefones.numero,endereco.logradouro,endereco.numero,endereco.complemento,endereco.bairro,endereco.municipio,endereco.uf,endereco.cep,email,enderecoOutros.logradouro,enderecoOutros.numero,enderecoOutros.complemento,enderecoOutros.bairro,enderecoOutros.municipio,enderecoOutros.uf,enderecoOutros.cep,infoEleitorais.titulo,infoEleitorais.situacao,infoEleitorais.zona,infoEleitorais.secao,infoEleitorais.localVotacao,infoEleitorais.enderecoVotacao,infoEleitorais.municipio,infoEleitorais.uf,participacaoSocietariaRF.cnpj,participacaoSocietariaRF.razaoSocial,participacaoSocietariaRF.descricaoCnae,participacaoSocietariaRF.ramoAtividade,participacaoSocietariaRF.dataAbertura,participacaoSocietariaRF.municipio,participacaoSocietariaRF.uf,participacaoSocietariaRF.situacao,participacaoSocietariaRF.dataEntrada,participacaoSocietariaRF.qualificacao,participacaoSocietariaRF.valorParticipacao,participacaoSocietariaRF.capitalSocialEmpresa,participacaoSocietariaRF.participacaoCapitalSocial,participacaoSocietariaRF.faixaFaturamentoPresumido,participacaoSocietariaRF.faixaFaturamentoPresumidoGrupo,participacaoSocietaria.cnpj,participacaoSocietaria.razaoSocial,participacaoSocietaria.descricaoCnae,participacaoSocietaria.ramoAtividade,participacaoSocietaria.dataAbertura,participacaoSocietaria.municipio,participacaoSocietaria.uf,participacaoSocietaria.situacao,participacaoSocietaria.dataEntrada,participacaoSocietaria.qualificacao,participacaoSocietaria.valorParticipacao,participacaoSocietaria.capitalSocialEmpresa,participacaoSocietaria.participacaoCapitalSocial,participacaoSocietaria.faixaFaturamentoPresumido,participacaoSocietaria.faixaFaturamentoPresumidoGrupo,participacaoSocietariaUnico.cnpj,participacaoSocietariaUnico.razaoSocial,participacaoSocietariaUnico.descricaoCnae,participacaoSocietariaUnico.ramoAtividade,participacaoSocietariaUnico.dataAbertura,participacaoSocietariaUnico.municipio,participacaoSocietariaUnico.uf,participacaoSocietariaUnico.situacao,participacaoSocietariaUnico.dataEntrada,participacaoSocietariaUnico.qualificacao,participacaoSocietariaUnico.valorParticipacao,participacaoSocietariaUnico.capitalSocialEmpresa,participacaoSocietariaUnico.participacaoCapitalSocial,participacaoSocietariaUnico.faixaFaturamentoPresumido,participacaoSocietariaUnico.faixaFaturamentoPresumidoGrupo,irpfRestituicao.exercicios.anoExercicio,irpfRestituicao.exercicios.nomeBanco,irpfRestituicao.exercicios.numAgencia,irpfRestituicao.exercicios.situacao,irpfRestituicao.exercicios.dataDisponibilidade,irpfRestituicao.exercicios.numLote,debitosPgfnDau.inscricao,debitosPgfnDau.natureza,debitosPgfnDau.valorTotal,debitosPgfnDau.dataProcessamento,mteCnd.processos.numero,mteCnd.processos.situacaoProcesso,mteCnd.processos.categoriaInfracao,mteCnd.processos.capitulacaoInfracao,mteCnd.tipoCertidao,mteCnd.situacaoDebito,mteCnd.codigo,mteCnd.dataEmissao,incomePrediction.incomeInterval,servidorPublico,transparencia.instituicao,transparencia.cargo,transparencia.remBruta,transparencia.remLiquida,transparencia.mesAnoPagamento,transparencia.vinculo,transparencia.fonte,atividadeFinanceira.numeroHabilitacao,atividadeFinanceira.dataConsulta,atividadeFinanceira.segmentos,atividadeFinanceira.situacaoHabilitacao,atividadeFinanceira.dataHabilitacao,enderecoEmpregoRaisNovo.cnpj,enderecoEmpregoRaisNovo.razaoSocial,enderecoEmpregoRaisNovo.descricaoCnae,enderecoEmpregoRaisNovo.ramoAtividade,enderecoEmpregoRaisNovo.quantidadeFuncionarios,enderecoEmpregoRaisNovo.faixaFaturamento,enderecoEmpregoRaisNovo.logradouro,enderecoEmpregoRaisNovo.numero,enderecoEmpregoRaisNovo.complemento,enderecoEmpregoRaisNovo.bairro,enderecoEmpregoRaisNovo.municipio,enderecoEmpregoRaisNovo.uf,enderecoEmpregoRaisNovo.cep,enderecoEmpregoRaisNovo.precisaoGeo,enderecoEmpregoRaisNovo.EnderecoResidencial,enderecoEmpregoRaisNovo.telefone,historicoFuncional.cnpj,historicoFuncional.razaoSocial,historicoFuncional.dataAdmissao,historicoFuncional.dataDesligamento,historicoFuncional.numeroMesesEmpresa,seguroDesemprego.pis,seguroDesemprego.situacao,seguroDesemprego.motivo,seguroDesemprego.dataPrimeiraParcela,cfm.numero,cfm.orgao,cfm.situacao,cfo.numeroInscricao,cfo.dataInscricaoCRO,cfo.dataInscricaoCFO,cfo.especialidade,cfo.funcao,cfo.situacao,cfo.orgao,cfc.registro,cfc.tipoRegistro,cfc.tipoConsulta,cfc.categoria,cfc.codigoCFC,cfc.situacao,cau.numeroRegistro,susepCorretor.registro,susepCorretor.situacao,susepCorretor.categoria,antt.numeroRntrc,antt.protocolo,antt.categoria,antt.situacao,antt.municipio,antt.uf,antt.dataEmissao,antt.dataValidade,mteTrabalhoEscravo.estabelecimentos.anoAcaoFiscal,mteTrabalhoEscravo.estabelecimentos.dataDecisaoProcedencia,mteTrabalhoEscravo.estabelecimentos.numeroTrabalhadoresEnvolvidos,mteTrabalhoEscravo.estabelecimentos.estabelecimento.complemento,mteTrabalhoEscravo.estabelecimentos.estabelecimento.logradouro,mteTrabalhoEscravo.estabelecimentos.estabelecimento.municipio,mteTrabalhoEscravo.estabelecimentos.estabelecimento.uf,imoveis.idReferencia,imoveis.areaConstruida,imoveis.valorAvaliacao,imoveis.areaTerreno,imoveis.dataConsulta,imoveis.endereco.logradouro,imoveis.endereco.numero,imoveis.endereco.complemento,imoveis.endereco.bairro,imoveis.endereco.municipio,imoveis.endereco.uf,imoveis.endereco.cep,cafir.imoveis.nirf,cafir.imoveis.nome,cafir.imoveis.area,cafir.imoveis.municipio,cafir.imoveis.uf,cafir.imoveis.condominioInfo,cafir.imoveis.tipo,cafir.numeroImoveisTitular,cafir.numeroImoveisCondomino,cafir.areaTotal,veiculosPesados.marca,veiculosPesados.debitos,veiculosPesados.tipo,veiculosPesados.renavam,veiculosPesados.anoFabricacao,veiculosPesados.placa,veiculosPesados.uf,veiculosPesados.municipio,qtdVeiculosPesados,aeronaves.matricula,aeronaves.proprietario,aeronaves.operador,aeronaves.modelo,aeronaves.fabricante,aeronaves.ano,bolsaFamilia.competencia,bolsaFamilia.uf,bolsaFamilia.municipio,bolsaFamilia.valorParcela,ceis.codigoProcesso,ceis.tipoSancao,ceis.dataInicioSancao,ceis.dataFimSancao,ceis.fundamentacaoLegal,ceis.orgaoSancionador,ceis.origemInformacoes,ceis.ufOrgaoSancionador,ceis.dataOrigemInformacoes,cnep.processos.numeroProcesso,cnep.processos.tipoSancao,cnep.processos.valorMulta,cnep.processos.dataInicioSancao,cnep.processos.dataFinalSancao,cnep.processos.orgaoSancionador,cnep.processos.ufOrgaoSancionador,processoJudicialTotalizadores.quantidades.tipo,processoJudicialTotalizadores.quantidades.qtdTotal,processoJudicialTotalizadores.quantidades.qtdAtivos,processoJudicialTotalizadores.quantidades.qtdParteAtiva,processoJudicialTotalizadores.quantidades.qtdPartePassiva,processoJudicialTotalizadores.quantidades.qtdOutrasPartes,processoJudicialTotalizadores.valorTotal,processoJudicialTotalizadores.valorTotalAtiva,processoJudicialTotalizadores.valorTotalPassiva,processoJudicialTotalizadores.valorTotalOutrasPartes,bancoCentral.acordaos.numeroRecurso,bancoCentral.acordaos.numeroProcesso,bancoCentral.acordaos.numeroAcordaoCRSFN,bancoCentral.acordaos.recurso,bancoCentral.acordaos.parte,cnjCnia.processos.numeroProcesso,cnjCnia.processos.dataCadastramento,cnjCnia.processos.esfera,cnjCnia.processos.descricaoOrgao,cnjCnia.processos.cargoFuncao.uf,cnjCnia.processos.assuntosRelacionados,cnjCnia.processos.ressarcimentoIntegralDano.valor,ibamaEmbargos.numeroTad,ibamaEmbargos.numeroInfracao,ibamaEmbargos.descricaoInfracao,ibamaEmbargos.area,ibamaEmbargos.logradouro,ibamaEmbargos.municipio,ibamaEmbargos.uf,ibamaEmbargos.dataJulgamento,ibamaEmbargos.dataInsercao,autoInfracao.infracoes.infracao,autoInfracao.infracoes.dataInfracao,autoInfracao.infracoes.uf,autoInfracao.infracoes.municipio,autoInfracao.infracoes.nai,autoInfracao.infracoes.valorMulta,autoInfracao.infracoes.numeroProcesso,autoInfracao.infracoes.statusDebito,autoInfracao.infracoes.sancoesAplicadas,ibamaCtf.numeroRegistro,ibamaCtf.cadastro,ibamaCtf.ocupacao,ibamaCtf.areaAtividade,ibamaCtf.dataEmissaoCr,ibamaCtf.crValidade,ibamaCtf.dataConsulta,ibamaCnd.situacao,ibamaCnd.certidao,ibamaCnd.emissao,ibamaCnd.validade,doacaoEleitoral.doacoes.descricaoEleicao,doacaoEleitoral.doacoes.nomeDoadorOriginario,doacaoEleitoral.doacoes.setorEconomicoDoador,doacaoEleitoral.doacoes.valorDoado,pep.descricaoNivel,pep.cpfPrimario,pep.nomePrimario,pep.descricaoCargoRelacao,pep.descricaoOrgao,pep.dataInclusao,pep.dataFimCarencia,estabilidadeEmprego.faixa,profissaoNeoway,planosSaude.codigoOperadora,planosSaude.nomeOperadora,planosSaude.codigo,planosSaude.descricao,planosSaude.caracteristica,planosSaude.cco,planosSaude.identificacaoBeneficiario,planosSaude.dataProcessamento'.format(cpf)
	req = requests.get(URL,headers=header)
	
	if req.status_code == 200:
		to_file(cpf, json.loads(req.text))
		retorno = True
	else:
		retorno = False
	
	return retorno


def consultaPJ(cnpj):
	# chamada à API PJ
	header = get_author_header()
	URL = 'https://api.neoway.com.br:/v1/data/empresas/{}?fields=cnpj,razaoSocial,fantasia,natureza.id,natureza.descricao,natureza.classificacao,porte,situacao.descricao,situacao.motivo,situacao.data,situacao.especial.descricao,situacao.especial.data,info.valorDividaPgfnDau,matriz.empresaMatriz,dataAbertura,info.idadeEmpresa,cnaePrincipal.codigo,cnaePrincipal.descricao,cnaePrincipal.setor,cnaePrincipal.ramoAtividade,matriz.quantidadeFilial,nivelAtividade,info.qsaDivergente,expectativaVidaEmpresas.idade,expectativaVidaEmpresas.faixaExpectativa,expectativaVidaEmpresas.idadeAcimaExpectativa,telefones.numero,telefones.fonteInformacao,endereco.logradouro,endereco.numero,endereco.complemento,endereco.bairro,endereco.bairroOriginal,endereco.municipio,endereco.municipioOriginal,endereco.mesoRegiao,endereco.uf,endereco.cep,endereco.precisao,endereco.enderecoResidencial,info.numeroTelefoneRF[0],info.numeroTelefoneRF[1],info.emailRF,info.possuiEmailContador,potencialConsumo.valorCapitalSocial,totalFuncionarios.quantidade,totalFuncionarios.quantidadeGrupo,faturamentoPresumido.faixaIndividual,faturamentoPresumido.faixaGrupo,empresaBalancoFinanceiro.balancosPatrimoniais.ano,empresaBalancoFinanceiro.balancosPatrimoniais.ativoTotal,empresaBalancoFinanceiro.balancosPatrimoniais.ativoCirculante,empresaBalancoFinanceiro.balancosPatrimoniais.ativoNaoCirculante,empresaBalancoFinanceiro.balancosPatrimoniais.passivoTotal,empresaBalancoFinanceiro.balancosPatrimoniais.passivoCirculante,empresaBalancoFinanceiro.balancosPatrimoniais.passivoNaoCirculante,empresaBalancoFinanceiro.balancosPatrimoniais.patrimonioLiquido,empresaBalancoFinanceiro.diarioOficial,empresaBalancoFinanceiro.demonstracoesResultados.receitaLiquida,empresaBalancoFinanceiro.demonstracoesResultados.lucroLiquido,empresaBalancoFinanceiro.demonstracoesResultados.depreciacao,empresaBalancoFinanceiro.demonstracoesResultados.EBITDAAproximado,empresaBalancoFinanceiro.diarioOficial,empresaBalancoFinanceiro.indicadoresFinanceiros.ano,empresaBalancoFinanceiro.indicadoresFinanceiros.crescimentoDaReceita,empresaBalancoFinanceiro.indicadoresFinanceiros.margemEBIT,empresaBalancoFinanceiro.indicadoresFinanceiros.custoSobreReceita,empresaBalancoFinanceiro.indicadoresFinanceiros.margemEBITDA,empresaBalancoFinanceiro.indicadoresFinanceiros.margemLucro,empresaBalancoFinanceiro.indicadoresFinanceiros.ROA,empresaBalancoFinanceiro.indicadoresFinanceiros.ROE,empresaBalancoFinanceiro.indicadoresFinanceiros.liquidezCorrente,empresaBalancoFinanceiro.indicadoresFinanceiros.liquidezGeral,empresaBalancoFinanceiro.indicadoresFinanceiros.passivoPorEBITDA,empresaBalancoFinanceiro.demonstracoesResultados.ano,empresaBalancoFinanceiro.demonstracoesResultados.receitaLiquida,empresaBalancoFinanceiro.indicadoresFinanceiros.ano,empresaBalancoFinanceiro.indicadoresFinanceiros.crescimentoDaReceita,capitalAberto.cdPregao,capitalAberto.cdNegociacao,capitalAberto.atividadePrincipal,capitalAberto.nomeDiretorInvestimento,capitalAberto.logradouroDiretorInvestimento,capitalAberto.numeroLogradouroDiretorInvestimento,capitalAberto.complementoLogradouroDiretorInvestimento,capitalAberto.municipioDiretorInvestimento,capitalAberto.ufDiretorInvestimento,capitalAberto.cepDiretorInvestimento,capitalAberto.site,capitalAberto.classificacaoSetorial,capitalAberto.telefoneDiretorInvestimento,capitalAberto.emailDiretorInvestimento,capitalAberto.multa.dataMulta,capitalAberto.multa.motivo,capitalAberto.balancoPatrimonial.ano,capitalAberto.balancoPatrimonial.ativoImobInvestIntangivel,capitalAberto.balancoPatrimonial.ativoTotal,capitalAberto.balancoPatrimonial.patrimonioLiquido,capitalAberto.balancoPatrimonial.patrimonioLiquidoControladora,capitalAberto.demonstracaoResultado.ano,capitalAberto.demonstracaoResultado.receitaVenda,capitalAberto.demonstracaoResultado.resultadoBruto,capitalAberto.demonstracaoResultado.resultadoEquivPatrimonial,capitalAberto.demonstracaoResultado.resultadoFinanceiro,capitalAberto.demonstracaoResultado.resultadoLiquiOperContinuada,capitalAberto.demonstracaoResultado.lucroPrejuPeriodo,capitalAberto.demonstracaoResultado.lucroPrejuPeriodoControladora,crescimentoPorAnoRais.ano,crescimentoPorAnoRais.percentual,cvm.faturamentoBruto,cvm.faturamentoLiquido,cvm.lucroBruto,cvm.lucroLiquido,cvm.ativoTotal,cvm.patrimonioLiquido,cvm.anoBalanco,imoveis.imovelId,imoveis.ufRegistro,imoveis.areaTerreno,imoveis.areaConstruida,imoveis.anoConstrucao,imoveis.valorAvaliacao,imoveis.logradouro,imoveis.numeroLogradouro,imoveis.complemento,imoveis.bairro,imoveis.municipio,imoveis.uf,imoveis.cep,cafir.imoveis.nirf,cafir.imoveis.nome,cafir.imoveis.area,cafir.imoveis.municipio,cafir.imoveis.uf,cafir.imoveis.condominioInfo,cafir.imoveis.tipo,cafir.numeroImoveisTitular,cafir.numeroImoveisCondomino,cafir.areaTotal,importacao.valor,importacao.ano,tributaryHealth.cnds.nome,tributaryHealth.cnds.descricaoSituacao,tributaryHealth.cnds.dataEmissao,tributaryHealth.cnds.numeroCertificacao,tributaryHealth.cnds.dataValidade,tributaryHealth.saudeTributaria,debitosPgfnDau.inscricao,debitosPgfnDau.natureza,debitosPgfnDau.valorTotal,debitosPgfnDau.dataProcessamento,sintegra.inscricaoEstadual,sintegra.uf,sintegra.situacaoCadastral,sintegra.dataSituacaoCadastral,sintegra.telefone,sintegra.email,sintegra.regimeApuracao,cfc.registro,cfc.codigoCFC,cfc.tipoRegistro,cfc.tipoConsulta,cfc.situacao,simplesNacional.optanteSimples,simplesNacional.dataOptanteSimples,simplesNacional.optanteSimei,simplesNacional.dataOptanteSimei,simplesNacional.simplesIrregular,ceis.numeroProcesso,ceis.tipoSancao,ceis.dataInicioSancao,ceis.dataFimSancao,ceis.fundamentacaoLegal,ceis.orgaoSancionador,ceis.origemInformacoes,ceis.ufOrgaoSancionador,ceis.dataOrigemInformacoes,processoJudicialTotalizadores.quantidades.tipo,processoJudicialTotalizadores.quantidades.qtdTotal,processoJudicialTotalizadores.quantidades.qtdAtivos,processoJudicialTotalizadores.quantidades.qtdParteAtiva,processoJudicialTotalizadores.quantidades.qtdPartePassiva,processoJudicialTotalizadores.quantidades.qtdOutrasPartes,processoJudicialTotalizadores.valorTotal,processoJudicialTotalizadores.valorTotalAtiva,processoJudicialTotalizadores.valorTotalPassiva,processoJudicialTotalizadores.valorTotalOutrasPartes,cnaes.codigo,cnaes.descricao,cnaePrincipal.codigo,cnaePrincipal.descricao,info.nomeFranquia,socios.participacaoSocietaria,socios.documento,socios.nome,socios.qualificacao,socios.documento,socios.paisOrigem,socios.falecido,socios.nivelPep,sociosJunta.participacaoSocietaria,sociosJunta.documento,sociosJunta.nome,sociosJunta.qualificacao,sociosJunta.documento,sociosJunta.falecido,sociosJunta.nivelPep,beneficiarios.documento,beneficiarios.nome,beneficiarios.participacao,beneficiarios.falecido,beneficiarios.grau,beneficiariosJunta.documento,beneficiariosJunta.nome,beneficiariosJunta.participacao,beneficiariosJunta.falecido,beneficiariosJunta.grau,capitalAberto.posicaoAcionaria.nome,capitalAberto.posicaoAcionaria.documento,capitalAberto.posicaoAcionaria.valorOrdemNominal,capitalAberto.posicaoAcionaria.valorPrefNominal,capitalAberto.posicaoAcionaria.valorTotal,empresasColigadas.cnpj,empresasColigadas.razaoSocial,empresasColigadas.dataAbertura,empresasColigadas.municipio,empresasColigadas.uf,empresasColigadas.cnae,crescimentoPorAnoRais.ano,crescimentoPorAnoRais.qtdFuncionarios,funcionarios.cpf,funcionarios.nome,funcionarios.dataNascimento,funcionarios.dataAdmissao,novoPat.numeroInscricao,novoPat.nomeResponsavel,novoPat.emailResponsavel,novoPat.cpfResponsavel,novoPat.situacao,novoPat.modalidades.descricao,novoPat.modalidades.numeroTrabBeneficiados,novoPat.modalidades.razaoSocialForcenedor,novoPat.modalidades.cnpjForcenedor,foodEstabCategories.establishmentTypes,foodEstabCategories.foodCategories,calc.totalExFuncionarios.porAno.ano,calc.totalExFuncionarios.porAno.quantidade,exfuncionarios.cpf,exfuncionarios.nome,exfuncionarios.dataNascimento,exfuncionarios.dataAdmissao,exfuncionarios.anoMesDesligamento,antt.cnpj,antt.regime,antt.modalidade,antt.numeroCertificado,antt.dataValidade,antt.dataAtualizacao,veiculosPesados.placa,veiculosPesados.uf,veiculosPesados.marcaModelo,veiculosPesados.tipo,veiculosPesados.renavam,veiculosPesados.combustivel,veiculosPesados.anoFabricacao,veiculosPesados.constaAntt,calc.totalVeiculosPesados.tipo.label,calc.totalVeiculosPesados.tipo.value,calc.totalVeiculosPesados.combustivel.label,calc.totalVeiculosPesados.combustivel.value,detran.totalVeiculosPesados,detran.totalVeiculosPesadosGrupo,totalVeiculos.ateUmAno,totalVeiculos.entreDoisCincoAnos,totalVeiculos.entreCincoDezAnos,totalVeiculos.acimaDezAnos,totalVeiculos.grupoAteUmAno,totalVeiculos.grupoEntreDoisCincoAnos,totalVeiculos.grupoEntreCincoDezAnos,totalVeiculos.grupoAcimaDezAnos,postosCombustiveis.listaEquipamentos.combustivel,postosCombustiveis.listaEquipamentos.tancagem,postosCombustiveis.listaEquipamentos.bicos,postosCombustiveis.autorizacao,postosCombustiveis.bandeiraAtual,postosCombustiveis.tipoPosto,postosCombustiveis.totalTancagem,postosCombustiveis.totalBicos,postosCombustiveis.bandeiras.bandeira,postosCombustiveis.bandeiras.inicioBandeira,pontosAbastecimento.numeroConsulta,pontosAbastecimento.municipio,pontosAbastecimento.uf,pontosAbastecimento.numeroTanques,pontosAbastecimento.totalTancagem,pontosAbastecimentoTanque.numeroConsulta,pontosAbastecimentoTanque.numeroDoTanque,pontosAbastecimentoTanque.combustivel,pontosAbastecimentoTanque.capacidade,aeronaves.matricula,aeronaves.modelo,aeronaves.fabricante,aeronaves.proprietario,aeronaves.operador,aeronaves.ano,cnes.identificador,cnes.tipoUnidade,cnes.dataCadastro,cnes.dataUltimaAtualizacao,cnes.totalProfissionais,cnes.totalLeitos,faculdades.codigo,faculdades.nome,faculdades.categoria,faculdades.situacao,escolas.nome,escolas.vinculo,escolas.funcionamento,escolas.categoria,escolas.totalMatricula,calc.totalObras.iniciadas.ano,calc.totalObras.iniciadas.quantidade,calc.totalObras.concluidas.ano,calc.totalObras.concluidas.quantidade,arts.vinculo,arts.cnpj,arts.numeroArt,arts.finalidade,arts.observacao,arts.dataRegistro,arts.dataInicio,arts.dataPrevisaoTermino,arts.valorTotalServico,arts.bairro,arts.municipio,arts.uf,arts.cep,arts.quantidadeObrasServicos,inpiMarcas.marca,inpiMarcas.dataDeposito,inpiMarcas.numeroProcesso,inpiMarcas.situacao,inpiMarcas.classe,inpiProgramas.tituloPrograma,inpiProgramas.dataDeposito,inpiProgramas.numeroProcesso,dominios.nome,dominios.dataCriacao,dominios.responsavel,dominios.email,empresasSimilares.cnpj,empresasSimilares.razaoSocial,empresasSimilares.naturezaJuridica,empresasSimilares.uf,empresasSimilares.cnae,empresasSimilares.quantidadeFunc,filiais.cnpj,filiais.razaoSocial,filiais.situacao,filiais.dataAbertura,filiais.municipio,filiais.uf,matriz.cnpj,matriz.razaoSocial,matriz.situacao,matriz.dataAbertura,matriz.municipio,matriz.uf,ibge.faixaRendaPopulacao,potencialConsumoRamo.potencialConsumoRamo.residencial,potencialConsumoRamo.potencialConsumoRamo.comercial,qsaUnificado.nivelPep,qsaUnificado.categoriaProcessoCriminal,mteCnd.processos.numero,mteCnd.processos.situacaoProcesso,mteCnd.processos.categoriaInfracao,mteCnd.processos.capitulacaoInfracao,mteCnd.tipoCertidao,mteCnd.situacaoDebito,mteCnd.codigo,mteCnd.dataEmissao,atividadeFinanceira.numeroHabilitacao,atividadeFinanceira.dataConsulta,atividadeFinanceira.segmentos,atividadeFinanceira.situacaoHabilitacao,atividadeFinanceira.dataHabilitacao,mteTrabalhoEscravo.estabelecimentos.anoAcaoFiscal,mteTrabalhoEscravo.estabelecimentos.dataDecisaoProcedencia,mteTrabalhoEscravo.estabelecimentos.numeroTrabalhadoresEnvolvidos,mteTrabalhoEscravo.estabelecimentos.estabelecimento.complemento,mteTrabalhoEscravo.estabelecimentos.estabelecimento.logradouro,mteTrabalhoEscravo.estabelecimentos.estabelecimento.municipio,mteTrabalhoEscravo.estabelecimentos.estabelecimento.uf,cnep.processos.numeroProcesso,cnep.processos.tipoSancao,cnep.processos.valorMulta,cnep.processos.dataInicioSancao,cnep.processos.dataFinalSancao,cnep.processos.orgaoSancionador,cnep.processos.ufOrgaoSancionador,empresaCepim.convenios.convenio,empresaCepim.convenios.concedente,empresaCepim.convenios.impedimento,empresaCepim.convenios.valorLiberado,empresaCepim.convenios.fimVigencia,bancoCentral.acordaos.numeroRecurso,bancoCentral.acordaos.numeroProcesso,bancoCentral.acordaos.numeroAcordaoCRSFN,bancoCentral.acordaos.recurso,bancoCentral.acordaos.parte,cnjCnia.processos.numeroProcesso,cnjCnia.processos.dataCadastramento,cnjCnia.processos.esfera,cnjCnia.processos.descricaoOrgao,cnjCnia.processos.cargoFuncao.uf,cnjCnia.processos.assuntosRelacionados,cnjCnia.processos.ressarcimentoIntegralDano.valor,ibamaEmbargos.numeroTad,ibamaEmbargos.numeroInfracao,ibamaEmbargos.descricaoInfracao,ibamaEmbargos.area,ibamaEmbargos.logradouro,ibamaEmbargos.municipioRaw,ibamaEmbargos.uf,ibamaEmbargos.dataJulgamento,ibamaEmbargos.dataInsercao,autoInfracao.infracoes.infracao,autoInfracao.infracoes.dataInfracao,autoInfracao.infracoes.uf,autoInfracao.infracoes.municipio,autoInfracao.infracoes.nai,autoInfracao.infracoes.valorMulta,autoInfracao.infracoes.numeroProcesso,autoInfracao.infracoes.statusDebito,autoInfracao.infracoes.sancoesAplicadas,ibamaCtf.ctfapp.categoria,ibamaCtf.ctfapp.detalhes,ibamaCtf.numeroRegistro,ibamaCtf.cadastro,ibamaCtf.dataEmissaoCr,ibamaCtf.crValidade,ibamaCtf.dataConsulta,ibamaCnd.situacao,ibamaCnd.certidao,ibamaCnd.emissao,ibamaCnd.validade,doacaoEleitoral.doacoes.descricaoEleicao,doacaoEleitoral.doacoes.nomeCandidato,doacaoEleitoral.doacoes.cargo,doacaoEleitoral.doacoes.siglaPartido,doacaoEleitoral.doacoes.uf,doacaoEleitoral.doacoes.valorDoado,qsaUnificado.nivelPep,qsaUnificado.categoriaProcessoCriminal,mteCnd.processos.numero,mteCnd.processos.situacaoProcesso,mteCnd.processos.categoriaInfracao,mteCnd.processos.capitulacaoInfracao,mteCnd.tipoCertidao,mteCnd.situacaoDebito,mteCnd.codigo,mteCnd.dataEmissao,atividadeFinanceira.numeroHabilitacao,atividadeFinanceira.dataConsulta,atividadeFinanceira.segmentos,atividadeFinanceira.situacaoHabilitacao,atividadeFinanceira.dataHabilitacao,mteTrabalhoEscravo.estabelecimentos.anoAcaoFiscal,mteTrabalhoEscravo.estabelecimentos.dataDecisaoProcedencia,mteTrabalhoEscravo.estabelecimentos.numeroTrabalhadoresEnvolvidos,mteTrabalhoEscravo.estabelecimentos.estabelecimento.complemento,mteTrabalhoEscravo.estabelecimentos.estabelecimento.logradouro,mteTrabalhoEscravo.estabelecimentos.estabelecimento.municipio,mteTrabalhoEscravo.estabelecimentos.estabelecimento.uf,cnep.processos.numeroProcesso,cnep.processos.tipoSancao,cnep.processos.valorMulta,cnep.processos.dataInicioSancao,cnep.processos.dataFinalSancao,cnep.processos.orgaoSancionador,cnep.processos.ufOrgaoSancionador,empresaCepim.convenios.convenio,empresaCepim.convenios.concedente,empresaCepim.convenios.impedimento,empresaCepim.convenios.valorLiberado,empresaCepim.convenios.fimVigencia,bancoCentral.acordaos.numeroRecurso,bancoCentral.acordaos.numeroProcesso,bancoCentral.acordaos.numeroAcordaoCRSFN,bancoCentral.acordaos.recurso,bancoCentral.acordaos.parte,cnjCnia.processos.numeroProcesso,cnjCnia.processos.dataCadastramento,cnjCnia.processos.esfera,cnjCnia.processos.descricaoOrgao,cnjCnia.processos.cargoFuncao.uf,cnjCnia.processos.assuntosRelacionados,cnjCnia.processos.ressarcimentoIntegralDano.valor,ibamaEmbargos.numeroTad,ibamaEmbargos.numeroInfracao,ibamaEmbargos.descricaoInfracao,ibamaEmbargos.area,ibamaEmbargos.logradouro,ibamaEmbargos.municipioRaw,ibamaEmbargos.uf,ibamaEmbargos.dataJulgamento,ibamaEmbargos.dataInsercao,autoInfracao.infracoes.infracao,autoInfracao.infracoes.dataInfracao,autoInfracao.infracoes.uf,autoInfracao.infracoes.municipio,autoInfracao.infracoes.nai,autoInfracao.infracoes.valorMulta,autoInfracao.infracoes.numeroProcesso,autoInfracao.infracoes.statusDebito,autoInfracao.infracoes.sancoesAplicadas,ibamaCtf.ctfapp.categoria,ibamaCtf.ctfapp.detalhes,ibamaCtf.numeroRegistro,ibamaCtf.cadastro,ibamaCtf.dataEmissaoCr,ibamaCtf.crValidade,ibamaCtf.dataConsulta,ibamaCnd.situacao,ibamaCnd.certidao,ibamaCnd.emissao,ibamaCnd.validade,doacaoEleitoral.doacoes.descricaoEleicao,doacaoEleitoral.doacoes.nomeCandidato,doacaoEleitoral.doacoes.cargo,doacaoEleitoral.doacoes.siglaPartido,doacaoEleitoral.doacoes.uf,doacaoEleitoral.doacoes.valorDoado'.format(cnpj)
	req = requests.get(URL,headers=header)
	
	if req.status_code == 200:
		to_file(cnpj, json.loads(req.text))
		retorno = True
	else:
		retorno = False
	
	return retorno
	

# -----------------------------------------------------------------------

def main(skip = False):
	
	NOW = time.time()
	# valido se o token ainda está valido.
	if TOKEN == '':
		autenticar()
	else:
		#pass
		refresh_token()
	
	documento = input('Digite o documento a pesquisar: ')
	documento = trata_cpf(documento)
	
	try:
		
		if existe_arquivo(documento):
			print('Já existe uma consulta para o documento.')
			print('Gostaria de sobrescrevê-la?')
			check = input('[s/n]: ')
			
			if check.lower() == 's':
				if len(documento) == 11 and validaCpf(documento):
					consultaPF(documento)
				elif len(documento) == 14 and validaCnpj(documento):
					consultaPJ(documento)
				else:
					print('O documento inserido é inválido. Favor digitar um documento válido!')
					main(True)
			else:
				pass
		else:
			if len(documento) == 11 and validaCpf(documento):
				consultaPF(documento)
			elif len(documento) == 14 and validaCnpj(documento):
				consultaPJ(documento)
			else:
				print('O documento inserido é inválido. Favor digitar um documento válido!')
				main(True)		
	
	except:
		print('Erro na pesquisa!')
	
	if not skip:
		print('Gostaria de consultar mais algum documento?')
		inp = input('[s/n]: ')
		if inp.lower() == 's':
			main()
		else:
			print('Saindo do programa.')
			pass
	else:
		pass
# -----------------------------------------------------------------------

def massivo():
	
	#abertura do arquivo de CPF e CNPJ
	CONSULTAS = []
	with open('CONSULTAR.txt', 'r') as f:
	    linhas = f.readlines()
	    
	for linha in linhas:
		CONSULTAS.append(trata_cpf(linha))
	
	
	for documento in CONSULTAS:
	
		print('Iniciando pesquisa no documento {}'.format(documento))
		
		try:
			# valido se o token ainda está valido.
			if TOKEN == '':
				autenticar()
			else:
				#pass
				refresh_token()
			
			documento = trata_cpf(documento)
			if not existe_arquivo(documento):
				if len(documento) == 11 and validaCpf(documento):
					consultaPF(documento)
				elif len(documento) == 14 and validaCnpj(documento):
					consultaPJ(documento)
				else:
					print('O documento {} é inválido!'.format(documento))
			else:
				print('Documento já pesquisado: {}'.format(documento))
				pass
			
			time.sleep(0.3)
			
			
		except:
			print('Erro na consulta!')
	
# -------------


if __name__ == '__main__':
	
	main()
	#massivo()
	