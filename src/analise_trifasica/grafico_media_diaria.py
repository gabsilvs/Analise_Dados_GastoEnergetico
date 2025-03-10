import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import todos_resultados

# Definir a demanda contratada (ajuste conforme necessário)
DEMANDA_CONTRATADA = 100  # Exemplo, ajuste conforme os dados reais

sns.set_theme(style="whitegrid")

def plotar_media_diaria(sheet_name, media_diaria):
    plt.figure(figsize=(12, 5))
    
    # Destacando os dias que ultrapassaram a demanda contratada
    acima_limite = media_diaria[media_diaria > DEMANDA_CONTRATADA]

    plt.plot(media_diaria.index, media_diaria.values, marker='o', linestyle='-', color='green', label="Média Diária")
    plt.scatter(acima_limite.index, acima_limite.values, color='red', label="Ultrapassagem", zorder=3)
    
    # Adicionando linha de referência para a demanda contratada
    plt.axhline(y=DEMANDA_CONTRATADA, color='red', linestyle='--', label="Demanda Contratada")

    plt.title(f"Média Diária da Potência Ativa ({sheet_name})")
    plt.ylabel("Potência Ativa (kW)")
    plt.xlabel("Data")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

for sheet, dados in todos_resultados.items():
    plotar_media_diaria(sheet, dados["Média_Diária"])

#Comentários sobre o código:

#O gráfico mostra a média diária de potência ativa, destacando os dias que ultrapassaram a demanda contratada.
#Um limite visual é adicionado para ajudar na identificação das ultrapassagens.

#grafico_media_diario.py

#Gerar um grafico igual ao de grafico_fator_potencia.py, mas inves de utilizar a coluna E, utilizar a coluna B, e o limite será 77kw 