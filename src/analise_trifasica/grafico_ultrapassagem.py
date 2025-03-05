import matplotlib.pyplot as plt
import seaborn as sns
from analise_dados import todos_resultados

sns.set_theme(style="whitegrid")

def plotar_ultrapassagem(sheet_name, df_ultrapassagem):
    plt.figure(figsize=(12, 5))
    plt.plot(df_ultrapassagem["momento"], df_ultrapassagem["Potência Ativa Trifásica (kW)"], color='blue', label="Potência Ativa")
    plt.fill_between(df_ultrapassagem["momento"], df_ultrapassagem["Potência Ativa Trifásica (kW)"], color='red', alpha=0.3, label="Ultrapassagem")
    
    plt.title(f"Ultrapassagem da Demanda Contratada ({sheet_name})")
    plt.ylabel("Potência Ativa (kW)")
    plt.xlabel("Momento")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

for sheet, dados in todos_resultados.items():
    plotar_ultrapassagem(sheet, dados["Ultrapassagem"])
