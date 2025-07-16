import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb
import os

# Crear la carpeta 'images' si no existe
os.makedirs('images', exist_ok=True)

# --- Gráfica 1: Complejidad temporal teórica O(n^k * k * log(L)) ---
n_values = np.arange(2, 21, 1)  # Cambiado de 5 a 2
k = 5
L = 10**6  # Valor arbitrario para L
complexity = [n**k * k * np.log2(L) for n in n_values]

plt.figure(figsize=(8,5))
plt.plot(complexity, n_values, marker='o')
plt.xscale('log')
plt.title('Crecimiento de la Complejidad Temporal O(n^k * k * log(L))')
plt.ylabel('n (tamaño del conjunto)')
plt.xlabel('Operaciones estimadas (escala log)')
plt.grid(True)
plt.tight_layout()
plt.savefig('images/complejidad_temporal_ejes_invertidos.png')
plt.show()

# --- Gráfica 2: Comparación de complejidad espacial ---
espacial_generador = [k for n in n_values]
espacial_lista = [comb(n, k, exact=True) * k for n in n_values]

plt.figure(figsize=(8,5))
plt.plot(espacial_generador, n_values, label='Con generador (O(k))')
plt.plot(espacial_lista, n_values, label='Sin generador (O(C(n,k)*k))')
plt.xscale('log')
plt.title('Comparación de Complejidad Espacial')
plt.ylabel('n (tamaño del conjunto)')
plt.xlabel('Memoria estimada (elementos)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('images/complejidad_espacial_ejes_invertidos.png')
plt.show()

# --- Gráfica 3: Tiempos reales de ejecución ---
escenarios = ["Caso Base", "Medio 1", "Medio 2", "Medio 3", "Medio-Alto", "Alto 1", "Alto 2"]
tiempos = [0.1523, 0.1486, 0.4897, 0.7411, 14.0720, 60.2780, 180.0]  # segundos, datos reales del benchmark

plt.figure(figsize=(10,5))
plt.plot(tiempos, escenarios, marker='o')
plt.xscale('log')
plt.title('Tiempos de Ejecución Reales por Escenario')
plt.ylabel('Escenario')
plt.xlabel('Tiempo (segundos, escala log)')
plt.grid(True)
plt.tight_layout()
plt.savefig('images/tiempos_reales_ejes_invertidos.png')
plt.show() 