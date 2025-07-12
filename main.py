
# ##############################################################################
# # 7. Implementación en Python (Demostración)
# ##############################################################################

# # El siguiente código implementa una solución de fuerza bruta para el problema
# # LCM Prime Factor Covering. Dado que el problema es NP-completo, esta
# # solución explora todas las combinaciones posibles de subconjuntos de tamaño
# # hasta k, lo cual es solo factible para entradas pequeñas.

import math
from itertools import combinations
# NOTA: Se utiliza `itertools.combinations` por ser un generador. Este método es crucial para la eficiencia de memoria,
        # generador. Este método es crucial para la eficiencia de memoria,
        # ya que crea las combinaciones una por una bajo demanda en lugar
        # de almacenarlas todas a la vez. Esto mantiene la complejidad
        # espacial en O(k). Una implementación que guarde todas las
        # combinaciones en una lista tendría una complejidad espacial de
        # O(C(n, k) * k), lo cual sería inviable.
def gcd(a, b):
    """Calcula el Máximo Común Divisor de a y b."""
    return math.gcd(a, b)

def lcm(a, b):
    """Calcula el Mínimo Común Múltiplo de a y b."""
    if a == 0 or b == 0:
        return 0
    # La fórmula estándar es (a * b) / gcd(a, b).
    # Sin embargo, para evitar un posible desbordamiento numérico (overflow)
    # cuando 'a' y 'b' son muy grandes, se realiza la división antes
    # de la multiplicación. Ambas formas son matemáticamente equivalentes.
    return abs(a // gcd(a, b)) * b

def lcm_list(numbers):
    """Calcula el LCM de una lista de números."""
    if not numbers:
        return 1
    
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = lcm(result, numbers[i])
    return result

def solve_lcm_pfc(S, T, k):
    """
    Resuelve el problema LCM Prime Factor Covering mediante fuerza bruta.

    Args:
        S (list or set): El conjunto de enteros positivos.
        T (int): El entero objetivo.
        k (int): El tamaño máximo del subconjunto.

    Returns:
        tuple: Una tupla (bool, list) donde el bool es True si se encontró
               una solución y la lista es el subconjunto S' que la satisface.
               Retorna (False, None) si no se encuentra solución.
    """
    print(f"Buscando un subconjunto S' ⊆ {S} de tamaño ≤ {k} tal que {T} | LCM(S')...\n")
    
    # Iterar sobre todos los tamaños de subconjunto posibles, desde 1 hasta k
    for i in range(1, k + 1):
        for s_prime in combinations(S, i):
            # Calcular el LCM del subconjunto actual
            current_lcm = lcm_list(list(s_prime))
            
            print(f"  Probando S' = {list(s_prime)} -> LCM = {current_lcm}")
            
            # Verificar si T divide al LCM
            if current_lcm % T == 0:
                print(f"\n¡Solución encontrada!")
                return True, list(s_prime)

    print("\nNo se encontró ningún subconjunto que satisfaga la condición.")
    return False, None

# --- Bloque de Demostración ---
if __name__ == "__main__":
    # Usamos el mismo ejemplo de la presentación
    S_example = {6, 10, 14, 35}
    T_example = 70
    k_example = 2 # <--- Aquí está la clave, ojo con esto.

    # Resolvemos el problema
    found, subset = solve_lcm_pfc(S_example, T_example, k_example)

    # Imprimimos el resultado final
    if found:
        print(f"Resultado: SÍ. El subconjunto {subset} funciona.")
        print(f"Verificación: LCM({subset}) = {lcm_list(subset)}, y {lcm_list(subset)} % {T_example} = {lcm_list(subset) % T_example}")
    else:
        print(f"Resultado: NO. No se encontró solución.")
