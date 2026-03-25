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
    #reauth=True
    )
    return df
  
  def frente_deputado(self, id_deputado: str):
    query = f"""
      SELECT
        dados.id_frente as id_frente,
        dados.id_deputado as id_deputado,
        dados.titulo_deputado as titulo_deputado,
        dados.nome_deputado as nome_deputado,
        dados.titulo_deputado as titulo_deputado,
        --dados.id_legislatura_deputado as id_legislatura_deputado
      FROM `basedosdados.br_camara_dados_abertos.frente_deputado` AS dados
      WHERE id_deputado = '{id_deputado}'
    """
    df = bd.read_sql(
      query=query,
      billing_project_id=self.billing_id,
      #reauth=True
    )
    return df

  def bd_candidatos(self):
    "Dados de candidatos em eleições brasileiras."
    query = """
      SELECT
          dados.ano as ano,
          dados.id_eleicao as id_eleicao,
          dados.tipo_eleicao as tipo_eleicao,
          dados.data_eleicao as data_eleicao,
          dados.sigla_uf AS sigla_uf,
          diretorio_sigla_uf.nome AS sigla_uf_nome,
          dados.id_municipio AS id_municipio,
          diretorio_id_municipio.nome AS id_municipio_nome,
          dados.id_municipio_tse AS id_municipio_tse,
          diretorio_id_municipio_tse.nome AS id_municipio_tse_nome,
          dados.titulo_eleitoral as titulo_eleitoral,
          dados.cpf as cpf,
          dados.sequencial as sequencial,
          dados.numero as numero,
          dados.nome as nome,
          dados.nome_urna as nome_urna,
          dados.numero_partido as numero_partido,
          dados.sigla_partido as sigla_partido,
          dados.cargo as cargo,
          dados.situacao as situacao,
          dados.data_nascimento as data_nascimento,
          dados.idade as idade,
          dados.genero as genero,
          dados.instrucao as instrucao,
          dados.ocupacao as ocupacao,
          dados.estado_civil as estado_civil,
          dados.nacionalidade as nacionalidade,
          dados.sigla_uf_nascimento as sigla_uf_nascimento,
          dados.municipio_nascimento as municipio_nascimento,
          dados.email as email,
          dados.raca as raca
      FROM `basedosdados.br_tse_eleicoes.candidatos` AS dados
      LEFT JOIN (SELECT DISTINCT sigla,nome  FROM `basedosdados.br_bd_diretorios_brasil.uf`) AS diretorio_sigla_uf
          ON dados.sigla_uf = diretorio_sigla_uf.sigla
      LEFT JOIN (SELECT DISTINCT id_municipio,nome  FROM `basedosdados.br_bd_diretorios_brasil.municipio`) AS diretorio_id_municipio
          ON dados.id_municipio = diretorio_id_municipio.id_municipio
      LEFT JOIN (SELECT DISTINCT id_municipio_tse,nome  FROM `basedosdados.br_bd_diretorios_brasil.municipio`) AS diretorio_id_municipio_tse
          ON dados.id_municipio_tse = diretorio_id_municipio_tse.id_municipio_tse
      WHERE data_eleicao >= '2021-01-01' AND tipo_eleicao = 'eleicao ordinaria'
      ORDER BY data_eleicao
          """
    df = bd.read_sql(
      query=query,
      billing_project_id=self.billing_id,
      #reauth=True
    )
    return df
