import os
import pandas as pd
from math import ceil

def analisar_potencia_ativa(input_path, output_path):
    # Leitura dos dados consolidados
    dados = pd.read_csv(input_path)

    # Conversão de data e hora para facilitar as análises
    dados['Hora (UTC)'] = pd.to_datetime(dados['Hora (UTC)'], format='%H:%M:%S', errors='coerce')
    dados['Periodo'] = pd.cut(
        dados['Hora (UTC)'].dt.hour,
        bins=[0, 6, 12, 18, 24],
        labels=['Madrugada', 'Matutino', 'Vespertino', 'Noturno'],
        right=False
    )

    # Identificar ultrapassagem de demanda
    def verificar_ultrapassagem(row):
        if 18 <= row['Hora (UTC)'].hour < 21:
            return row['Potência Ativa Trifásica (kW)'] > 77
        return row['Potência Ativa Trifásica (kW)'] > 72

    dados['Ultrapassagem'] = dados.apply(verificar_ultrapassagem, axis=1)

    # Calcular porcentagem de ultrapassagem
    porcentagem_ultrapassagem = (
        dados['Ultrapassagem'].sum() / len(dados) * 100
    )

    # Identificar picos de consumo
    dados['Delta Consumo'] = dados['Potência Ativa Trifásica (kW)'].diff().abs()
    dados['Pico'] = dados['Delta Consumo'] > dados['Delta Consumo'].quantile(0.95)

    # Salvar análise de Potência Ativa dividindo em várias abas se necessário
    os.makedirs(output_path, exist_ok=True)
    potencia_saida_path = os.path.join(output_path, "Analise_Potencia_Ativa.xlsx")

    max_rows = 1_000_000
    num_sheets = ceil(len(dados) / max_rows)

    with pd.ExcelWriter(potencia_saida_path, engine="openpyxl") as writer:
        for i in range(num_sheets):
            start_row = i * max_rows
            end_row = (i + 1) * max_rows
            dados.iloc[start_row:end_row].to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)

    print(f"Análise de Potência Ativa salva em: {potencia_saida_path}")

def analisar_fator_potencia(input_path, output_path):
    # Leitura dos dados consolidados
    dados = pd.read_csv(input_path)

    # Análise diária: Média do fator de potência e dias abaixo de 0.92
    dados['Fator de Potência Médio'] = dados.filter(like='Fator de Potência').mean(axis=1)
    dados['Abaixo de 0.92'] = dados['Fator de Potência Médio'] < 0.92

    # Porcentagem de dias abaixo de 0.92
    porcentagem_abaixo = (
        dados['Abaixo de 0.92'].sum() / len(dados) * 100
    )

    # Identificar incidência por período
    fator_potencia_por_periodo = dados.groupby('Periodo')['Fator de Potência Médio'].mean()

    # Salvar análise de Fator de Potência dividindo em várias abas se necessário
    fator_saida_path = os.path.join(output_path, "Analise_Fator_Potencia.xlsx")

    max_rows = 1_000_000
    num_sheets = ceil(len(fator_potencia_por_periodo) / max_rows)

    with pd.ExcelWriter(fator_saida_path, engine="openpyxl") as writer:
        for i in range(num_sheets):
            start_row = i * max_rows
            end_row = (i + 1) * max_rows
            fator_potencia_por_periodo.iloc[start_row:end_row].to_excel(writer, sheet_name=f"Sheet{i+1}")

    print(f"Análise de Fator de Potência salva em: {fator_saida_path}")