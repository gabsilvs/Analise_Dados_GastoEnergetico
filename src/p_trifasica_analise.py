import pandas as pd

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
    
    # Criar um dataframe apenas com os dados de 15 em 15 minutos
    df_ultrapassagem = df[["momento", "Potência Ativa Trifásica (kW)", "Ultrapassagem"]]
    
    return df_ultrapassagem, ultrapassagem_percentual

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

def exibir_resultados(sheet_name, df_ultrapassagem, ultrapassagem, media_diaria, media_mensal, media_fp, perc_fp_baixo):
    print(f"\n{'='*40}")
    print(f" Análise de {sheet_name} ")
    print(f"{'='*40}")
    print(f"Ultrapassagem da demanda contratada: {ultrapassagem:.2f}%")
    print(f"\nDetalhes da ultrapassagem (de 15 em 15 min):")
    print(df_ultrapassagem.to_string(index=False))
    print(f"\nMédia de potência diária:")
    print(media_diaria.to_string())
    print(f"\nMédia de potência mensal:")
    print(media_mensal.to_string())
    print(f"\nMédia do fator de potência diário:")
    print(media_fp.to_string())
    print(f"\nPercentual de dias com FP abaixo de 0.92: {perc_fp_baixo:.2f}%")
    print(f"{'='*40}\n")

todos_resultados = {}

for sheet, df in dataframes.items():
    df_ultrapassagem, ultrapassagem = analisar_15_min(df)
    media_diaria = analisar_diario(df)
    media_mensal = analisar_mensal(df)
    media_fp, perc_fp_baixo = analisar_fp_diario(df)
    
    todos_resultados[sheet] = {
        "Ultrapassagem": df_ultrapassagem,
        "Média_Diária": media_diaria,
        "Média_Mensal": media_mensal,
        "Média_FP_Diária": media_fp,
        "Percentual_FP_Abaixo": perc_fp_baixo
    }
    
    exibir_resultados(sheet, df_ultrapassagem, ultrapassagem, media_diaria, media_mensal, media_fp, perc_fp_baixo)
