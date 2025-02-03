import pandas as pd
import matplotlib.pyplot as plt

#Leitura dos dados Excel
arquivo_geracao = "data/brutos/Dados_Geração_Fotovoltaica.xlsx"
arquivo_meteorologicos = "data/brutos/Dados_Meteorologicos.xlsx"

dados_geracao = pd.read_excel(arquivo_geracao, sheet_name= None)
dados_meteorologicos = pd.read_excel(arquivo_meteorologicos)

for nome_aba, df in dados_geracao.items():
    print(f"\nAba: {nome_aba}")
    print(df.head())
    
print("nDados Meteorologicos:")
print(dados_meteorologicos.head())

#Criação Dataframe

df_geracao_completo = pd.DataFrame()

for nome_aba, df in dados_geracao.items():
    df["SFCR_ID"] = nome_aba
    df_geracao_completo = pd.concat([df_geracao_completo, df],ignore_index=True)

print(f"Df completo:")    
print(df_geracao_completo.head())
print({df_geracao_completo.shape[0]})

#Conversões para formatos corretos
# Mostrar os nomes reais das colunas do DataFrame meteorológico


##Data para formato correto Dd/Mm/Yy>>>
dados_meteorologicos["Data"] = pd.to_datetime(dados_meteorologicos["Data"])

# Agrupar por Data e calcular a média diária da temperatura e da chuva
df_meteorologicos_diario = dados_meteorologicos.groupby("Data", as_index=False).agg({
    "Temp. Ins. (C)": "mean",  # Temperatura
    "Chuva (mm)": "mean"  # Chuva
})

# Exibir as primeiras linhas
print(df_meteorologicos_diario.head())
print(df_meteorologicos_diario.shape[0])

# Realizar o merge entre os dados de geração e os dados meteorológicos
df_completo = df_geracao_completo.merge(df_meteorologicos_diario, on="Data", how="left")

# Exibir algumas linhas para conferir
print(df_completo.head())

# Confirmar se o número de linhas está correto
print(f"Total de linhas após o merge: {df_completo.shape[0]}")

