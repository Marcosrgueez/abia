

class Nodo:
    """Clase base para representar un estado en el árbol de exploración."""
    def __init__(self, data_estado, node_padre):
        self.estado = data_estado
        self.padre = node_padre


class NodoAnchura(Nodo):
    """Nodo estándar para búsquedas no informadas (BFS/DFS)."""
    def __init__(self, estado, padre, op_aplicado):
        super().__init__(estado, padre)
        self.operador = op_aplicado


class NodoAcotado(Nodo):
    """Extensión para búsquedas con límite de profundidad o IDA*."""
    def __init__(self, state, parent, action, nivel):
        super().__init__(state, parent)
        self.operador = action
        self.depth = nivel


class NodoVoraz(Nodo):
    """Nodo que autocalcula su prioridad basada únicamente en la heurística."""
    def __init__(self, st, p, op, fn_h):
        super().__init__(st, p)
        self.operador = op
        # Calculamos el valor heurístico en el momento de la instanciación
        self.heuristica = fn_h(st)


class NodoAEstrella(Nodo):
    """Nodo para algoritmos A* que gestiona coste acumulado (g) y estimado (h)."""
    def __init__(self, estado_actual, padre, movimiento, coste_g, estimado_h):
        super().__init__(estado_actual, padre)
        self.operador = movimiento
        self.g = coste_g
        self.h = estimado_h
        # La función f(n) es la suma del coste real y la estimación
        self.f = coste_g + estimado_h
