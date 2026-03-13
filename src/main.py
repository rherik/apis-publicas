# src/main.py
# from api_senado import APISenado
# from processador_dados import ProcessadorDadosSenado
import os
from processador_dados import ProcessadorDadosCamara
import pandas as pd
from api_camara import APICamara

# def servico_senado():
#     api = APISenado()
    
#     # Buscar senadores
#     senadores = api.buscar_senadores_atuais()
    #  df_senadores = ProcessadorDadosSenado.senadores_para_dataframe(senadores)
    
#     print(f"Encontrados {len(df_senadores)} senadores")
#     df_senadores.to_csv('../data/senadores.csv', index=False)

def get_file():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, 'deputados.csv')
    return csv_path

def servico_camara():
    api = APICamara()
    #deputados = api.comissao(cod_colegiado='449')
    deputados = api.busca_deputados_atual()
    df_deputados = ProcessadorDadosCamara.deputados_para_dataframe(deputados['dados'])
    print(f"Encontrados {len(df_deputados)} deputados.")
    df_deputados.to_csv(get_file(), index=False, sep=';')
    #print(deputados)
    
def detalhes_deputado(nome):
    api = APICamara()
    usecols=["id", "nome"]
    df = pd.read_csv(get_file(), index_col="id", usecols=usecols, sep=';')
    for id_dep, row in df.iterrows():
        if nome.lower() in row["nome"].lower():
            print(f"Deputado(a) encontrado {row["nome"]} - {id_dep}")
            deputados = api.busca_deputado(id=id_dep)
            print(deputados)

if __name__ == "__main__":
    #servico_camara()
    detalhes_deputado(nome='Talíria')