import pandas as pd
import matplotlib.pyplot as plt

from leitura_dados.leitura_excel import df_completo

fig, ax1 = plt.subplots(figsize=(20, 6))

cores_energia = {"SFCR_1": "blue", "SFCR_2": "red"}

for sfcr, cor in cores_energia.items():
    df_filtrado = df_completo[df_completo["SFCR_ID"] == sfcr]
    df_filtrado = df_filtrado.groupby("Data")["E_gerada [kW/h]"].sum().reset_index()
    df_filtrado["E_gerada_MM7"] = df_filtrado["E_gerada [kW/h]"].rolling(window=7, min_periods=1).mean()
    ax1.plot(df_filtrado["Data"], df_filtrado["E_gerada_MM7"], label=sfcr, color=cor, linewidth=1)

ax2 = ax1.twinx()

df_temp = df_completo.groupby("Data")["Temp. Ins. (C)"].mean().reset_index()
df_temp["Temp_MM7"] = df_temp["Temp. Ins. (C)"].rolling(window=7, min_periods=1).mean()

ax2.plot(df_temp["Data"], df_temp["Temp_MM7"], label="Temperatura Ambiente", color="black", linestyle="--", linewidth=1.5)

ax1.set_xlabel("Data")
ax1.set_ylabel("Geração de Energia [kWh]")
ax2.set_ylabel("Temperatura [°C]")

ax1.set_title("Geração de Energia x Tempo (Média Móvel 7 dias)")

ax1.xaxis.set_major_locator(plt.MaxNLocator(12))

ax1.legend(loc="upper right", bbox_to_anchor=(1, 1))
ax2.legend(loc="upper right", bbox_to_anchor=(0.9, 1))

ax1.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

plt.show()