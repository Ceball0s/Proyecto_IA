class Nodo:
    def __init__(self, estado, padre=None, accion=None):
        self.estado = estado  # Representa el estado del nodo (posición)
        self.padre = padre  # Nodo padre (de dónde vino)
        self.accion = accion  # Acción que llevó a este estado
        self.hijos = []  # Lista de nodos hijos

    #def agregar_hijo(self, hijo):
    #    """Agrega un nodo hijo a la lista de hijos."""
    #    self.hijos.append(hijo)
    
    def __eq__(self, otro):
        """Compara el estado de dos nodos."""
        
        return self.estado == otro.estado and self.padre == otro.padre
 

    def __hash__(self):
        """Genera un hash basado en el estado del nodo."""
        return hash(self.estado)

    def obtener_camino(self):
        """Reconstruye el camino desde la raíz hasta este nodo."""
        nodo_actual, camino = self, []
        while nodo_actual:
            camino.append(nodo_actual.accion)
            nodo_actual = nodo_actual.padre
        return camino[::-1]

    def obtener_todos_los_estados(self):
        """Obtiene todos los estados en el árbol a partir de este nodo."""
        def retornar_hijos(nodo):
            lista = []
            if not nodo.hijos:
                return [nodo.estado]
            for hijo in nodo.hijos:
                salida = retornar_hijos(hijo)
                if salida is not None:
                    lista.extend(salida)
            lista.append(nodo.estado)
            return lista

        nodo_actual = self
        while nodo_actual.padre:
            nodo_actual = nodo_actual.padre
        return retornar_hijos(nodo_actual)

    def obtener_hijos_a_profundidad(self, profundidad):
        """Obtiene los estados de los nodos a una profundidad específica."""
        def retornar_hijos(nodo, contador, lista):
            if contador == profundidad:
                if nodo.padre:
                    lista.append((nodo.estado,nodo.padre.estado,nodo))
                else:
                    lista.append((nodo.estado,(),nodo))
                return lista
            if not nodo.hijos or contador > profundidad:
                return 
            for hijo in nodo.hijos:
                retornar_hijos(hijo, contador + 1, lista)
            return lista

        nodo_actual = self
        while nodo_actual.padre:
            nodo_actual = nodo_actual.padre
        return retornar_hijos(nodo_actual, 0, [])
    
    def agregar_hijo(self, posicion, accion):
        """Obtiene un hijo existente o crea uno nuevo si no existe."""
        nodo_actual = self
        while nodo_actual:
            if nodo_actual.estado == posicion:
                return None
            nodo_actual = nodo_actual.padre
        for hijo in self.hijos:
            if posicion == hijo.estado:
                return hijo
    
        nuevo_hijo = Nodo(posicion, padre=self, accion=accion)
        self.hijos.append(nuevo_hijo)
        return nuevo_hijo

    def profundidad(self):
        def profundidad(nodo_actual,contador):
            if nodo_actual.hijos == []:
                return contador
            else:
                mayor = 0
                for hijo in nodo_actual.hijos:
                    salida = profundidad(hijo,contador+1)
                    if salida > mayor:
                        mayor = salida
            return mayor


        nodo_actual = self
        while nodo_actual.padre:
            nodo_actual = nodo_actual.padre
        return profundidad(nodo_actual, 0)
