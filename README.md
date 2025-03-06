# Análise de Geração de Energia e Precipitação

Este projeto tem como objetivo analisar dados de geração de energia e precipitação, utilizando técnicas de processamento de dados e visualização para extrair informações relevantes. A ferramenta permite a leitura de arquivos Excel contendo dados brutos, o processamento desses dados e a geração de gráficos informativos.

## Estrutura do Projeto

📂 src/
 ├── grafico_chuva.py  # Gera gráficos de precipitação
 ├── grafico_diario_mes.py  # Gera gráficos de média diária e mensal
 ├── graficos_mensal.py  # Processa e plota médias mensais
 ├── graficos_rad.py  # Análise de radiação solar
 ├── graficos_trifasica_analise.py  # Análise de potência ativa trifásica
 ├── leitura_excel.py  # Responsável pela leitura e tratamento dos dados
 ├── p_trifasica_analise.py  # Processamento avançado de potência trifásica

## Como Instalar e Executar

1. **Clonar o repositório**

   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio/src
   ```

2. **Criar um ambiente virtual e instalar dependências**

   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Executar a análise e geração de gráficos**

   ```sh
   python graficos_trifasica_analise.py
   ```

   Outros módulos podem ser executados individualmente para gerar gráficos específicos.

## Como Funciona

- Os dados são extraídos de um arquivo Excel (".xlsx") localizado em `data/brutos/dados_IFSP_SJBV.xlsx`.
- Cada script processa um conjunto de informações específico:
  - **gráficos_trifasica_analise.py**: Analisa a potência ativa trifásica e fator de potência, gerando gráficos detalhados.
  - **grafico_diario_mes.py**: Calcula médias diárias e mensais de consumo energético.
  - **graficos_rad.py**: Avalia a radiação solar e sua variação ao longo do tempo.
  - **grafico_chuva.py**: Gera visualização sobre a distribuição da precipitação.

## Requisitos

- Python 3.8+
- Bibliotecas: `pandas`, `matplotlib`, `seaborn`, `openpyxl`
