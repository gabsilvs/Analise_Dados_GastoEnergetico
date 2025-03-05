import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import todos_resultados

sns.set_theme(style="whitegrid")

def plotar_media_mensal(sheet_name, media_mensal):
    plt.figure(figsize=(10, 5))
    plt.bar(media_mensal.index, media_mensal.values, color='purple')

    plt.title(f"Média Mensal da Potência Ativa ({sheet_name})")
    plt.xlabel("Mês")
    plt.ylabel("Potência Ativa (kW)")
    plt.tight_layout()
    plt.show()

for sheet, dados in todos_resultados.items():
    plotar_media_mensal(sheet, dados["Média_Mensal"])
