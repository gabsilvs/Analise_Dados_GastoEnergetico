import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import todos_resultados

# Definir a demanda contratada (ajuste conforme necessário)
DEMANDA_CONTRATADA = 100  # Exemplo, ajuste conforme os dados reais

sns.set_theme(style="whitegrid")

def plotar_media_mensal(sheet_name, media_mensal):
    plt.figure(figsize=(12, 6))

    meses_labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    indices_convertidos = [meses_labels[m-1] for m in media_mensal.index]

    # Destacar os meses que ultrapassaram a demanda contratada
    cores = ["red" if v > DEMANDA_CONTRATADA else "green" for v in media_mensal.values]

    sns.barplot(x=indices_convertidos, y=media_mensal.values, palette=cores)

    # Linha da demanda contratada
    plt.axhline(DEMANDA_CONTRATADA, color="black", linestyle="--", linewidth=2, label=f"Demanda Contratada: {DEMANDA_CONTRATADA} kW")

    plt.title(f"Média Mensal da Potência Ativa ({sheet_name})", fontsize=14, fontweight="bold")
    plt.xlabel("Mês", fontsize=12)
    plt.ylabel("Potência Ativa (kW)", fontsize=12)

    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

for sheet, dados in todos_resultados.items():
    plotar_media_mensal(sheet, dados["Média_Mensal"])

#Comentários sobre o código:

#O gráfico mensal compara os valores de potência ativa com a demanda contratada, destacando meses que ultrapassaram esse limite.
#Usa-se seaborn para criar um gráfico de barras com coloração diferenciada para meses acima e abaixo do limite.

#grafico_media_mensal.py
#Juntar todos os meses em um gráfico só, 12 colunas (um para cada mês)