from nodos import *
from heuristicas import heuristica_mal_colocadas
from abc import abstractmethod, ABCMeta
from collections import deque

class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass

    def _recuperar_camino(self, nodo):
        path = []
        curr = nodo
        while curr.padre is not None:
            path.append(curr.operador)
            curr = curr.padre
        return path[::-1] # Invertimos la lista

class BusquedaAnchura(Busqueda):
    def buscarSolucion(self, inicial):
        self.nodos_explorados = 0
        self.max_abiertos = 0
        
        # Usamos deque para que el popleft() sea O(1)
        queue = deque([NodoAnchura(inicial, None, None)])
        visitados = {inicial.cubo.visualizar(): inicial}

        while queue:
            if len(queue) > self.max_abiertos:
                self.max_abiertos = len(queue)
            
            nodo_act = queue.popleft()
            estado_act = nodo_act.estado
            self.nodos_explorados += 1

            if estado_act.esFinal():
                return self._recuperar_camino(nodo_act)

            for op in estado_act.operadoresAplicables():
                hijo_estado = estado_act.aplicarOperador(op)
                id_hijo = hijo_estado.cubo.visualizar()
                
                if id_hijo not in visitados:
                    nuevo_nodo = NodoAnchura(hijo_estado, nodo_act, op)
                    queue.append(nuevo_nodo)
                    visitados[id_hijo] = hijo_estado
                    
        return None

class BusquedaProfundidad(Busqueda):
    def buscarSolucion(self, inicial):
        self.nodos_explorados = 0
        self.max_abiertos = 0
        
        stack = [NodoAnchura(inicial, None, None)]
        visitados = {inicial.cubo.visualizar(): inicial}

        while stack:
            if len(stack) > self.max_abiertos:
                self.max_abiertos = len(stack)
                
            curr_node = stack.pop()
            curr_state = curr_node.estado
            self.nodos_explorados += 1

            if curr_state.esFinal():
                return self._recuperar_camino(curr_node)

            for op in curr_state.operadoresAplicables():
                succ_state = curr_state.aplicarOperador(op)
                succ_id = succ_state.cubo.visualizar()
                
                if succ_id not in visitados:
                    stack.append(NodoAnchura(succ_state, curr_node, op))
                    visitados[succ_id] = succ_state
        return None

class BusquedaProfundidadAcotada(Busqueda):
    def buscarSolucion(self, inicial, limite=6):
        self.nodos_explorados = 0
        self.max_abiertos = 0
        
        # Diccionario guarda la profundidad mínima a la que se vio un estado
        history = {inicial.cubo.visualizar(): 0}
        frontier = [NodoAcotado(inicial, None, None, 0)]

        while frontier:
            if len(frontier) > self.max_abiertos:
                self.max_abiertos = len(frontier)
                
            node = frontier.pop()
            self.nodos_explorados += 1

            if node.depth <= limite:
                if node.estado.esFinal():
                    return self._recuperar_camino(node)
                
                for action in node.estado.operadoresAplicables():
                    child_state = node.estado.aplicarOperador(action)
                    cid = child_state.cubo.visualizar()
                    new_depth = node.depth + 1
                    
                    if cid not in history or new_depth < history[cid]:
                        history[cid] = new_depth
                        frontier.append(NodoAcotado(child_state, node, action, new_depth))
        return None

class BusquedaIterativa(Busqueda):
    def buscarSolucion(self, inicial):
        self.nodos_explorados = 0
        self.max_abiertos = 0
        depth_limit = 0

        while True:
            engine = BusquedaProfundidadAcotada()
            res = engine.buscarSolucion(inicial, depth_limit)
            
            self.nodos_explorados += engine.nodos_explorados
            self.max_abiertos = max(self.max_abiertos, engine.max_abiertos)

            if res is not None:
                return res
            depth_limit += 1

class BusquedaVoraz(Busqueda):
    def __init__(self, h_func=heuristica_mal_colocadas):
        self.h_func = h_func

    def buscarSolucion(self, inicial):
        self.nodos_explorados = 0
        self.max_abiertos = 0
        
        open_list = [NodoVoraz(inicial, None, None, self.h_func)]
        closed_list = {inicial.cubo.visualizar()}

        while open_list:
            # Ordenar por heurística y sacar el mejor
            open_list.sort(key=lambda n: n.heuristica)
            node = open_list.pop(0)
            
            self.nodos_explorados += 1
            if node.estado.esFinal():
                return self._recuperar_camino(node)

            for op in node.estado.operadoresAplicables():
                child = node.estado.aplicarOperador(op)
                uid = child.cubo.visualizar()
                
                if uid not in closed_list:
                    open_list.append(NodoVoraz(child, node, op, self.h_func))
                    closed_list.add(uid)
            
            self.max_abiertos = max(self.max_abiertos, len(open_list))
        return None

class BusquedaAEstrella(Busqueda):
    def __init__(self, h_func=heuristica_mal_colocadas):
        self.h_func = h_func

    def buscarSolucion(self, inicial):
        self.nodos_explorados = 0
        self.max_abiertos = 0
        
        start_node = NodoAEstrella(inicial, None, None, 0, self.h_func(inicial))
        open_set = [start_node]
        closed_set = {inicial.cubo.visualizar(): 0}

        while open_set:
            # Seleccionamos el nodo con menor f
            current = min(open_set, key=lambda n: n.f)
            open_set.remove(current)
            self.nodos_explorados += 1

            if current.estado.esFinal():
                return self._recuperar_camino(current)

            for action in current.estado.operadoresAplicables():
                neighbor_state = current.estado.aplicarOperador(action)
                g_score = current.g + 1
                nid = neighbor_state.cubo.visualizar()

                if nid not in closed_set or g_score < closed_set[nid]:
                    closed_set[nid] = g_score
                    h_score = self.h_func(neighbor_state)
                    open_set.append(NodoAEstrella(neighbor_state, current, action, g_score, h_score))
            
            self.max_abiertos = max(self.max_abiertos, len(open_set))
        return None

class BusquedaIDAEstrella(Busqueda):
    def __init__(self, h_func=heuristica_mal_colocadas):
        self.h_func = h_func

    def buscarSolucion(self, inicial):
        threshold = self.h_func(inicial)
        self.nodos_explorados = 0
        self.max_abiertos = 0

        while True:
            result = self._dfs_coste(inicial, threshold)
            if isinstance(result, list):
                return result
            if result == float('inf'):
                return None
            threshold = result

    def _dfs_coste(self, inicial, limite_f):
        # Implementación usando una pila para evitar recursión pesada
        stack = [NodoAcotado(inicial, None, None, 0)]
        min_over = float('inf')

        while stack:
            self.max_abiertos = max(self.max_abiertos, len(stack))
            node = stack.pop()
            self.nodos_explorados += 1
            
            f_val = node.depth + self.h_func(node.estado)

            if node.estado.esFinal():
                return self._recuperar_camino(node)

            if f_val <= limite_f:
                for op in node.estado.operadoresAplicables():
                    child = node.estado.aplicarOperador(op)
                    stack.append(NodoAcotado(child, node, op, node.depth + 1))
            else:
                if f_val < min_over:
                    min_over = f_val
        
        return min_over

class BusquedaAEstrellaWeighted(Busqueda):
    W = 1.5
    def __init__(self, h_func=heuristica_mal_colocadas):
        self.h_func = h_func

    def buscarSolucion(self, inicial):
        self.nodos_explorados = 0
        self.max_abiertos = 0
        
        entry = NodoAEstrella(inicial, None, None, 0, self.W * self.h_func(inicial))
        frontier = [entry]
        costs = {inicial.cubo.visualizar(): 0}

        while frontier:
            node = min(frontier, key=lambda n: n.f)
            frontier.remove(node)
            self.nodos_explorados += 1

            if node.estado.esFinal():
                return self._recuperar_camino(node)

            for op in node.estado.operadoresAplicables():
                child_st = node.estado.aplicarOperador(op)
                new_g = node.g + 1
                cid = child_st.cubo.visualizar()

                if cid not in costs or new_g < costs[cid]:
                    costs[cid] = new_g
                    h_val = self.h_func(child_st) * self.W
                    frontier.append(NodoAEstrella(child_st, node, op, new_g, h_val))
            
            self.max_abiertos = max(self.max_abiertos, len(frontier))
        return None
