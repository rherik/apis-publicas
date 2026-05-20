# src/main.py
# from api_senado import APISenado
import os
from processador_dados import ProcessadorDadosCamara, ProcessadorDadosSenado
from dados_org import FonteBaseDosDados
import pandas as pd
from api_camara import APICamara
import logging
from time import sleep
from dotenv import load_dotenv

load_dotenv()
api_camara = APICamara()
api_org = FonteBaseDosDados()

# def servico_senado():
#     api = APISenado()
    
#     # Buscar senadores
#     senadores = api.buscar_senadores_atuais()
    #  df_senadores = ProcessadorDadosSenado.senadores_para_dataframe(senadores)
    
#     print(f"Encontrados {len(df_senadores)} senadores")
#     df_senadores.to_csv('../data/senadores.csv', index=False)

def caminho_arquivo(params:str = ''):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, f"{params}.csv")
    return csv_path

def salva_arquivo(dataframe: pd.DataFrame, params:str = ''):
    """Salva DataFrame fornecido. Escrever nome do arquivo de acordo com os parâmetros"""
    dataframe.to_csv(caminho_arquivo(params=params), index=False, sep=',', encoding="UTF-8")

def retorna_deputados():
    paramsMulheres = {'dataInicio': '2023-02-01', 'dataFim': '2027-01-31', 'siglaSexo': 'F'} #Isso é params = {'idLegislatura': 57}
    paramsHomens = {'dataInicio': '2023-02-01', 'dataFim': '2027-01-31', 'siglaSexo': 'M'} #Isso é params = {'idLegislatura': 57}

    deputadasMulheres = api_camara.busca_deputados_atual(**paramsMulheres)
    deputadosHomens = api_camara.busca_deputados_atual(**paramsHomens)

    df_deputadas_mulheres = ProcessadorDadosCamara.deputados_para_dataframe(deputadasMulheres.get('dados', []), sigla_sexo='Feminino')
    df_deputados_homens = ProcessadorDadosCamara.deputados_para_dataframe(deputadosHomens.get('dados', []), sigla_sexo='Masculino')

    df_deputados = pd.concat([df_deputadas_mulheres, df_deputados_homens], ignore_index=True)

    df_deputados = df_deputados.drop_duplicates(subset='id')

    print(f"Encontrados {len(df_deputados)} deputados.")
    print('id - Nome - Id do Deputado - Sigla do partido - Legislatura - UF - Sigla Sexo')
    for index, deputado in df_deputados.iterrows():
        sleep(0.8)
        print(f"{index+1} - {deputado['nome']} - {deputado['id']} - {deputado['siglaPartido']} - {deputado['idLegislatura']} - {deputado['siglaUf']} - {deputado['siglaSexo']}")

    salva_arquivo(dataframe=df_deputados, params='M_F_discriminados_legis57')
    
def detalhes_deputado(nome):
    usecols=["id", "nome"]
    df = pd.read_csv(caminho_arquivo('deputados_2024.csv'), index_col="id", usecols=usecols, sep=';')
    for id_dep, row in df.iterrows():
        if nome.lower() in row["nome"].lower():
            print(f"Deputado(a) encontrado {row["nome"]} - {id_dep}")
            deputados = api_camara.busca_deputado(id=id_dep)
            
            print(deputados)

def detalhes_despesas(nome):
    usecols=["id", "nome"]
    df = pd.read_csv(caminho_arquivo('deputados_2024'), index_col="id", usecols=usecols, sep=';')
    for id_dep, row in df.iterrows():
        if nome.lower() in row["nome"].lower():
            print(f"{row["nome"]} de ID {id_dep} encontrado(a) para exibir as despesas.\n")
            
            params = {'ano': '2024'}
            despesas = api_camara.busca_despesas(id=id_dep, **params)
            df_despesas = ProcessadorDadosCamara.despesas_para_dataframe(despesas['dados'])
            
            #print(df_despesas)
            salva_arquivo(df_despesas, f"despesas_{nome}")
            
def bd_bens():
    fonte_base_dos_dados = api_org.bens_candidatos()
    salva_arquivo(fonte_base_dos_dados, 'bens_deputados_rj')
    

def fonte_frente_deputado():
    fonte_base_dos_dados = api_org.frente_deputado(id_deputado='204464')
    return fonte_base_dos_dados
    
def bd_candidatos():
    fonte_bd_candidatos = api_org.bd_candidatos()
    salva_arquivo(dataframe=fonte_bd_candidatos, params='candidatos_em_eleicoes')
    return fonte_bd_candidatos

def bd_receitas_por_candidato():
    fonte_bd = api_org.receitas_por_candidato()
    salva_arquivo(fonte_bd, 'receitas_por_candidato')
    return fonte_bd

def arquivos_iniciais():
    retorna_deputados()

def main():
    # Arquivos a serem criados
    # Todos os deputados da legislatura atual (2023-2027)
    # Retornar Deputados por estado e sexo
    pass

if __name__ == "__main__":
    retorna_deputados()
    #detalhes_deputado(nome='')
    #detalhes_despesas(nome='')
    #print(api.busca_deputados_atual())
    #print(bd_bens())
    #print(fonte_frente_deputado())
    #print(bd_candidatos())
    #print(bd_receitas_por_candidato())
