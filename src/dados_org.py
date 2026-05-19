import os
import basedosdados as bd
from dotenv import load_dotenv

load_dotenv()

class FonteBaseDosDados:
  """
  Fontes originais
  https://dadosabertos.tse.jus.br/
  """

  def __init__(self):
    self.billing_id = os.environ['USER']
    
  def bens_candidatos(self):
    """
    Declaração de bens de candidatos em eleições brasileiras.
    Última atualização: 22/11/2024
    """
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
    """
    Dados de candidatos em eleições brasileiras.
    Cobertura temporal: 1994 à 2024
    Última atualização: 22/11/2024
    """
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
      WHERE data_eleicao >= '2024-01-01' 
      AND tipo_eleicao = 'eleicao ordinaria' 
      AND sigla_uf = 'RJ'
      --AND cargo = 'deputado federal'
      --AND sigla_partido = 'PSOL'
      --AND nome_urna = 'Taliria Petrone'
      ORDER BY data_eleicao
      LIMIT 25
          """
    df = bd.read_sql(
      query=query,
      billing_project_id=self.billing_id
      #reauth=True
    )
    return df
  
  def receitas_por_candidato(self):
    """
    Dados de financiamento de campanha de receita para candidatos.
    Cobertura temporal: 2002 à 2024
    Ultima atualização: 22/11/2024
    
    ☢️☢️ ATENÇÃOOOOO!!! ☢️☢️
    Essa tabela completa, com todas as colunas, tem 5.15 GB. Cuidado para não ultrapassar o limite de processamento gratuito do BigQuery.
    Para otimizar a consulta, você pode selecionar menos colunas ou adicionar filtros no BigQuery.
    """

    query = """
      SELECT
        dados.ano as ano,
        dados.turno as turno,
        dados.id_eleicao as id_eleicao,
        dados.tipo_eleicao as tipo_eleicao,
        dados.data_eleicao as data_eleicao,
        dados.sigla_uf AS sigla_uf,
        diretorio_sigla_uf.nome AS sigla_uf_nome,
        dados.id_municipio AS id_municipio,
        diretorio_id_municipio.nome AS id_municipio_nome,
        dados.id_municipio_tse AS id_municipio_tse,
        diretorio_id_municipio_tse.nome AS id_municipio_tse_nome,
        dados.titulo_eleitoral_candidato as titulo_eleitoral_candidato,
        dados.sequencial_candidato as sequencial_candidato,
        dados.numero_candidato as numero_candidato,
        dados.cnpj_candidato as cnpj_candidato,
        dados.numero_partido as numero_partido,
        dados.sigla_partido as sigla_partido,
        dados.cargo as cargo,
        dados.sequencial_receita as sequencial_receita,
        dados.data_receita as data_receita,
        dados.fonte_receita as fonte_receita,
        dados.origem_receita as origem_receita,
        dados.natureza_receita as natureza_receita,
        dados.especie_receita as especie_receita,
        dados.situacao_receita as situacao_receita,
        dados.descricao_receita as descricao_receita,
        dados.valor_receita as valor_receita,
        dados.sequencial_candidato_doador as sequencial_candidato_doador,
        dados.cpf_cnpj_doador as cpf_cnpj_doador,
        dados.sigla_uf_doador as sigla_uf_doador,
        dados.id_municipio_tse_doador as id_municipio_tse_doador,
        dados.nome_doador as nome_doador,
        dados.nome_doador_rf as nome_doador_rf,
        dados.cargo_candidato_doador as cargo_candidato_doador,
        dados.numero_partido_doador as numero_partido_doador,
        dados.sigla_partido_doador as sigla_partido_doador,
        dados.esfera_partidaria_doador as esfera_partidaria_doador,
        dados.numero_candidato_doador as numero_candidato_doador,
        dados.cnae_2_doador as cnae_2_doador,
        dados.cnae_2_doador_classe as cnae_2_doador_classe,
        dados.cnae_2_doador_subclasse AS cnae_2_doador_subclasse,
        diretorio_cnae_2_doador_subclasse.descricao_subclasse AS cnae_2_doador_subclasse_descricao_subclasse,
        diretorio_cnae_2_doador_subclasse.descricao_classe AS cnae_2_doador_subclasse_descricao_classe,
        diretorio_cnae_2_doador_subclasse.descricao_grupo AS cnae_2_doador_subclasse_descricao_grupo,
        diretorio_cnae_2_doador_subclasse.descricao_divisao AS cnae_2_doador_subclasse_descricao_divisao,
        diretorio_cnae_2_doador_subclasse.descricao_secao AS cnae_2_doador_subclasse_descricao_secao,
        dados.descricao_cnae_2_doador as descricao_cnae_2_doador,
        dados.cpf_cnpj_doador_orig as cpf_cnpj_doador_orig,
        dados.nome_doador_orig as nome_doador_orig,
        dados.nome_doador_orig_rf as nome_doador_orig_rf,
        dados.tipo_doador_orig as tipo_doador_orig,
        dados.descricao_cnae_2_doador_orig as descricao_cnae_2_doador_orig,
        dados.nome_administrador as nome_administrador,
        dados.cpf_administrador as cpf_administrador,
        dados.numero_recibo_eleitoral as numero_recibo_eleitoral,
        dados.numero_documento as numero_documento,
        dados.numero_recibo_doacao as numero_recibo_doacao,
        dados.numero_documento_doacao as numero_documento_doacao,
        dados.tipo_prestacao_contas as tipo_prestacao_contas,
        dados.data_prestacao_contas as data_prestacao_contas,
        dados.sequencial_prestador_contas as sequencial_prestador_contas,
        dados.cnpj_prestador_contas as cnpj_prestador_contas,
        dados.entrega_conjunto as entrega_conjunto
      FROM `basedosdados.br_tse_eleicoes.receitas_candidato` AS dados
      LEFT JOIN (SELECT DISTINCT sigla,nome  FROM `basedosdados.br_bd_diretorios_brasil.uf`) AS diretorio_sigla_uf
          ON dados.sigla_uf = diretorio_sigla_uf.sigla
      LEFT JOIN (SELECT DISTINCT id_municipio,nome  FROM `basedosdados.br_bd_diretorios_brasil.municipio`) AS diretorio_id_municipio
          ON dados.id_municipio = diretorio_id_municipio.id_municipio
      LEFT JOIN (SELECT DISTINCT id_municipio_tse,nome  FROM `basedosdados.br_bd_diretorios_brasil.municipio`) AS diretorio_id_municipio_tse
          ON dados.id_municipio_tse = diretorio_id_municipio_tse.id_municipio_tse
      LEFT JOIN (SELECT DISTINCT subclasse,descricao_subclasse,descricao_classe,descricao_grupo,descricao_divisao,descricao_secao  FROM `basedosdados.br_bd_diretorios_brasil.cnae_2`) AS diretorio_cnae_2_doador_subclasse
          ON dados.cnae_2_doador_subclasse = diretorio_cnae_2_doador_subclasse.subclasse
      WHERE ano = 2024
        --AND cnpj_candidato IS NOT NULL
      LIMIT 20
      """
    df = bd.read_sql(
      query=query,
      billing_project_id=self.billing_id
    )
    return df
