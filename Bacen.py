from zeep import Client
import json

class Bacen:
    '''
    Consulta as séries do BACEN e traz a última posição também.
    É possivel rodar diariamente para trazer todos os índices
    '''
    _WSDLFILE = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
    _Cliente = None
    
    def __init__(self):
        try:
            self._Cliente = Client(self._WSDLFILE)
        except OSError as err:
            print('Erro na conexão!')
        return

    #Consulto o último valor da serie informada
    def consultaUltimoValor(self, idValor):
        resposta = self._Cliente.service.getUltimoValorVO(idValor)
        print(resposta)
        return
    #Consulto o valor da serie informada dada a data informada.
    #É possivel colocar um loop aqui para alimentar uma base de dados.
    def consultaValor(self, idValor, dtConsulta):
        resposta = self._Cliente.service.getValor(idValor,dtConsulta)
        print(resposta)
        return