from collections import deque
import heapq  # Para la cola de prioridad
from Juego_herramientas import generate_grid,get_move_cost,obtener_vecinos
from Nodo import Nodo
from Constantes import *

# Función que implementa la búsqueda en anchura (BFS)
def bfs(raiz, meta, grid, n):
    explorado = set()  # Conjunto para evitar ciclos
    frontera = deque([raiz])  # Cola con el nodo inicial
    contador = 0
    
    # Mientras haya nodos en la frontera
    while frontera:
        # Extraer el nodo de la frontera
        nodo_actual = frontera.popleft()

        # Si el estado es el objetivo o se llega al límite de nodos explorados
        if nodo_actual.estado == meta or contador >= n:
            return nodo_actual

        # Marcar el nodo actual como explorado
        if nodo_actual.estado in explorado:
            continue
        explorado.add(nodo_actual.estado)

        # Si no tiene hijos y no hay vecinos, continuar con el siguiente nodo
        if not nodo_actual.hijos and len(obtener_vecinos(nodo_actual.estado, grid)) == 0:
            continue

        # Verificar los hijos actuales
        hijos_actuales = [hijo.estado for hijo in nodo_actual.hijos]
        hijos_agregados = 0

        # Expandir los hijos (vecinos) del nodo actual
        for accion, posicion, costo in obtener_vecinos(nodo_actual.estado, grid):
            if posicion not in explorado:
                # Agregar el hijo al nodo actual
                hijo = nodo_actual.agregar_hijo(posicion, accion)
                
                if not hijo:  # Si el hijo no es válido, continuar
                    continue

                # Verificar si el hijo no está en la frontera ya
                if hijo not in frontera:
                    frontera.append(hijo)  # Agregar a la frontera
                
                # Solo contar el hijo si no estaba ya en los hijos actuales
                if posicion not in hijos_actuales:
                    hijos_agregados += 1

        # Incrementar el contador solo si se agregaron nuevos hijos
        if hijos_agregados != 0:
            contador += 1  
    
    # Si no se encuentra la meta, retornar None
    return None


def dfs(raiz, meta, grid, n):
    frontera = [raiz]  # Usamos una lista como pila
    explorado = set()  # Conjunto de nodos explorados
    contador = 0  # Contador de nodos explorados
    
    while frontera:
        nodo_actual = frontera.pop()  # Extrae de la frontera (último elemento)
        
        # Si es el estado objetivo o alcanzamos el límite de nodos
        if nodo_actual.estado == meta or contador >= n:
            return nodo_actual
        
        # Si el nodo actual ya ha sido explorado, lo saltamos
        if nodo_actual.estado in explorado:
            continue
        
        
        explorado.add(nodo_actual.estado)  # Marcar el nodo como explorado
        hijos_actuales = [hijo.estado for hijo in nodo_actual.hijos]
        hijos_agregados = 0
        # Expandir los hijos (vecinos)
        for accion, posicion, costo in obtener_vecinos(nodo_actual.estado, grid):
            if posicion not in explorado:
                hijo = nodo_actual.agregar_hijo(posicion, accion)
                if not hijo:
                    continue
                if hijo not in frontera:
                    frontera.append(hijo)  # Agregar a la frontera (pila)
                # Solo contar el hijo si no estaba ya en los hijos actuales
                if posicion not in hijos_actuales:
                    hijos_agregados += 1
        # Incrementar el contador solo si se agregaron nuevos hijos
        if hijos_agregados != 0:
            contador += 1      
    return None  # Si no se encuentra la meta o se alcanzan los nodos límite


# Función que implementa la búsqueda por costo uniforme (UCS)
def ucs(raiz, meta, grid, n):
    frontera = []  # Usamos una cola de prioridad
    heapq.heappush(frontera, (0, 0, raiz))  # (costo acumulado, contador, nodo)
    
    explorado = set()  # Conjunto para evitar ciclos
    contador = 0  # Para gestionar el desempate en la cola de prioridad
    pasos_realizados = 0  # Contador para los nodos explorados

    while frontera:
        # Extraer el nodo con el costo acumulado más bajo
        costo_acumulado, _, nodo_actual = heapq.heappop(frontera)
        
        # Si el nodo actual es la meta o hemos alcanzado el límite de nodos, lo devolvemos
        if nodo_actual.estado == meta or pasos_realizados >= n:
            return nodo_actual
        #pasos_realizados += 1
        # Marcar el estado como explorado
        explorado.add(nodo_actual.estado)
        
        hijos_actuales = [hijo.estado for hijo in nodo_actual.hijos]
        hijos_agregados = 0
        # Expandir los hijos (vecinos) del nodo actual
        for accion, posicion, costo in obtener_vecinos(nodo_actual.estado, grid):
            if posicion not in explorado:
                # Verificar si ya es un hijo actual
                hijo = nodo_actual.agregar_hijo(posicion, accion)
                if not hijo:
                    continue
                contador += 1  # Incrementar el contador para desempatar en el heap
                heapq.heappush(frontera, (costo_acumulado + costo, contador, hijo))
                if hijo.estado not in hijos_actuales:
                    # Sumar el costo y agregar a la cola de prioridad
                    hijos_agregados += 1  # Incrementar el contador de pasos

                    # Si hemos alcanzado el límite de `n` nodos creados, detenemos
                    #if pasos_realizados >= n:
                    #    return hijo
        if hijos_agregados != 0:
            pasos_realizados += 1
    return None  # Si no se encuentra la meta o se agotan los pasos


def distancia_manhattan(estado, meta):
    # Estado y meta son tuplas con coordenadas (x, y)
    return abs(estado[0] - meta[0]) + abs(estado[1] - meta[1])

# Función que implementa la búsqueda ávara con desempate
def avara(raiz, meta, grid, n):
    frontera = []  # Cola de prioridad
    heapq.heappush(frontera, (0, 0, raiz))  # (heurística, contador, nodo)
    
    explorado = set()  # Conjunto para evitar ciclos
    pasos_realizados = 0  # Contador para los nodos explorados
    contador = 0  # Para desempatar en la cola de prioridad

    while frontera:
        heuristica, _, nodo_actual = heapq.heappop(frontera)
        
        # Si el nodo actual es la meta o hemos alcanzado el límite de nodos, devolvemos el nodo
        if nodo_actual.estado == meta or pasos_realizados >= n:
            return nodo_actual
        #pasos_realizados += 1
        # Marcar el estado como explorado
        explorado.add(nodo_actual.estado)

        # Expandir los hijos (vecinos)
        hijos_actuales = [hijo.estado for hijo in nodo_actual.hijos]
        hijos_agregados = 0
        for accion, posicion, costo in obtener_vecinos(nodo_actual.estado, grid):
            if posicion not in explorado:
                # Verificar si el nodo hijo ya existe, si no, crearlo
                hijo = nodo_actual.agregar_hijo(posicion, accion)
                if not hijo:
                    continue
                # Calcular la heurística (distancia Manhattan en este caso)
                heuristica = distancia_manhattan(posicion, meta)
                heapq.heappush(frontera, (heuristica, contador, hijo))
                contador += 1
                # Incrementar el contador para desempatar en el heap
                # Añadir el hijo a la frontera si no es un hijo actual
                if hijo.estado not in hijos_actuales:
                #    
                    hijos_agregados += 1
                #    # Si alcanzamos el límite de `n` nodos, detenemos
                #    if pasos_realizados >= n:
                #        return hijo
        if hijos_agregados != 0:
            pasos_realizados += 1
    return None  # Si no se encuentra la meta o se agotan los pasos


def busqueda_en_profundidad_limitada(nodo_actual, meta, grid, limite, explorado, n, nodos_creados):
    # Si se alcanzó la meta, retorna el nodo
    if nodo_actual.estado == meta:
        return nodo_actual, nodos_creados
    
    # Si se ha alcanzado el límite de profundidad o el número de nodos creados, retornar None
    if limite == 0 or nodos_creados >= n:
        return nodo_actual, nodos_creados
    #nodos_creados += 1
    # Evitar explorar nodos ya explorados
    explorado.add(nodo_actual.estado)

    hijos_actuales = [hijo.estado for hijo in nodo_actual.hijos]
    # Expandir los hijos del nodo actual
    hijos_agregados = 0
    for accion, posicion, costo in obtener_vecinos(nodo_actual.estado, grid):
        if posicion not in explorado:
            hijo = nodo_actual.agregar_hijo(posicion, accion)
            if not hijo:
                continue
            # Solo contar el nodo si realmente se creó un nuevo hijo
            if posicion not in hijos_actuales:
                hijos_agregados += 1
            
            # Llamada recursiva para seguir explorando en profundidad
            resultado, nodos_creados = busqueda_en_profundidad_limitada(hijo, meta, grid, limite - 1, explorado, n, nodos_creados)
            
            # Si se encuentra la meta en la llamada recursiva
            if resultado:
                return resultado, nodos_creados
    if hijos_agregados != 0:
                nodos_creados += 1
    # Si no se encuentra solución en esta rama
    return None, nodos_creados


def ids(raiz, meta, grid, n):
    limite = raiz.profundidad()
    nodos_creados = 0
    contador = 0
    while nodos_creados <= n:
        explorado = set()  # Reiniciar el conjunto de estados explorados para cada profundidad
        nodos_antes = nodos_creados
        # Llamada a la búsqueda en profundidad limitada
        resultado, nodos_creados = busqueda_en_profundidad_limitada(raiz, meta, grid, limite, explorado, n, nodos_creados)

        if nodos_antes == nodos_creados and contador == 2:
            return None # no ahi solucion
        if nodos_antes == nodos_creados:
            contador += 1
        if nodos_antes != nodos_creados and contador != 0:
            contador = 0

        # Si se encuentra la meta, retornamos el resultado
        if resultado:
            return resultado
        # Si no se encuentra solución, aumentamos el límite de profundidad
        limite += 1

    # Si no se encuentra solución en `n` nodos, retornamos None
    return None

# Ejemplo de función para obtener vecinos (esto variará según el tablero)
#def obtener_vecinos(estado):
#    # Vecinos del nodo en función del estado actual (esto es un ejemplo simple)
#    vecinos = []
#    vecinos.append(('arriba', estado + 1))  # Vecino hipotético "arriba"
#    vecinos.append(('abajo', estado - 1))   # Vecino hipotético "abajo"
#    return vecinos
if __name__ == "__main__":
    # Ejemplo de uso
    inicio = (0,0)  # Estado inicial (por ejemplo, la posición del ratón)
    meta = (4,4)    # Estado meta (por ejemplo, la posición del queso)
    grid = generate_grid(5)
    for i in grid:
        pass
        #print(i)
    camino = bfs(inicio, meta, obtener_vecinos, grid)

    if camino:
        print("Camino encontrado:", camino)
    else:
        print("No se encontró una solución.")
