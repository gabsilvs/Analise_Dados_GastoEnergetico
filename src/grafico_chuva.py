import pandas as pd
import matplotlib.pyplot as plt

# Importando os dados processados
from leitura_excel import df_completo  

# 🔹 Criar figura mais larga
fig, ax1 = plt.subplots(figsize=(20, 6))  # Mantendo o formato wide

# 🔹 Cores e estilos
cores_energia = {"SFCR_1A": "blue", "SFCR_1B": "green", "SFCR_1C": "orange", "SFCR_2": "red"}

# 🔹 Plotar geração de energia (média móvel de 7 dias)
for sfcr, cor in cores_energia.items():
    df_filtrado = df_completo[df_completo["SFCR_ID"] == sfcr]
    
    # Agregar por dia
    df_filtrado = df_filtrado.groupby("Data")["E_gerada [kW/h]"].sum().reset_index()

    # Aplicar média móvel
    df_filtrado["E_gerada_MM7"] = df_filtrado["E_gerada [kW/h]"].rolling(window=7, min_periods=1).mean()
    
    ax1.plot(df_filtrado["Data"], df_filtrado["E_gerada_MM7"], label=sfcr, color=cor, linewidth=1)

# 🔹 Criar segundo eixo Y para precipitação (mm de chuva)
ax2 = ax1.twinx()

# 🔹 Garantir que a precipitação esteja agregada corretamente por dia
df_chuva = df_completo.groupby("Data")["Chuva (mm)"].sum().reset_index()

# 🔹 Aplicar média móvel corretamente
df_chuva["Chuva_MM7"] = df_chuva["Chuva (mm)"].rolling(window=7, min_periods=1).mean()

ax2.plot(df_chuva["Data"], df_chuva["Chuva_MM7"], label="Chuva (mm)", color="black", linestyle="--", linewidth=1.5)

# 🔹 Melhorar formatação
ax1.set_xlabel("Data")
ax1.set_ylabel("Geração de Energia [kWh]")
ax2.set_ylabel("Precipitação [mm]")

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
