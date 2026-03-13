import os
import basedosdados as bd
from dotenv import load_dotenv

load_dotenv()

BILLING_PROJECT = os.environ['USER']

query = """
  SELECT
    dados.ano as ano,
    dados.sigla_uf AS sigla_uf,
    diretorio_sigla_uf.nome AS sigla_uf_nome,
    dados.tipo_eleicao as tipo_eleicao,
    dados.data_eleicao as data_eleicao
  FROM `basedosdados.br_tse_eleicoes.bens_candidato` AS dados
  LEFT JOIN (SELECT DISTINCT sigla, nome FROM `basedosdados.br_bd_diretorios_brasil.uf`) AS diretorio_sigla_uf
    ON dados.sigla_uf = diretorio_sigla_uf.sigla
"""

df = bd.read_sql(
    query=query,
    billing_project_id=BILLING_PROJECT
    #from_file=True  # ESSENCIAL: força o uso das credenciais do arquivo definido em GOOGLE_APPLICATION_CREDENTIALS
)

print(df.head())