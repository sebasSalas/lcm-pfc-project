import math
import time
import random
import tracemalloc
import multiprocessing
import queue

# --- Funciones de Lógica del Problema ---

def get_combinations(s, k):
    if k == 0:
        return [[]]
    if not s or k < 0:
        return []
    s_list = list(s)
    first = s_list[0]
    rest = s_list[1:]
    combs_with_first = [[first] + c for c in get_combinations(rest, k - 1)]
    combs_without_first = get_combinations(rest, k)
    return combs_with_first + combs_without_first

def gcd(a, b):
    return math.gcd(a, b)

def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b)) * b

def lcm_list(numbers):
    if not numbers:
        return 1
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = lcm(result, numbers[i])
    return result

def solve_lcm_pfc_no_itertools(S, T, k, verbose=True):
    """
    Resuelve el problema usando una lista en memoria.
    Retorna: (encontrado, subconjunto, combinaciones_probadas)
    """
    all_combinations = get_combinations(list(S), k)
    combinations_checked = 0
    for s_prime in all_combinations:
        combinations_checked += 1
        current_lcm = lcm_list(list(s_prime))
        if current_lcm % T == 0:
            return True, list(s_prime), combinations_checked
    return False, None, len(all_combinations)

# --- Bloque de Pruebas de Rendimiento ---

TEST_SCENARIOS = [
    {"name": "Caso Base", "n": 4, "k": 2, "max_val": 100},
    {"name": "Medio 1", "n": 10, "k": 4, "max_val": 500},
    {"name": "Medio 2", "n": 15, "k": 7, "max_val": 500},
    {"name": "Medio 3", "n": 20, "k": 5, "max_val": 1000},
    {"name": "Medio-Alto", "n": 20, "k": 10, "max_val": 1000},
    {"name": "Alto 1", "n": 22, "k": 11, "max_val": 5000},
    # Advertencia: Los siguientes casos excederán el tiempo o la memoria.
    {"name": "Alto 2", "n": 25, "k": 12, "max_val": 5000},
    {"name": "Muy Alto", "n": 28, "k": 14, "max_val": 10000},
]

def solver_wrapper(solver_function, q, S, T, k):
    """
    Wrapper para ejecutar el solver y capturar la memoria en un proceso separado.
    """
    tracemalloc.start()
    found, subset, combinations_checked = solver_function(S, T, k, verbose=False)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    q.put((found, combinations_checked, peak))

def run_performance_tests(solver_function, script_name):
    print(f"Iniciando pruebas de rendimiento para {script_name} (límite de 180s por prueba)...")
    header = f"{'Escenario':<15} | {'n':>3} | {'k':>3} | {'Combinaciones':>18} | {'Tiempo (s)':>12} | {'Memoria (KB)':>15} | {'Resultado':>12}"
    print(header)
    print("-" * len(header))

    for scenario in TEST_SCENARIOS:
        n, k, max_val = scenario["n"], scenario["k"], scenario["max_val"]
        S = set(random.sample(range(2, max_val), n))
        T = 9999999999

        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=solver_wrapper, args=(solver_function, q, S, T, k))

        start_time = time.perf_counter()
        p.start()
        p.join(timeout=180) # <--- LÍMITE DE TIEMPO
        end_time = time.perf_counter()

        if p.is_alive():
            # El proceso excedió el tiempo límite
            p.terminate()
            p.join()
            print(f"{scenario['name']:<15} | {n:>3} | {k:>3} | {'N/A':>18} | {'>180.0':>12} | {'N/A':>15} | {'TIMED OUT':>12}")
            continue

        try:
            # Obtener resultados del proceso hijo
            found, combinations_checked, peak = q.get_nowait()
            time_taken = end_time - start_time
            peak_kb = peak / 1024
            print(
                f"{scenario['name']:<15} | {n:>3} | {k:>3} | {combinations_checked:>18,} | "
                f"{time_taken:>12.4f} | {peak_kb:>15.2f} | {str(found):>12}"
            )
        except queue.Empty:
            time_taken = end_time - start_time
            print(f"{scenario['name']:<15} | {n:>3} | {k:>3} | {'N/A':>18} | {time_taken:>12.4f} | {'N/A':>15} | {'ERROR':>12}")

if __name__ == "__main__":
    # Necesario para que multiprocessing funcione correctamente en algunos S.O.
    multiprocessing.freeze_support()
    run_performance_tests(solve_lcm_pfc_no_itertools, "benchmark_no_itertools.py") 