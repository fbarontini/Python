select
	   aj.IdJuizo
     , aj.IdCliente
     , aj.IdCaso
     , aj.IdOperacao
     , aj.IdFase
	 , aj.DsFase
     , aj.IdSubFase
     , aj.DsSubFase
     , aj.DsStatusJuizo
     , aj.DsCarteiraJuizo
     , aj.DsJurisdicao
     , aj.DsJurisdicaoDetalhe
     , aj.IdTipoJuizo
     , aj.DsTipoJuizo
     , aj.IdEstadoJuizo
     , aj.DsEstadoJuizo as dsEtapa
     , aj.DsSubEstadoJuizo
     , aj.DsCitacao
     , aj.DsMoeda
     , aj.DsStatusUltimoAcordo
     , aj.DsSegmentoAjuizado
     , aj.DsSituacaoProcessual  
     , aj.DsDemandante    
     , aj.DsJulgado  
     , aj.DsForum    
     , aj.DsSecretaria    
     , aj.DsObjetoProcesso 
     , aj.DsDemandado 
     , aj.DsUsuarioUltimaModificacao 
     , aj.DsEmbargoOutros       
     , aj.CdDemandado 
     , aj.DsCoDemandado   
     , aj.CdCoDemandado   
     , aj.NrExpediente
     , aj.NrCNJ
     , aj.NrCaso
     , aj.VlDemanda
     , aj.VlQuirografario
     , aj.VlComPrivilegio
     , aj.VlSentenca
     , aj.VlHonorario
     , aj.VlGasto
     , aj.VlUltimoRecebimento
     , aj.FgEmbargoImovel
     , aj.FgEmbargoOutros
     , aj.FgRegistroAtivo
     , aj.DtUltimoRecebimento
     , aj.DtReferencia
     , case
			when o.IdCarteira = 73 then 'Iresolve'
			else 'Mercado'
	   end as Categoria
     , o.dsAgencia
     , o.idAgencia
     , o.dsLote
     , o.vlSop
	 , aj.DtUltimaModificacao
from
     db_dm1..viwAjuizado as aj
     inner join db_dm1..viwOperacao as o on aj.idOperacao = o.idOperacao
     --inner join escobsEmailsJuizo as ej on o.idAgencia = ej.idAgenciaViwOperacao
where
	aj.FgRegistroAtivo = 1 --aj.dsStatusJuizo = 'Ativo'
	and o.IdAgencia in (
						0646,0653,0655,0676,0735,0830,1007,1036,
						1108,1119,1137,1156,1199,1201,1434,1477,
						1483,1493,1505,1507,1533,1633,1646,1665,
						1714,1736,1897,1899,1904,1929,2404,2413,
						2415,2416,2417,2419,2420,2424,2425,2427,
						2428,2457,2506,2508,2616,2619,2622,2873
					)
	and o.idPaisCarteira = 9
    and
		(
			o.DsSegmentoGestao IN ('PCJ','PCJ IMOB','PCJ_Aco','PNJ','PNJ_Aco')
		or
			o.DsSegmentoGestaoAgrupado = 'VEICULOS'
		)