import pandas as pd
import matplotlib.pyplot as plt

# Importando os dados processados do outro arquivo
from leitura_excel import df_completo  

# 🔹 Criar figura mais larga
fig, ax1 = plt.subplots(figsize=(20, 6))  # Aumentando a largura do gráfico

# 🔹 Cores e estilos
cores_energia = {"SFCR_1": "blue", "SFCR_2": "red"}  # SFCR_1 é agora a soma dos 1A, 1B, 1C

# 🔹 Plotar geração de energia (média móvel de 7 dias)
for sfcr, cor in cores_energia.items():
    df_filtrado = df_completo[df_completo["SFCR_ID"] == sfcr]
    
    # Agregar por dia
    df_filtrado = df_filtrado.groupby("Data")["E_gerada [kW/h]"].sum().reset_index()

    # Aplicar média móvel
    df_filtrado["E_gerada_MM7"] = df_filtrado["E_gerada [kW/h]"].rolling(window=7, min_periods=1).mean()
    
    ax1.plot(df_filtrado["Data"], df_filtrado["E_gerada_MM7"], label=sfcr, color=cor, linewidth=1)

# 🔹 Criar segundo eixo Y para temperatura ambiente
ax2 = ax1.twinx()

# 🔹 Garantir que a temperatura esteja agregada corretamente por dia
df_temp = df_completo.groupby("Data")["Temp. Ins. (C)"].mean().reset_index()

# 🔹 Aplicar média móvel corretamente
df_temp["Temp_MM7"] = df_temp["Temp. Ins. (C)"].rolling(window=7, min_periods=1).mean()

ax2.plot(df_temp["Data"], df_temp["Temp_MM7"], label="Temperatura Ambiente", color="black", linestyle="--", linewidth=1.5)

# 🔹 Melhorar formatação
ax1.set_xlabel("Data")
ax1.set_ylabel("Geração de Energia [kWh]")
ax2.set_ylabel("Temperatura [°C]")

ax1.set_title("Geração de Energia x Tempo (Média Móvel 7 dias)")

# 🔹 Ajustar formatação do eixo X para exibir todos os meses corretamente
ax1.xaxis.set_major_locator(plt.MaxNLocator(12))  

# 🔹 Ajustando as legendas corretamente
ax1.legend(loc="upper right", bbox_to_anchor=(1, 1))  # 🔹 Legenda da geração no canto superior esquerdo
ax2.legend(loc="upper right", bbox_to_anchor=(0.9, 1))  # 🔹 Legenda da temperatura no canto superior direito

ax1.grid(True, linestyle="--", alpha=0.5)  # Linhas de grade suaves
plt.tight_layout()  # Ajusta automaticamente para não cortar legendas

# 🔹 Exibir gráfico
plt.show()
