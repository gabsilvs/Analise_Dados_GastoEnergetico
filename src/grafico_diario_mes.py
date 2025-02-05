import pandas as pd
import matplotlib.pyplot as plt

# Importando os dados do outro arquivo
from leitura_excel import df_completo  # Certifique-se de que o script de leitura foi rodado antes

# 🔹 Definir o mês desejado (exemplo: Janeiro = 1, Fevereiro = 2, ..., Dezembro = 12)
mes_escolhido = 1  # Altere esse número para o mês que deseja visualizar

# 🔹 Filtrar os dados para o mês escolhido
df_completo["Data"] = pd.to_datetime(df_completo["Data"])  # Garantir que Data está no formato correto
df_mes = df_completo[df_completo["Data"].dt.month == mes_escolhido]

# 🔹 Definir cores para cada célula fotovoltaica
cores = {"SFCR_1A": "blue", "SFCR_1B": "green", "SFCR_1C": "purple", "SFCR_2": "red"}

# 🔹 Criar o gráfico
plt.figure(figsize=(12, 5))  # Menor que o anual, mas ainda confortável

for sfcr, cor in cores.items():
    df_filtrado = df_mes[df_mes["SFCR_ID"] == sfcr]
    plt.plot(df_filtrado["Data"], df_filtrado["E_gerada [kW/h]"], label=sfcr, color=cor, linewidth=1)

# 🔹 Melhorando a formatação
plt.xlabel("Data")
plt.ylabel("Energia Gerada (kWh)")
plt.title(f"Geração de Energia - Mês {mes_escolhido:02d}")
plt.xticks(rotation=45)  # Rotaciona datas para melhor leitura
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # Legenda fora do gráfico
plt.grid(True, linestyle="--", alpha=0.5)  # Linhas de grade mais suaves
plt.tight_layout()  # Ajusta para não cortar rótulos

# 🔹 Exibir o gráfico
plt.show()
