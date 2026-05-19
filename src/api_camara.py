import requests
import ssl
import pandas as pd
from requests.adapters import HTTPAdapter

class TLSv1_2Adapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        # Cria um contexto SSL que só permite TLSv1.2
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        # Usa o contexto SSL customizado no PoolManager
        self.poolmanager = requests.packages.urllib3.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context
        )


class APICamara:
    """
    Docstring para APICamara
    https://dadosabertos.camara.leg.br/swagger/api.html
    /comissao/
    Informações de Comissões, Órgãos, Conselhos e demais Colegiados do Senado Federal e Congresso Nacional
    """
    def __init__(self):
        self.url_base = 'https://dadosabertos.camara.leg.br/api/v2'
        self.session = requests.Session()
        self.session.mount('https://', TLSv1_2Adapter()) 

        self.session.headers.update({'Accept': 'application/json',
        'User-Agent': 'Python-API-Senado/1.0'})

    
    def _comissao(self, cod_colegiado):
        """
        Detalhes de um Colegiado do Congresso Nacional
        Em desuso pois usa api do senado
        Url: https://legis.senado.leg.br/dadosabertos/
        """
        endpoint = f"comissao/{cod_colegiado}"
        url = f"{self.url_base}{endpoint}"
        try:
            response = self.session.get(url, timeout=25)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Tempo limite excedido para {url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: {e}")

    def busca_deputados_atual(self, **kwargs):
        """
        Busca lista de todos os deputados em exercício        
        Se não for passado um parâmetro de tempo, como idLegislatura ou dataInicio, a lista enumerará somente os deputados em exercício no momento da requisição.
        """
        endpoint = f"/deputados"
        url = f"{self.url_base}{endpoint}"
        params = kwargs

        try:
            if params is not None:
                response = self.session.get(url, params=params, timeout=25)

            else:
                response = self.session.get(url, timeout=25)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Tempo limite exedido para {url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: \n {e}")
            
    def busca_deputado(self, id: str=''):
        """
        Informações detalhadas sobre um deputado específico pelo id(integer)
        """
        endpoint = f"/deputados/{id}"
        url = f"{self.url_base}{endpoint}"
        try:
            response = self.session.get(url, timeout=25)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Tempo limite exedido para {url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: \n {e}")

    def busca_despesas(self, id, **kwargs):
        """
        Dá acesso aos registros de pagamentos e reembolsos feitos pela Câmara em prol do deputado identificado por {id}, a título da Cota para Exercício da Atividade Parlamentar, a chamada "cota parlamentar".

        A lista pode ser filtrada por mês, ano, legislatura, CNPJ ou CPF de um fornecedor.

        Se não forem passados os parâmetros de tempo, o serviço retorna os dados dos seis meses anteriores à requisição.
        """
        endpoint = f"/deputados/{id}/despesas"
        url = f"{self.url_base}{endpoint}"
        params = kwargs
        
        try:
            response = self.session.get(url, params=params, timeout=25)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Tempo limite exedido para {url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: \n {e}")

    def integrantes_partidos(self, siglaPartido: str=''):
        """
        Retorna uma lista de dados básicos sobre os partidos políticos que têm ou já tiveram deputados na Câmara. Se não forem passados parâmetros, o serviço retorna os partidos que têm deputados em exercício no momento da requisição.

        É possível obter uma lista de partidos representados na Câmara em um certo intervalo de datas ou de legislaturas. Se um intervalo e uma ou mais legislatura(s) não coincidentes forem passados, todos os intervalos de tempo serão somados.

        Também se pode fazer busca por uma ou mais sigla(s), mas atenção: em diferentes legislaturas, pode haver mais de um partido usando a mesma sigla.
        """
        endpoint = f"/partidos/{id}/membros"
        url = f"{self.url_base}{endpoint}"
        try:
            response = self.session.get(url, timeout=25)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Tempo limite exedido para {url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: \n {e}")

    def busca_partidos(self, id):
        """
        Retorna uma lista de deputados que estão ou estiveram em exercício pelo partido {id}.

        Opcionalmente, pode-se usar os parâmetros dataInicio, dataFim ou idLegislatura para se obter uma lista de deputados filiados ao partido num certo intervalo de tempo. Isso é equivalente ao serviço /deputados com filtro por partido, mas é melhor para obter informações sobre membros de partidos já extintos.
        """
        endpoint = f"/partidos/{id}/membros"
        url = f"{self.url_base}{endpoint}"
        try:
            response = self.session.get(url, timeout=25)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Tempo limite exedido para {url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: \n {e}")

    def situacoesDeputados(self, id):
        pass
