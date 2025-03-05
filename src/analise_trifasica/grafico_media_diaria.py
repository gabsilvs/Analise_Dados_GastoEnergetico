import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import todos_resultados

sns.set_theme(style="whitegrid")

def plotar_media_diaria(sheet_name, media_diaria):
    plt.figure(figsize=(12, 5))
    plt.plot(media_diaria.index, media_diaria.values, marker='o', linestyle='-', color='green')

    plt.title(f"Média Diária da Potência Ativa ({sheet_name})")
    plt.ylabel("Potência Ativa (kW)")
    plt.xlabel("Data")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

for sheet, dados in todos_resultados.items():
    plotar_media_diaria(sheet, dados["Média_Diária"])
