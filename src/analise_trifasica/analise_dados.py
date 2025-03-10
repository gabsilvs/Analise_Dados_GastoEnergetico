# Importando o pandas para manipulação de dados
import pandas as pd

# Carregar os dados do arquivo Excel
caminho_arquivo = "data/brutos/dados_IFSP_SJBV.xlsx"
sheets = pd.ExcelFile(caminho_arquivo).sheet_names  # Obtendo os nomes das abas (sheets) no Excel

# Função para carregar os dados de cada aba
def carregar_dados(sheet_name):
    df = pd.read_excel(caminho_arquivo, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()  # Removendo espaços em branco extras nos nomes das colunas
    df["momento"] = pd.to_datetime(df["momento"], format="%d/%m/%Y %H:%M")  # Convertendo a coluna 'momento' para datetime
    return df

# Carregando os dados de todas as abas no Excel
dataframes = {sheet: carregar_dados(sheet) for sheet in sheets}

# Função para analisar os dados a cada 15 minutos
def analisar_15_min(df):
    # Definindo as condições para identificar ultrapassagens com base na hora e potência
    df["Ultrapassagem"] = ((df["momento"].dt.hour >= 18) & (df["momento"].dt.hour < 21) & (df["Potência Ativa Trifásica (kW)"] > 77)) | \
                           ((df["momento"].dt.hour < 18) & (df["Potência Ativa Trifásica (kW)"] > 72))
    
    # Calculando a porcentagem de ultrapassagem
    ultrapassagem_percentual = df["Ultrapassagem"].mean() * 100
    
    # Criando um dataframe resumido apenas com as ultrapassagens
    df_resumido = df[df["Ultrapassagem"]].copy()
    df_resumido = df_resumido[["momento", "Potência Ativa Trifásica (kW)"]]
    
    return df_resumido, ultrapassagem_percentual

# Função para calcular a média diária da potência ativa
def analisar_diario(df):
    media_diaria = df.groupby(df["momento"].dt.date)["Potência Ativa Trifásica (kW)"].mean()
    return media_diaria

# Função para calcular a média mensal da potência ativa
def analisar_mensal(df):
    df["Mes"] = df["momento"].dt.month  # Adicionando a coluna "Mes"
    media_mensal_total = df.groupby("Mes")["Potência Ativa Trifásica (kW)"].mean()
    return media_mensal_total

# Função para calcular a média diária do fator de potência
def analisar_fp_diario(df):
    media_fp_diaria = df.groupby(df["momento"].dt.date)["Fator de Potência Trifásico"].mean()
    return media_fp_diaria

# Processando os dados para gerar os resultados
todos_resultados = {}
for sheet, df in dataframes.items():
    df_ultrapassagem, ultrapassagem = analisar_15_min(df)
    media_diaria = analisar_diario(df)
    media_mensal = analisar_mensal(df)
    media_fp = analisar_fp_diario(df)
    
    # Armazenando os resultados para cada sheet
    todos_resultados[sheet] = {
        "Ultrapassagem": df_ultrapassagem,
        "Média_Diária": media_diaria,
        "Média_Mensal": media_mensal,
        "Média_FP_Diária": media_fp
    }

#Comentários sobre o código:

#O código faz a leitura de um arquivo Excel e carrega todos os dados das planilhas para análise.
#As funções analisar_15_min, analisar_diario, analisar_mensal, e analisar_fp_diario processam os dados e geram resumos que serão utilizados para gerar gráficos posteriormente.
#A função analisar_15_min marca ultrapassagens de potência ativa de acordo com a hora do dia e a potência contratada, e a função retorna um resumo dessas ultrapassagens.
#As funções de análise diária e mensal calculam médias das variáveis para facilitar o acompanhamento.