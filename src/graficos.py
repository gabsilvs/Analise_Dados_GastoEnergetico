import matplotlib.pyplot as plt

def gerar_graficos(merged_data):
    # Gráfico de ultrapassagem por horário
    ultrapassagem_por_horario = merged_data.groupby('Hora')['Ultrapassagem'].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(ultrapassagem_por_horario.index, ultrapassagem_por_horario.values, marker='o')
    plt.title("Frequência de ultrapassagem por hora")
    plt.xlabel("Hora")
    plt.ylabel("Frequência de ultrapassagem (%)")
    plt.grid()
    plt.savefig('./outputs/graficos/ultrapassagem_por_horario.png')
    plt.show()

    print("Gráficos salvos em 'outputs/graficos/'.")
