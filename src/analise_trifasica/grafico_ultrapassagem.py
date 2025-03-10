import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import todos_resultados

sns.set_theme(style="whitegrid")

def plotar_ultrapassagem(sheet_name, df_ultrapassagem, demanda_contratada):
    plt.figure(figsize=(12, 5))

    # Média diária da demanda consumida
    media_diaria = df_ultrapassagem.groupby(df_ultrapassagem["momento"].dt.date)["Potência Ativa Trifásica (kW)"].mean()

    plt.plot(media_diaria.index, media_diaria.values, marker='o', linestyle='-', color='blue', label="Consumo diário")
    plt.axhline(demanda_contratada, color='red', linestyle='--', label="Demanda Contratada")

    plt.title(f"Ultrapassagens de Potência Ativa ({sheet_name})")
    plt.ylabel("Potência Ativa (kW)")
    plt.xlabel("Data")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

for sheet, dados in todos_resultados.items():
    plotar_ultrapassagem(sheet, dados["Ultrapassagem"], 100)

#Comentários sobre o código:

#O gráfico de ultrapassagem mostra o consumo diário de potência ativa e destaca as ultrapassagens de demanda contratada.