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
        #self.url_base = 'https://legis.senado.leg.br/dadosabertos/'
        self.url_base = 'https://dadosabertos.camara.leg.br/api/v2'
        self.session = requests.Session()
        self.session.mount('https://', TLSv1_2Adapter()) 

        self.session.headers.update({'Accept': 'application/json',
        'User-Agent': 'Python-API-Senado/1.0'})

    
    def _comissao(self, cod_colegiado):
        """
        Detalhes de um Colegiado do Congresso Nacional
        Em desuso pois usa api do senado
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

    def busca_deputados_atual(self):
        """
        Busca lista de todos os deputados em exercício        
        Se não for passado um parâmetro de tempo, como idLegislatura ou dataInicio, a lista enumerará somente os deputados em exercício no momento da requisição.
        """
        endpoint = f"/deputados"
        url = f"{self.url_base}{endpoint}"
        try:
            response = self.session.get(url, timeout=25)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Tempo limite exedido para {url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: \n {e}")
            
    def busca_deputado(self, id):
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
        
