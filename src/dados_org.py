import os
import basedosdados as bd
from dotenv import load_dotenv

load_dotenv()

class FonteBaseDosDados:
  def __init__(self):
    self.billing_id = os.environ['USER']
    
  def bens_deputado(self):
    query_tudo_de_bens = """
      SELECT
        dados.ano as ano,
        dados.sigla_uf AS sigla_uf,
        diretorio_sigla_uf.nome AS sigla_uf_nome,
        dados.id_eleicao as id_eleicao,
        dados.tipo_eleicao as tipo_eleicao,
        dados.data_eleicao as data_eleicao,
        dados.titulo_eleitoral_candidato as titulo_eleitoral_candidato,
        dados.sequencial_candidato as sequencial_candidato,
        dados.tipo_item as tipo_item,
        dados.descricao_item as descricao_item,
        dados.valor_item as valor_item
      FROM `basedosdados.br_tse_eleicoes.bens_candidato` AS dados
      LEFT JOIN (SELECT DISTINCT sigla,nome  FROM `basedosdados.br_bd_diretorios_brasil.uf`) AS diretorio_sigla_uf
          ON dados.sigla_uf = diretorio_sigla_uf.sigla
      WHERE dados.ano = 2024 AND dados.sigla_uf = 'RJ'
      LIMIT 10 
    """
    df = bd.read_sql(
    query=query_tudo_de_bens,
    billing_project_id=self.billing_id,
    reauth=True
    )
    return df
  
  def frente_deputado(self):
    query = """
      SELECT
        dados.id_frente as id_frente,
        dados.id_deputado as id_deputado,
        dados.titulo_deputado as titulo_deputado,
        dados.nome_deputado as nome_deputado,
        dados.titulo_deputado as titulo_deputado,
        --dados.id_legislatura_deputado as id_legislatura_deputado
      FROM `basedosdados.br_camara_dados_abertos.frente_deputado` AS dados
      LIMIT 10
    """
    df = bd.read_sql(
      query=query,
      billing_project_id=self.billing_id,
      reauth=True
    )
    return df
