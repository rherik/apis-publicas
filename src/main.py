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

def servico_camara():
    api = APICamara()
    #deputados = api.comissao(cod_colegiado='449')
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, 'deputados.csv')
    deputados = api.busca_deputados_atual()
    df_deputados = ProcessadorDadosCamara.deputados_para_dataframe(deputados['dados'])
    print(f"Encontrados {len(df_deputados)} deputados.")
    df_deputados.to_csv(csv_path, index=False)
    #print(deputados)

if __name__ == "__main__":
    servico_camara()