#Test
import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import todos_resultados

# Configurar tema do Seaborn
sns.set_theme(style="whitegrid")

def plotar_media_mensal(sheet_name, media_mensal):
    plt.figure(figsize=(12, 6))

    # Converter índices numéricos para nomes dos meses
    meses_labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    indices_convertidos = [meses_labels[m-1] for m in media_mensal.index]

    # Definir limite de ultrapassagem como o maior valor registrado
    limite_ultrapassagem = media_mensal.max()

    # Criar gráfico de barras
    sns.barplot(x=indices_convertidos, y=media_mensal.values, palette="magma")

    # Adicionar linha de limite de ultrapassagem
    plt.axhline(limite_ultrapassagem, color="red", linestyle="--", linewidth=2, label=f"Limite: {limite_ultrapassagem:.2f} kW")

    # Definir o limite fixo no eixo Y
    plt.ylim(0, 50)

    # Ajustes visuais
    plt.title(f"Média Mensal da Potência Ativa ({sheet_name})", fontsize=14, fontweight="bold")
    plt.xlabel("Mês", fontsize=12)
    plt.ylabel("Potência Ativa (kW)", fontsize=12)

    plt.xticks(rotation=45)  # Rotaciona os nomes dos meses para melhor legibilidade
    plt.legend()  # Exibir legenda da linha de ultrapassagem
    plt.grid(axis="y", linestyle="--", alpha=0.7)  # Linhas de grade apenas no eixo Y
    plt.tight_layout()

    # Exibir gráfico
    plt.show()

# Gerar gráficos para todas as planilhas
for sheet, dados in todos_resultados.items():
    plotar_media_mensal(sheet, dados["Média_Mensal"])
