# src/main.py
# from api_senado import APISenado
import os
from processador_dados import ProcessadorDadosCamara, ProcessadorDadosSenado
import pandas as pd
from api_camara import APICamara
import logging
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.experimental.query_engine.pandas import PandasQueryEngine

load_dotenv()
groq_key = os.environ['GROQ_KEY']
api = APICamara()
llm = Groq(model='llama-3.3-70b-versatile', api_key=groq_key)

# def servico_senado():
#     api = APISenado()
    
#     # Buscar senadores
#     senadores = api.buscar_senadores_atuais()
    #  df_senadores = ProcessadorDadosSenado.senadores_para_dataframe(senadores)
    
#     print(f"Encontrados {len(df_senadores)} senadores")
#     df_senadores.to_csv('../data/senadores.csv', index=False)

def caminho_arquivo(params):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, f"deputados-{params}.csv")
    return csv_path

def salva_arquivo(dataframe):
    """Salva DataFrame fornecido. Escrever nome do arquivo de acordo com os parâmetros"""
    arquivo = dataframe.to_csv(caminho_arquivo(), index=False, sep=';')
    return arquivo

def retorna_todos_deputados():
    params = {'siglaPartido': 'PSOL', 'dataInicio': '2023-01-01', 'dataFim': '2023-12-31'}
    deputados = api.busca_deputados_atual(**params)
    df_deputados = ProcessadorDadosCamara.deputados_para_dataframe(deputados['dados'])
    print(f"Encontrados {len(df_deputados)} deputados.")
    # for index, deputado in df_deputados.iterrows():
    #     print(f"{index+1} - {deputado['nome']} - {deputado['id']} - {deputado['siglaPartido']} - {deputado['idLegislatura']} - {deputado['siglaUf']}")
    query_engine = PandasQueryEngine(df=df_deputados, llm=llm, verbose=True)
    response = query_engine.query('Quais deputados tiveram mais de um mandato?')
    print(response)

    
def detalhes_deputado(nome):
    usecols=["id", "nome"]
    df = pd.read_csv(caminho_arquivo(), index_col="id", usecols=usecols, sep=';')
    for id_dep, row in df.iterrows():
        if nome.lower() in row["nome"].lower():
            print(f"Deputado(a) encontrado {row["nome"]} - {id_dep}")
            deputados = api.busca_deputado(id=id_dep)
            print(deputados)

def detalhes_despesas(nome):
    usecols=["id", "nome"]
    df = pd.read_csv(caminho_arquivo(), index_col="id", usecols=usecols, sep=';')
    for id_dep, row in df.iterrows():
        if nome.lower() in row["nome"].lower():
            print(f"{row["nome"]} de ID {id_dep} encontrado(a) para exibir as despesas.\n")

            despesas = api.busca_despesas(id=id_dep)
            df_despesas = ProcessadorDadosCamara.despesas_para_dataframe(despesas['dados'])
            print(df_despesas)

if __name__ == "__main__":
    retorna_todos_deputados()
    #detalhes_despesas(nome='Talíria')
    #print(api.busca_deputados_atual())
