import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração do estilo dos gráficos
sns.set_theme(style="whitegrid")

# Carregar os dados do arquivo Excel
caminho_arquivo = "data/brutos/dados_IFSP_SJBV.xlsx"
sheets = pd.ExcelFile(caminho_arquivo).sheet_names

def carregar_dados(sheet_name):
    df = pd.read_excel(caminho_arquivo, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()
    df["momento"] = pd.to_datetime(df["momento"], format="%d/%m/%Y %H:%M")
    return df

dataframes = {sheet: carregar_dados(sheet) for sheet in sheets}

def analisar_15_min(df):
    df["Ultrapassagem"] = ((df["momento"].dt.hour >= 18) & (df["momento"].dt.hour < 21) & (df["Potência Ativa Trifásica (kW)"] > 77)) | \
                           ((df["momento"].dt.hour < 18) & (df["Potência Ativa Trifásica (kW)"] > 72))
    
    ultrapassagem_percentual = df["Ultrapassagem"].mean() * 100
    
    return df[["momento", "Potência Ativa Trifásica (kW)", "Ultrapassagem"]], ultrapassagem_percentual

def analisar_diario(df):
    df["Periodo"] = pd.cut(df["momento"].dt.hour, bins=[6, 12, 18, 24], labels=["Matutino", "Vespertino", "Noturno"], right=False, include_lowest=True)
    media_diaria = df.groupby(df["momento"].dt.date)["Potência Ativa Trifásica (kW)"].mean()
    return media_diaria

def analisar_mensal(df):
    df["Mes"] = df["momento"].dt.month
    media_mensal_total = df.groupby("Mes")["Potência Ativa Trifásica (kW)"].mean()
    return media_mensal_total

def analisar_fp_diario(df):
    media_fp_diaria = df.groupby(df["momento"].dt.date)["Fator de Potência Trifásico"].mean()
    dias_abaixo_092 = (media_fp_diaria < 0.92).sum()
    percentual_dias_abaixo = (dias_abaixo_092 / len(media_fp_diaria)) * 100
    return media_fp_diaria, percentual_dias_abaixo

def plotar_graficos(sheet_name, df_ultrapassagem, media_diaria, media_mensal, media_fp):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Gráfico 1: Ultrapassagem da Demanda Contratada
    axes[0, 0].plot(df_ultrapassagem["momento"], df_ultrapassagem["Potência Ativa Trifásica (kW)"], color='blue', label="Potência Ativa")
    axes[0, 0].fill_between(df_ultrapassagem["momento"], df_ultrapassagem["Potência Ativa Trifásica (kW)"], where=df_ultrapassagem["Ultrapassagem"], color='red', alpha=0.3, label="Ultrapassagem")
    axes[0, 0].set_title("Ultrapassagem da Demanda Contratada")
    axes[0, 0].set_ylabel("Potência Ativa (kW)")
    axes[0, 0].legend()

    # Gráfico 2: Média Diária da Potência Ativa
    axes[0, 1].plot(media_diaria.index, media_diaria.values, marker='o', linestyle='-', color='green')
    axes[0, 1].set_title("Média Diária da Potência Ativa")
    axes[0, 1].set_ylabel("Potência Ativa (kW)")
    axes[0, 1].tick_params(axis='x', rotation=45)

    # Gráfico 3: Média Mensal da Potência Ativa
    axes[1, 0].bar(media_mensal.index, media_mensal.values, color='purple')
    axes[1, 0].set_title("Média Mensal da Potência Ativa")
    axes[1, 0].set_xlabel("Mês")
    axes[1, 0].set_ylabel("Potência Ativa (kW)")

    # Gráfico 4: Média Diária do Fator de Potência
    axes[1, 1].plot(media_fp.index, media_fp.values, marker='s', linestyle='-', color='orange')
    axes[1, 1].axhline(0.92, color='red', linestyle="--", label="Limite 0.92")
    axes[1, 1].set_title("Média Diária do Fator de Potência")
    axes[1, 1].set_ylabel("Fator de Potência")
    axes[1, 1].legend()
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.suptitle(f"Análises de {sheet_name}")
    plt.tight_layout()
    plt.show()

# Processar os dados e gerar gráficos para cada aba
for sheet, df in dataframes.items():
    df_ultrapassagem, ultrapassagem = analisar_15_min(df)
    media_diaria = analisar_diario(df)
    media_mensal = analisar_mensal(df)
    media_fp, perc_fp_baixo = analisar_fp_diario(df)
    
    plotar_graficos(sheet, df_ultrapassagem, media_diaria, media_mensal, media_fp)
