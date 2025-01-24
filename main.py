import os
from src.analise_dados import analisar_potencia_ativa, analisar_fator_potencia

# Caminhos dos arquivos
PROCESSADOS_PATH = "./data/processados"
SAIDAS_PATH = "./data/saidas"

def main():
    PROCESSADOS_PATH = "./data/processados"
    SAIDAS_PATH = "./data/saidas"

    dados_consolidados_path = os.path.join(PROCESSADOS_PATH, "dados_consolidados.csv")

    analisar_potencia_ativa(dados_consolidados_path, SAIDAS_PATH)
    analisar_fator_potencia(dados_consolidados_path, SAIDAS_PATH)

    print("Análises concluídas! Resultados salvos na pasta './data/saidas/'.")

if __name__ == "__main__":
    main()


