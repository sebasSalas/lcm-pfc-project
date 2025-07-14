import matplotlib.pyplot as plt


def generar_graficas(combinaciones, tiempos, memoria_kb, n_valores, k_valores, nombres_escenarios):
    # --- Gráfica 1: Tiempo vs combinaciones ---
    plt.figure(figsize=(10, 6))
    plt.plot(combinaciones, tiempos, marker='o', color='blue')
    plt.title("Tiempo de ejecución vs Cantidad de combinaciones")
    plt.xlabel("Número de combinaciones")
    plt.ylabel("Tiempo (segundos)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficas/tiempo_vs_combinaciones.png")
    plt.close()

    # --- Gráfica 2: Memoria vs combinaciones ---
    plt.figure(figsize=(10, 6))
    plt.plot(combinaciones, memoria_kb, marker='s', color='green')
    plt.title("Consumo de memoria vs Cantidad de combinaciones")
    plt.xlabel("Número de combinaciones")
    plt.ylabel("Memoria (KB)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficas/memoria_vs_combinaciones.png")
    plt.close()

    # --- Gráfica 3: Tiempo por n para distintos k ---
    plt.figure(figsize=(10, 6))
    for k in sorted(set(k_valores)):
        tiempos_k = [t for i, t in enumerate(tiempos) if k_valores[i] == k]
        n_k = [n_valores[i] for i in range(len(n_valores)) if k_valores[i] == k]
        plt.plot(n_k, tiempos_k, marker='o', linestyle='-', label=f'k = {k}')



    plt.title("Tiempo de ejecución según el tamaño de entrada")
    plt.xlabel("n (tamaño del conjunto)")
    plt.ylabel("Tiempo (segundos)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficas/tiempo_por_n_y_k.png")
    plt.close()


# --- Ejemplo de uso ---
if __name__ == "__main__":
    nombres_escenarios = ["Caso Base", "Medio 1", "Medio 2", "Medio 3", "Medio-Alto", "Alto 1", "Alto 2"]
    n_valores = [10, 15, 15, 20, 20, 22, 25]
    k_valores = [5, 5, 7, 5, 10, 11, 12]
    combinaciones = [252, 3003, 6435, 15504, 184756, 705432, 5200300]
    tiempos = [0.01, 0.03, 0.08, 0.15, 1.9, 5.5, 22.3]
    memoria_kb = [23, 52, 108, 240, 390, 720, 1340]

    generar_graficas(combinaciones, tiempos, memoria_kb, n_valores, k_valores, nombres_escenarios)
    print(" Gráficas generadas en la carpeta 'graficas'")
