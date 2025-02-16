import requests
import pandas as pd

def get_bcb_data(codigo_serie, data_inicio="2000-01-01"):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json"
    
    response = requests.get(url)
    
    # Novo bloco para depuração
    print(f"Status Code: {response.status_code}")
    print(f"Resposta da API: {response.text[:500]}")  # Mostra os primeiros 500 caracteres

    if response.status_code != 200:
        print("Erro ao buscar os dados. Verifique o código da série.")
        return None
    
    try:
        data = response.json()
    except Exception as e:
        print("Erro ao converter JSON:", e)
        return None
    
    df = pd.DataFrame(data)
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)  
    df["valor"] = df["valor"].astype(float)
    
    return df

df = get_bcb_data(433)



