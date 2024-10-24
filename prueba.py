from Nodo import Nodo
# Crear nodos de ejemplo
nodo_raiz = Nodo(estado=(0, 0))

# Crear hijos del nodo raíz
nodo_hijo1 = Nodo(estado=(1, 0), padre=nodo_raiz, accion="Derecha")
nodo_hijo2 = Nodo(estado=(0, 1), padre=nodo_raiz, accion="Abajo")

# Agregar los hijos al nodo raíz
nodo_raiz.agregar_hijo(nodo_hijo1)
nodo_raiz.agregar_hijo(nodo_hijo2)

# Crear nietos del nodo raíz
nodo_nieto1 = Nodo(estado=(2, 0), padre=nodo_hijo1, accion="Derecha")
nodo_nieto2 = Nodo(estado=(1, 1), padre=nodo_hijo1, accion="Abajo")
nodo_nieto3 = Nodo(estado=(0, 2), padre=nodo_hijo2, accion="Derecha")
nodo_nieto4 = Nodo(estado=(1, 2), padre=nodo_hijo2, accion="Abajo")

# Agregar los nietos
nodo_hijo1.agregar_hijo(nodo_nieto1)
nodo_hijo1.agregar_hijo(nodo_nieto2)
nodo_hijo2.agregar_hijo(nodo_nieto3)
nodo_hijo2.agregar_hijo(nodo_nieto4)

# Obtener los estados de los nodos hasta la profundidad 1
#print("Nodos hasta profundidad 1:", nodo_raiz.obtener_hijos_profundidad(1))

# Obtener los estados de los nodos hasta la profundidad 2
#print("Nodos hasta profundidad 2:", nodo_raiz.obtener_hijos_profundidad(2))

#lista_profundidad = nodo_raiz.obtener_hijos_profundidad(2)

def aplanar_lista(lista):
    return [item for sublista in lista for item in sublista]



#print(recorrer_arbol(nodo_raiz))
print()
print("                                                                                   ")
print("                                                                                   ")

# Crear el árbol
nodo_raiz = Nodo((0, 0))  # Nodo raíz
hijo1 = Nodo((0, 1), padre=nodo_raiz)
hijo2 = Nodo((1, 0), padre=nodo_raiz)

# Agregar los hijos al nodo raíz
nodo_raiz.agregar_hijo(hijo1)
nodo_raiz.agregar_hijo(hijo2)

# Ahora el árbol tiene la siguiente estructura:
# (0, 0)
# ├── (0, 1)
# └── (1, 0)

# Para comprobar la estructura del árbol, puedes imprimir los estados de los nodos:
print("Nodo raíz:", nodo_raiz.estado)
lista = [hijo.estado for hijo in nodo_raiz.hijos]
print("Hijos del nodo raíz:", lista)
for i in lista:
    print(nodo_raiz.indice_padre(i,1))