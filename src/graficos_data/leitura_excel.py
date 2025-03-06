import pandas as pd

arquivo_geracao = "data/brutos/Dados_Geração_Fotovoltaica.xlsx"
arquivo_meteorologicos = "data/brutos/Dados_Meteorologicos.xlsx"

# Carrega os dados de geração e meteorológicos
dados_geracao = pd.read_excel(arquivo_geracao, sheet_name=None)
dados_meteorologicos = pd.read_excel(arquivo_meteorologicos)

# DataFrame para consolidar os dados de geração
df_geracao_completo = pd.DataFrame()

for nome_aba, df in dados_geracao.items():
    df["SFCR_ID"] = nome_aba
    df_geracao_completo = pd.concat([df_geracao_completo, df], ignore_index=True)

# Padroniza os nomes dos SFCRs
df_geracao_completo["SFCR_ID"] = df_geracao_completo["SFCR_ID"].replace({
    "SFCR_1A": "SFCR_1",
    "SFCR_1B": "SFCR_1",
    "SFCR_1C": "SFCR_1"
})

# Agrupa por data e SFCR_ID somando os valores
df_geracao_completo = df_geracao_completo.groupby(["Data", "SFCR_ID"], as_index=False).sum()

print(f"Df completo após somar SFCR_1A, 1B, 1C:")
print(df_geracao_completo.head())
print(f"{df_geracao_completo.shape[0]} linhas")

# Padroniza os nomes das colunas para evitar problemas de espaços extras
dados_meteorologicos.columns = dados_meteorologicos.columns.str.strip()

# Converte a coluna Data para datetime
dados_meteorologicos["Data"] = pd.to_datetime(dados_meteorologicos["Data"])

# Agrupa os dados meteorológicos por dia, calculando médias
df_meteorologicos_diario = dados_meteorologicos.groupby("Data", as_index=False).agg({
    "Temp. Ins. (C)": "mean",
    "Chuva (mm)": "mean",
    "Radiacao": "sum"  # Agora inclui a soma da Radiação
})

print(f"Dados Meteorológicos Diários:")
print(df_meteorologicos_diario.head())
print(f"{df_meteorologicos_diario.shape[0]} linhas")

# Junta os dados meteorológicos com os dados de geração
df_completo = df_geracao_completo.merge(df_meteorologicos_diario, on="Data", how="left")

print(f"DataFrame após merge com dados meteorológicos:")
print(df_completo.head())

print(f"Total de linhas após o merge: {df_completo.shape[0]}")
