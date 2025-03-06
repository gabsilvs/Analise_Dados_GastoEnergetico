import pandas as pd
import matplotlib.pyplot as plt

from leitura_excel import df_completo

mes_escolhido = 1

df_completo["Data"] = pd.to_datetime(df_completo["Data"])
df_mes = df_completo[df_completo["Data"].dt.month == mes_escolhido]

df_mes["SFCR_ID"] = df_mes["SFCR_ID"].replace({"SFCR_1A": "SFCR_1", "SFCR_1B": "SFCR_1", "SFCR_1C": "SFCR_1"})
df_mes = df_mes.groupby(["Data", "SFCR_ID"], as_index=False).sum()

cores = {"SFCR_1": "blue", "SFCR_2": "red"}

plt.figure(figsize=(12, 5))

for sfcr, cor in cores.items():
    df_filtrado = df_mes[df_mes["SFCR_ID"] == sfcr]
    plt.plot(df_filtrado["Data"], df_filtrado["E_gerada [kW/h]"], label=sfcr, color=cor, linewidth=1)

plt.xlabel("Data")
plt.ylabel("Energia Gerada (kWh)")
plt.title(f"Geração de Energia - Mês {mes_escolhido:02d}")
plt.xticks(rotation=45)
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

plt.show()