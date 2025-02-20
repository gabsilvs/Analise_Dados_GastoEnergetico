import pandas as pd

# Leitura dos dados Excel
arquivo_geracao = "data/brutos/Dados_Geração_Fotovoltaica.xlsx"
arquivo_meteorologicos = "data/brutos/Dados_Meteorologicos.xlsx"

dados_geracao = pd.read_excel(arquivo_geracao, sheet_name=None)
dados_meteorologicos = pd.read_excel(arquivo_meteorologicos)

# Criação do DataFrame de geração de energia
df_geracao_completo = pd.DataFrame()

for nome_aba, df in dados_geracao.items():
    df["SFCR_ID"] = nome_aba
    df_geracao_completo = pd.concat([df_geracao_completo, df], ignore_index=True)

# Somar SFCR_1A, SFCR_1B, SFCR_1C e transformá-los em SFCR_1
df_geracao_completo["SFCR_ID"] = df_geracao_completo["SFCR_ID"].replace({"SFCR_1A": "SFCR_1", "SFCR_1B": "SFCR_1", "SFCR_1C": "SFCR_1"})
df_geracao_completo = df_geracao_completo.groupby(["Data", "SFCR_ID"], as_index=False).sum()

# Exibir o DataFrame completo após a soma
print(f"Df completo após somar SFCR_1A, 1B, 1C:")    
print(df_geracao_completo.head())
print(f"{df_geracao_completo.shape[0]} linhas")

# Conversões para formatos corretos
# Data para formato correto (Dd/Mm/Yy >> YYYY-MM-DD)
dados_meteorologicos["Data"] = pd.to_datetime(dados_meteorologicos["Data"])

# Agrupar por Data e calcular a média diária da temperatura e da chuva
df_meteorologicos_diario = dados_meteorologicos.groupby("Data", as_index=False).agg({
    "Temp. Ins. (C)": "mean",  # Temperatura
    "Chuva (mm)": "mean"  # Chuva
})

# Exibir as primeiras linhas
print(f"Dados Meteorológicos Diários:")
print(df_meteorologicos_diario.head())
print(f"{df_meteorologicos_diario.shape[0]} linhas")

# Realizar o merge entre os dados de geração e os dados meteorológicos
df_completo = df_geracao_completo.merge(df_meteorologicos_diario, on="Data", how="left")

# Exibir o DataFrame completo após o merge
print(f"DataFrame após merge com dados meteorológicos:")
print(df_completo.head())

# Confirmar se o número de linhas está correto
print(f"Total de linhas após o merge: {df_completo.shape[0]}")
