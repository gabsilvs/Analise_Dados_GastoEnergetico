import matplotlib.pyplot as plt
import seaborn as sns
from leitura_excel import dados_geracao,dados_meteorologicos,df_completo,df_meteorologicos_diario,df_geracao_completo
# Configurar o estilo do gráfico
sns.set(style="whitegrid")

# Configurar o estilo do gráfico
sns.set(style="whitegrid")

# Criar a figura e o eixo principal
fig, ax1 = plt.subplots(figsize=(12, 6))

# Definir cores suaves para os sistemas fotovoltaicos
cores = {
    "SFCR_1A": "#1f77b4",  # Azul
    "SFCR_1B": "#ff7f0e",  # Laranja
    "SFCR_1C": "#2ca02c",  # Verde
    "SFCR_2": "#d62728"    # Vermelho
}

# Plotar a geração de energia para cada SFCR com suavização (média móvel de 7 dias)
for sfcr in df_completo["SFCR_ID"].unique():
    df_filtrado = df_completo[df_completo["SFCR_ID"] == sfcr].copy()
    
    # Aplicar uma média móvel de 7 dias para suavizar
    df_filtrado["E_gerada [kW/h]"] = df_filtrado["E_gerada [kW/h]"].rolling(window=7, min_periods=1).mean()
    
    ax1.plot(df_filtrado["Data"], df_filtrado["E_gerada [kW/h]"], 
             label=f"{sfcr}", color=cores.get(sfcr, "gray"), linewidth=2)

# Configurar rótulos e legendas
ax1.set_xlabel("Data")
ax1.set_ylabel("Geração de Energia [kWh]")
ax1.set_title("Geração de Energia x Tempo (Média Móvel 7 dias)")
ax1.legend(title="Sistema Fotovoltaico", loc="upper left")

# Criar o segundo eixo Y para a temperatura
ax2 = ax1.twinx()
ax2.plot(df_meteorologicos_diario["Data"], 
         df_meteorologicos_diario["Temp. Ins. (C)"].rolling(window=7, min_periods=1).mean(), 
         color='black', linestyle='--', linewidth=2, label="Temperatura Ambiente")

# Configurar o eixo de temperatura
ax2.set_ylabel("Temperatura [°C]")
ax2.legend(loc="upper right")

# Ajustar espaçamento dos rótulos do eixo X para não sobrepor
plt.xticks(rotation=30)

# Melhorar espaçamento do gráfico
plt.tight_layout()

# Mostrar o gráfico
plt.show()
