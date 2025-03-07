#Working
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
    
    # Resumir os dados para facilitar a visualização
    df_resumido = df[df["Ultrapassagem"]].copy()
    df_resumido = df_resumido[["momento", "Potência Ativa Trifásica (kW)"]]
    
    return df_resumido, ultrapassagem_percentual

def analisar_diario(df):
    media_diaria = df.groupby(df["momento"].dt.date)["Potência Ativa Trifásica (kW)"].mean()
    return media_diaria

def analisar_mensal(df):
    df["Mes"] = df["momento"].dt.month
    media_mensal_total = df.groupby("Mes")["Potência Ativa Trifásica (kW)"].mean()
    return media_mensal_total

def analisar_fp_diario(df):
    media_fp_diaria = df.groupby(df["momento"].dt.date)["Fator de Potência Trifásico"].mean()
    return media_fp_diaria

# Processar os dados para uso nos gráficos
todos_resultados = {}
for sheet, df in dataframes.items():
    df_ultrapassagem, ultrapassagem = analisar_15_min(df)
    media_diaria = analisar_diario(df)
    media_mensal = analisar_mensal(df)
    media_fp = analisar_fp_diario(df)
    
    todos_resultados[sheet] = {
        "Ultrapassagem": df_ultrapassagem,
        "Média_Diária": media_diaria,
        "Média_Mensal": media_mensal,
        "Média_FP_Diária": media_fp
    }
