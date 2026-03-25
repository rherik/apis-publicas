# src/main.py
# from api_senado import APISenado
import os
from processador_dados import ProcessadorDadosCamara, ProcessadorDadosSenado
from dados_org import FonteBaseDosDados
import pandas as pd
from api_camara import APICamara
import logging
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
    arquivo = dataframe.to_csv(caminho_arquivo(params=params), index=False, sep=';', encoding="UTF-8")
    return arquivo

def retorna_todos_deputados():
    params = {'dataInicio': '2024-01-01', 'dataFim': '2024-12-31'}
    deputados = api_camara.busca_deputados_atual(**params)
    df_deputados = ProcessadorDadosCamara.deputados_para_dataframe(deputados['dados'])
    print(f"Encontrados {len(df_deputados)} deputados.")
    for index, deputado in df_deputados.iterrows():
        print(f"{index+1} - {deputado['nome']} - {deputado['id']} - {deputado['siglaPartido']} - {deputado['idLegislatura']} - {deputado['siglaUf']}")
    salva_arquivo(dataframe=df_deputados, params='2024')
    
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
            
def fonte_base_dos_dados():
    fonte_base_dos_dados = api_org.bens_deputado()
    print(fonte_base_dos_dados)

def fonte_frente_deputado():
    fonte_base_dos_dados = api_org.frente_deputado(id_deputado='204464')
    print(fonte_base_dos_dados)
    
def bd_candidatos():
    fonte_bd_candidatos = api_org.bd_candidatos()
    salva_arquivo(dataframe=fonte_bd_candidatos, params='candidatos_em_eleicoes')
    return fonte_bd_candidatos

if __name__ == "__main__":
    #retorna_todos_deputados()
    #detalhes_deputado(nome='')
    detalhes_despesas(nome='')
    #print(api.busca_deputados_atual())
    #fonte_frente_deputado()
    #print(bd_candidatos())
