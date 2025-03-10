import pandas as pd
import matplotlib.pyplot as plt
from leitura_excel import df_completo

# Removendo espaços em branco dos nomes das colunas
df_completo.columns = df_completo.columns.str.strip()

# Agrupando SFCR_1A, SFCR_1B e SFCR_1C em SFCR_1
df_completo["SFCR_ID"] = df_completo["SFCR_ID"].replace({"SFCR_1A": "SFCR_1", "SFCR_1B": "SFCR_1", "SFCR_1C": "SFCR_1"})

# Agrupando os dados por Data e SFCR_ID e somando os valores
df_completo = df_completo.groupby(["Data", "SFCR_ID"], as_index=False).sum()

# Criando figura e eixo principal
fig, ax1 = plt.subplots(figsize=(20, 6))

# Cores dos SFCRs
cores_energia = {"SFCR_1": "blue", "SFCR_2": "red"}

# Plotando geração de energia para cada SFCR
for sfcr, cor in cores_energia.items():
    df_filtrado = df_completo[df_completo["SFCR_ID"] == sfcr]
    df_filtrado = df_filtrado.groupby("Data")["E_gerada [kW/h]"].sum().reset_index()
    df_filtrado["E_gerada_MM7"] = df_filtrado["E_gerada [kW/h]"].rolling(window=7, min_periods=1).mean()
    ax1.plot(df_filtrado["Data"], df_filtrado["E_gerada_MM7"], label=sfcr, color=cor, linewidth=1)

# Criando eixo secundário para a radiação e temperatura
ax2 = ax1.twinx()

# Média móvel de 7 dias da Radiação
df_radiacao = df_completo.groupby("Data")["Radiacao"].sum().reset_index()
df_radiacao["Radiacao_MM7"] = df_radiacao["Radiacao"].rolling(window=7, min_periods=1).mean()

# Média móvel de 7 dias da Temperatura
df_temperatura = df_completo.groupby("Data")["Temp. Ins. (C)"].mean().reset_index()
df_temperatura["Temp_MM7"] = df_temperatura["Temp. Ins. (C)"].rolling(window=7, min_periods=1).mean()

# 🔹 Normalizando radiação e temperatura para ficarem na mesma escala
radiacao_max = df_radiacao["Radiacao_MM7"].max()
temperatura_max = df_temperatura["Temp_MM7"].max()

df_radiacao["Radiacao_Normalizada"] = df_radiacao["Radiacao_MM7"] / radiacao_max
df_temperatura["Temp_Normalizada"] = df_temperatura["Temp_MM7"] / temperatura_max

# Plotando os dados normalizados
ax2.plot(df_radiacao["Data"], df_radiacao["Radiacao_Normalizada"], label="Radiação (Normalizada)", color="orange", linestyle="--", linewidth=1.5)
ax2.plot(df_temperatura["Data"], df_temperatura["Temp_Normalizada"], label="Temperatura (Normalizada)", color="green", linestyle="-.", linewidth=1.5)

# Configurações dos eixos
ax1.set_xlabel("Data")
ax1.set_ylabel("Geração de Energia [kWh]")
ax2.set_ylabel("Escala Normalizada")

# Título do gráfico
ax1.set_title("Geração de Energia x Radiação x Temperatura (Média Móvel 7 dias)")

# Ajustando espaçamento do eixo X
ax1.xaxis.set_major_locator(plt.MaxNLocator(12))

# Adicionando legendas
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

# Grid no eixo principal
ax1.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Exibir gráfico
plt.show()
