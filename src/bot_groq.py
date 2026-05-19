import os
import pandas as pd
import time
from groq import Groq
from rich import print

def configurar_groq(api_key):
    """Inicializa o cliente da Groq."""
    return Groq(api_key=api_key)

def analisar_pautas(client, objeto, perfil, index, total):
    prompt = f"""
    Você é um jornalista que irá informar de forma clara uma pauta votada na câmara dos depudados.
    
    PERFIL DA PAUTA:
    {perfil}
    
    OBJETO DA LICITAÇÃO:
    {objeto}
    
    Responda ESTRITAMENTE no formato abaixo, sem texto adicional:
    STATUS: [ATENDE, NÃO ATENDE ou ATENDE PARCIALMENTE]
    JUSTIFICATIVA: [Sua justificativa baseada no perfil e no objeto, destacando pontos de atenção ou adequação]
    """
    
    max_retries = 3
    
    for tentativa in range(max_retries):
        try:
            # Requisição para a API da Groq usando o Llama 3
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-8b-instant",
                temperature=0.1, # Temperatura baixa para garantir que ele siga o formato estrito
            )
            
            texto = chat_completion.choices[0].message.content
            
            status = "DÚVIDA"
            justificativa = "Não foi possível extrair a justificativa da IA."
            
            for linha in texto.split('\n'):
                if linha.upper().startswith("STATUS:"):
                    status = linha.split(":", 1)[1].strip()
                elif linha.upper().startswith("JUSTIFICATIVA:"):
                    justificativa = linha.split(":", 1)[1].strip()
                    
            # A Groq é muito rápida, mas o plano gratuito permite ~30 requisições por minuto.
            # Essa pausa de 2.5s garante que o bot faça 24 requisições por minuto com segurança.
            time.sleep(2.5) 
            return status, justificativa
            
        except Exception as e:
            erro_str = str(e)
            
            # Tratamento do Rate Limit da Groq
            if "429" in erro_str or "rate limit" in erro_str.lower():
                espera = 15 
                print(f"⏳ [GROQ] Limite atingido ({index+1}/{total}). Pausa de {espera}s (Tentativa {tentativa+1}/3)...")
                time.sleep(espera)
            else:
                print(f"❌ [GROQ] Erro na linha {index+1}: {e}")
                time.sleep(3) 
                
    return "ERRO IA", "Falha após múltiplas tentativas de comunicação com a API."

# def processar_lote_ia(df, api_key, perfil_empresa):
#     if df.empty:
#         return df
        
#     print(f"\n🧠 [GROQ] Iniciando análise de {len(df)} licitações com Llama 3...")
    
#     try:
#         client = configurar_groq(api_key)
#     except Exception as e:
#         print(f"❌ [GROQ] Erro ao configurar API: {e}")
#         return df
    
#     status_list = []
#     just_list = []
#     total_linhas = len(df)
    
#     for index, row in df.iterrows():
#         objeto = row.get('Objeto da Licitação', 'Não informado')
#         num_processo = row.get('Num. Processo', 'S/N')
        
#         print(f"🔎 [GROQ] Analisando {index + 1}/{total_linhas} | Processo: {num_processo}")
        
#         status, just = analisar_pautas(client, objeto, perfil_empresa, index, total_linhas)
        
#         status_list.append(status)
#         just_list.append(just)
        
#     df['IA_STATUS'] = status_list
#     df['IA_JUSTIFICATIVA'] = just_list
    
#     print("✅ [GROQ] Análise concluída com sucesso.")
#     return df