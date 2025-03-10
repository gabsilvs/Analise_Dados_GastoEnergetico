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

def analisar_15_min(df):
    # Verificando as ultrapassagens baseadas na hora e potência
    df["Ultrapassagem"] = ((df["momento"].dt.hour >= 18) & (df["momento"].dt.hour < 21) & (df["Potência Ativa Trifásica (kW)"] > 77)) | \
                           ((df["momento"].dt.hour < 18) & (df["Potência Ativa Trifásica (kW)"] > 72))
    
    ultrapassagem_percentual = df["Ultrapassagem"].mean() * 100
    
    # Gerando o dataframe de ultrapassagens a cada 15 minutos
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
    dias_abaixo_092 = (media_fp_diaria < 0.92).sum()  # Contagem dos dias abaixo de 0.92 no fator de potência
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

df_ultrapassagem.to_excel(f"D:/DocumentosD/TCC_Caio/data/saidas/excel.xlsx", index=False)

print(f"Arquivos gerados: ultrapassagem_{caminho_arquivo}.csv e ultrapassagem_{caminho_arquivo}.xlsx")

#Comentários sobre o código:

#A análise de dados foi expandida para incluir o percentual de dias com o fator de potência abaixo de 0.92.
#O código agora também imprime os resultados detalhados para cada aba do Excel com as análises feitas.
#O arquivo de saída foi gerado em formato Excel após o processamento dos dados.

#excel_datagenerate.py
#Fator de Potência
#A porcentagem deve ser mostrada por dia, a % diaria, e não a média mensal no final, por dia é pra ser 96 linhas(pontos), e deve ser mostrar quantos % ficou abaixo. Em cada mes deve ser ter o numero de % equivalentes ao tanto de dias no mês, calculando quantos dias do mês ultrapassou a porcentagem. Coluna E
#Adicione esta porcentagem no excel também, dividindo cada aba 1 mês

#A demanda contratada varia de acordo com o horário, gerar um excel com as colunas dia,ultrapassagem de demanda 77kw, ultrapassagem de demnanda 72kw, o horário das 18h as 21h a demanda é 77kw, e os demais horarios 00h as 18h e 21h as 00h é 72kw
# 100% é o que a demanda é 77kw, e outro 100% é 72kw
# Coluna B


