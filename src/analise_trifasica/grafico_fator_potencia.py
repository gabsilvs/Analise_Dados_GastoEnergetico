import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import todos_resultados

sns.set_theme(style="whitegrid")

def plotar_fp(sheet_name, media_fp):
    plt.figure(figsize=(12, 5))
    plt.plot(media_fp.index, media_fp.values, marker='s', linestyle='-', color='orange')
    plt.axhline(0.92, color='red', linestyle="--", label="Limite 0.92")

    plt.title(f"Média Diária do Fator de Potência ({sheet_name})")
    plt.ylabel("Fator de Potência")
    plt.xlabel("Data")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

for sheet, dados in todos_resultados.items():
    plotar_fp(sheet, dados["Média_FP_Diária"])
