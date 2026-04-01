

#Nodos a almacenar como parte de los algoritmos de búsqueda

class Nodo:
    def __init__(self, estado, padre):
        self.estado=estado
        self.padre=padre




#Nodos usados por la BusquedaAnchura. 
#Añade el Operador usado para generar el estado almacenado en este Nodo. 
#Usado para simplificar la reconstrucción del camino solución.

class NodoAnchura(Nodo):
    def __init__(self, estado, padre, operador):
        super().__init__(estado, padre)
        self.operador = operador

class NodoAcotado(Nodo):
    def __init__(self, estado, padre, operador, depth):
        super().__init__(estado, padre)
        self.operador = operador
        self.depth = depth

class NodoVoraz(Nodo):
    def __init__(self, estado, padre, operador, heuristica_fn):
        super().__init__(estado, padre)
        self.operador = operador
        self.heuristica = heuristica_fn(estado)  # ← con (estado), llamando a la función

class NodoAEstrella(Nodo):
    def __init__(self, estado, padre, operador, g, h):
        super().__init__(estado, padre)
        self.operador = operador
        self.g = g
        self.h = h
        self.f = g + h
