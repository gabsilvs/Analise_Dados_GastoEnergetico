import pandas as pd
import os

# Carregar os dados do arquivo Excel
caminho_arquivo = "data/brutos/dados_IFSP_SJBV.xlsx"
sheets = pd.ExcelFile(caminho_arquivo).sheet_names

def carregar_dados(sheet_name):
    df = pd.read_excel(caminho_arquivo, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()  # Removendo espaços extras nas colunas
    df["momento"] = pd.to_datetime(df["momento"], format="%d/%m/%Y %H:%M")  # Convertendo para datetime
    return df

dataframes = {sheet: carregar_dados(sheet) for sheet in sheets}

def calcular_porcentagem_ultrapassagem(df):
    """
    Calcula a porcentagem de ultrapassagem de demanda diária separada por horários.
    """
    resultados = []
    
    for data, grupo in df.groupby(df["momento"].dt.date):
        # Separar os períodos
        periodo_pico = grupo[(grupo["momento"].dt.hour >= 18) & (grupo["momento"].dt.hour < 21)]
        periodo_fora_pico = grupo[~((grupo["momento"].dt.hour >= 18) & (grupo["momento"].dt.hour < 21))]

        # Cálculo de ultrapassagem
        if not periodo_pico.empty:
            ultrapassagem_77 = (periodo_pico["Potência Ativa Trifásica (kW)"] > 77).mean() * 100
        else:
            ultrapassagem_77 = 0

        if not periodo_fora_pico.empty:
            ultrapassagem_72 = (periodo_fora_pico["Potência Ativa Trifásica (kW)"] > 72).mean() * 100
        else:
            ultrapassagem_72 = 0

        resultados.append([data, ultrapassagem_77, ultrapassagem_72])
    
    return pd.DataFrame(resultados, columns=["Dia", "Ultrapassagem 77kW (%)", "Ultrapassagem 72kW (%)"])

def calcular_porcentagem_fp(df):
    """
    Calcula a porcentagem de medições do fator de potência abaixo de 0.92 por dia.
    """
    resultados = []

    for data, grupo in df.groupby(df["momento"].dt.date):
        total_medicoes = len(grupo)
        abaixo_092 = (grupo["Fator de Potência Trifásico"] < 0.92).sum()

        if total_medicoes > 0:
            percentual_abaixo_092 = (abaixo_092 / total_medicoes) * 100
        else:
            percentual_abaixo_092 = 0

        resultados.append([data, percentual_abaixo_092])
    
    return pd.DataFrame(resultados, columns=["Dia", "Fator de Potência < 0.92 (%)"])

# Processar os dados e armazenar em um dicionário separado por mês
resultados_por_mes = {}

for sheet, df in dataframes.items():
    df["Mês"] = df["momento"].dt.strftime("%Y-%m")  # Criando coluna de mês no formato "YYYY-MM"

    for mes, grupo in df.groupby("Mês"):
        ultrapassagem_df = calcular_porcentagem_ultrapassagem(grupo)
        fp_df = calcular_porcentagem_fp(grupo)

        # Unir os dois dataframes pelos dias
        resultado_final = pd.merge(ultrapassagem_df, fp_df, on="Dia", how="outer")

        if mes not in resultados_por_mes:
            resultados_por_mes[mes] = resultado_final
        else:
            resultados_por_mes[mes] = pd.concat([resultados_por_mes[mes], resultado_final])

# Criar e salvar o Excel com abas para cada mês
caminho_saida = "D:/DocumentosD/TCC_Caio/data/saidas/analise_trifasica.xlsx"
with pd.ExcelWriter(caminho_saida) as writer:
    for mes, df in resultados_por_mes.items():
        df.to_excel(writer, sheet_name=mes, index=False)

print(f"Arquivo Excel gerado em: {caminho_saida}")
