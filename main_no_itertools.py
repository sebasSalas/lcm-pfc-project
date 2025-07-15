# # El siguiente código implementa una solución de fuerza bruta para el problema
# # LCM Prime Factor Covering. A diferencia de la versión original, esta
# # implementación NO UTILIZA `itertools.combinations`. En su lugar, genera
# # y almacena todas las combinaciones de subconjuntos en memoria, lo que
# # demuestra la ineficiencia espacial de este enfoque.

import math
# Se elimina la importación de `itertools.combinations`

# NOTA DE DISEÑO:
# En esta versión, hemos reemplazado el generador `itertools.combinations`
# por una función `find_combinations` que retorna una lista completa con
# todos los subconjuntos. Esto tiene una implicación directa y negativa
# en la complejidad espacial. Mientras que la versión con `itertools`
# tenía una complejidad espacial de O(k), esta versión tiene una
# complejidad de O(C(n, k) * k), donde C(n, k) es el coeficiente
# binomial. Para entradas grandes, esto agotaría rápidamente la memoria
# del sistema.

def get_combinations(s, k):
    
    # Genera todas las combinaciones de tamaño k del conjunto s.
    # Esta función es ineficiente en memoria ya que retorna una lista completa.
    
    if k == 0:
        return [[]]
    if not s or k < 0:
        return []

    s_list = list(s)
    first = s_list[0]
    rest = s_list[1:]
    
    # Combinaciones que incluyen el primer elemento + combinaciones que no lo incluyen.
    combs_with_first = [[first] + c for c in get_combinations(rest, k - 1)]
    combs_without_first = get_combinations(rest, k)
    
    return combs_with_first + combs_without_first

def gcd(a, b):
    # Calcula el Máximo Común Divisor de a y b.
    return math.gcd(a, b)

def lcm(a, b):
    # Calcula el Mínimo Común Múltiplo de a y b.
    if a == 0 or b == 0:
        return 0
    # La fórmula estándar es (a * b) / gcd(a, b).
    # Sin embargo, para evitar un posible desbordamiento numérico (overflow)
    # cuando 'a' y 'b' son muy grandes, se realiza la división antes
    # de la multiplicación. Ambas formas son matemáticamente equivalentes.
    return abs(a // gcd(a, b)) * b

def lcm_list(numbers):
    # Calcula el LCM de una lista de números.
    if not numbers:
        return 1
    
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = lcm(result, numbers[i])
    return result

def solve_lcm_pfc(S, T, k):
    """
    Resuelve el problema LCM Prime Factor Covering mediante fuerza bruta
    busca todos los subconjuntos de tamaño EXACTO k que cumplan la condición.

    Args:
        S (list or set): El conjunto de enteros positivos.
        T (int): El entero objetivo.
        k (int): El tamaño máximo del subconjunto.

    Returns:
        tuple: Una tupla (bool, list) donde el bool es True si se encontró
               al menos una solución, y la lista contiene todos los subconjuntos S'
               que la satisfacen. Retorna (False, None) si no se encuentra solución.
    """
    print(f"Buscando todos los subconjuntos S' ⊆ {S} de tamaño EXACTO {k} tal que {T} | LCM(S')...\n")
    
    # Generamos y almacenamos TODAS las combinaciones de tamaño 'k' en una lista.
    all_combinations = get_combinations(list(S), k)
    print(f"Generadas {len(all_combinations)} combinaciones de tamaño {k} para S'.")

    solutions = [] # Lista para almacenar todas las soluciones encontradas

    for s_prime in all_combinations:
        # Calcular el LCM del subconjunto actual
        current_lcm = lcm_list(list(s_prime))
        
        print(f"  Probando S' = {list(s_prime)} -> LCM = {current_lcm}")
        
        # Verificar si T divide al LCM
        if current_lcm % T == 0:
            print(f"    -> ¡Solución válida encontrada!")
            solutions.append(list(s_prime))

    if solutions:
        print(f"\nSe encontraron {len(solutions)} subconjunto(s) que satisfacen la condición.")
        return True, solutions
    else:
        print("\nNo se encontró ningún subconjunto que satisfaga la condición.")
        return False, None

# --- Bloque de Demostración ---
if __name__ == "__main__":
    # Usamos el mismo ejemplo de la presentación
    S = {6, 10, 14, 35}
    T = 70
    k = 3 # <--- Aquí está la clave, ojo con esto.

    # Resolvemos el problema
    found, subsets = solve_lcm_pfc(S, T, k)

    # Imprimimos el resultado final
    if found:
        print(f"\nResultado: SÍ. Se encontraron {len(subsets)} soluciones:")
        for s in subsets:
            print(f"  - El subconjunto {s} funciona.")
            print(f"    Verificación: LCM({s}) = {lcm_list(s)}, y {lcm_list(s)} % {T} = {lcm_list(s) % T}")
    else:
        print(f"Resultado: NO. No se encontró solución.") 