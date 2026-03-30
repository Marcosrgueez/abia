from nodos import *
from heuristicas import heuristica_mal_colocadas


from abc import abstractmethod
from abc import ABCMeta


#Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass





#Implementa una búsqueda en Anchura genérica (independiente de Estados y Operadores) controlando repetición de estados.
#Usa lista ABIERTOS (lista) y lista CERRADOS (diccionario usando Estado como clave)
class BusquedaAnchura(Busqueda):
    
    #Implementa la búsqueda en anchura. Si encuentra solución recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoAnchura
    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                #cerrados[actual.cubo.visualizar()] = actual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo #utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS 
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
class BusquedaProfundidad(Busqueda):
    
    #Implementa la búsqueda en anchura. Si encuentra solución recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoAnchura
    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAcotado(inicial, None, None))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                #cerrados[actual.cubo.visualizar()] = actual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo #utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS 
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

class BusquedaVoraz(Busqueda):
    def __init__(self, heuristica_fn=heuristica_mal_colocadas):
        self.heuristica_fn = heuristica_fn

    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoVoraz(inicial, None, None, self.heuristica_fn))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                #cerrados[actual.cubo.visualizar()] = actual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoVoraz(hijo, nodoActual, operador, self.heuristica_fn))
                        cerrados[hijo.cubo.visualizar()] = hijo #utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS 
                        abiertos.sort(key=lambda x: x.heuristica) #ordenamos ABIERTOS por heurística (menor primero)
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
class BusquedaAEstrella(Busqueda):
    def __init__(self, heuristica_fn=heuristica_mal_colocadas):
        self.heuristica_fn = heuristica_fn

    def heuristica(self, estado):
        return self.heuristica_fn(estado)

    def buscarSolucion(self, inicial):

        abiertos = []
        cerrados = dict()

        h0 = self.heuristica(inicial)
        nodoInicial = NodoAEstrella(inicial, None, None, 0, h0)

        abiertos.append(nodoInicial)
        cerrados[inicial.cubo.visualizar()] = 0

        while len(abiertos) > 0:

            # Elegir nodo con menor f
            nodoActual = min(abiertos, key=lambda x: x.f)
            abiertos.remove(nodoActual)

            actual = nodoActual.estado

            if actual.esFinal():
                return self.reconstruir(nodoActual)

            for operador in actual.operadoresAplicables():
                hijo_estado = actual.aplicarOperador(operador)
                g_hijo = nodoActual.g + 1
                id_hijo = hijo_estado.cubo.visualizar()

                if id_hijo not in cerrados or g_hijo < cerrados[id_hijo]:
                    cerrados[id_hijo] = g_hijo
                    h_hijo = self.heuristica(hijo_estado)
                    nodoHijo = NodoAEstrella(hijo_estado, nodoActual, operador, g_hijo, h_hijo)
                    abiertos.append(nodoHijo)

        return None


    def reconstruir(self, nodo):
        lista = []
        while nodo.padre is not None:
            lista.insert(0, nodo.operador)
            nodo = nodo.padre
        return lista
        
class BusquedaProfundidadAcotada(Busqueda):
    
    # Implementa la búsqueda en profundidad acotada (cota 6)
    def buscarSolucion(self, inicial, cotaMax=6):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict() 
        cerrados[inicial.cubo.visualizar()] = 0 #añadimos el estado inicial a cerrados para evitar que se vuelva a añadir a abiertos
        # 1. Creamos el nodo raíz con profundidad (depth) 0
        # Usamos tu clase NodoAcotado
        abiertos.append(NodoAcotado(inicial, None, None, 0))
        
        while not solucion and len(abiertos) > 0:
            # 2. LIFO: pop() saca el último elemento (comportamiento de Pila)
            # Esto es lo que define a la búsqueda en Profundidad
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            if nodoActual.depth <= cotaMax:
                # 3. Verificamos si el estado del cubo es el objetivo
                if actual.esFinal():
                    solucion = True
                else:
                    # 4. GESTIÓN DE LA COTA:
                    # Si el nodo actual tiene una profundidad menor que la cota, expandimos
                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)
                        if hijo.cubo.visualizar() not in cerrados.keys() or nodoActual.depth + 1 < cerrados[hijo.cubo.visualizar()]:
                            abiertos.append(NodoAcotado(hijo, nodoActual, operador, nodoActual.depth + 1))
                            cerrados[hijo.cubo.visualizar()] = nodoActual.depth + 1 #utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS
            
        # 6. Reconstrucción del camino (si hay solución)
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: 
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

class BusquedaIterativa(Busqueda):
    
    def buscarSolucion(self, inicial):
        # La búsqueda iterativa va probando cotas crecientes
        cota = 0
        solucion = None
        
        # El bucle continúa hasta que se encuentre una solución
        # (O podrías poner un límite máximo de seguridad, por ejemplo 20)
        while solucion is None:
            # Llamamos a un método auxiliar que hace la búsqueda acotada
            
            solucion = BusquedaProfundidadAcotada().buscarSolucion(inicial, cota)

            
            if solucion is not None:
                return solucion # Si la encuentra, la devuelve y termina
            
            # Si no hay solución con esta cota, incrementamos y repetimos
            cota += 1
            
    # Este método es idéntico al que hicimos antes
    def busqueda_acotada(self, inicial, cotaMax):
        abiertos = []
        # Usamos tu NodoAcotado
        abiertos.append(NodoAcotado(inicial, None, None, 0))
        
        while len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            
            if actual.esFinal():
                # Reconstrucción del camino
                lista = []
                nodo = nodoActual
                while nodo.padre != None: 
                    lista.insert(0, nodo.operador)
                    nodo = nodo.padre
                return lista
            
            if nodoActual.depth < cotaMax:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    nuevoNodo = NodoAcotado(hijo, nodoActual, operador, nodoActual.depth + 1)
                    abiertos.append(nuevoNodo)
        
        return None # No hay solución para esta cota específica

class BusquedaVoraz(Busqueda):
    def __init__(self, heuristica_fn=heuristica_mal_colocadas):
        self.heuristica_fn = heuristica_fn

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()

        # a�adir ESTADO_INICIAL a ABIERTOS
        abiertos.append(NodoVoraz(inicial, None, None, self.heuristica_fn))

        # inicializar CERRADOS a VACIO
        while not solucion and len(abiertos) > 0:
            # ACTUAL := primer nodo de ABIERTOS
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado

            if actual.esFinal():
                solucion = True
            else:
                # a�adir ACTUAL a CERRADOS
                cerrados[actual.cubo.visualizar()] = actual

                # expandir ACTUAL
                for operador in actual.operadoresAplicables():
                    # generar NUEVO_ESTADO aplicando OPERADOR
                    hijo = actual.aplicarOperador(operador)
                    idHijo = hijo.cubo.visualizar()

                    # NUEVO_ESTADO no en ABIERTOS
                    enAbiertos = False
                    for nodo in abiertos:
                        if nodo.estado.cubo.visualizar() == idHijo:
                            enAbiertos = True
                            break

                    # NUEVO_ESTADO no en CERRADOS
                    if not enAbiertos and idHijo not in cerrados.keys():
                        # a�adir NUEVO_ESTADO en ABIERTOS
                        abiertos.append(NodoVoraz(hijo, nodoActual, operador, self.heuristica_fn))
                        # ordenar ABIERTOS por valor heuristico [h(e)]
                        abiertos.sort(key=lambda x: x.heuristica)

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:  # Asciende hasta la raiz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
class BusquedaIDAEstrella(Busqueda):

    def __init__(self, heuristica_fn=heuristica_mal_colocadas):
        self.heuristica_fn = heuristica_fn

    def heuristica(self, estado):
        return self.heuristica_fn(estado)

    def buscarSolucion(self, inicial):
        cota = self.heuristica(inicial)  # ← único cambio: la cota inicial es h(inicial), no 0
        solucion = None

        while solucion is None:
            solucion = self.busqueda_acotada(inicial, cota)

            if solucion is not None:
                return solucion

            cota += 1  # ← en IDA* puro esto sería el mínimo f que superó la cota, pero +1 es válido

        return None

    def busqueda_acotada(self, inicial, cotaMax):
        abiertos = []
        abiertos.append(NodoAcotado(inicial, None, None, 0))

        while len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado

            if actual.esFinal():
                lista = []
                nodo = nodoActual
                while nodo.padre is not None:
                    lista.insert(0, nodo.operador)
                    nodo = nodo.padre
                return lista

            g_actual = nodoActual.depth
            f_actual = g_actual + self.heuristica(actual)  # ← único cambio respecto a BusquedaIterativa

            if f_actual <= cotaMax:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    nuevoNodo = NodoAcotado(hijo, nodoActual, operador, g_actual + 1)
                    abiertos.append(nuevoNodo)

        return None
    
class BusquedaAEstrellaWeighted(Busqueda):

    W = 1.5

    def __init__(self, heuristica_fn=heuristica_mal_colocadas):
        self.heuristica_fn = heuristica_fn

    def heuristica(self, estado):
        return self.heuristica_fn(estado)

    def buscarSolucion(self, inicial):

        abiertos = []
        cerrados = dict()

        h0 = self.heuristica(inicial)
        nodoInicial = NodoAEstrella(inicial, None, None, g=0, h=self.W * h0)

        abiertos.append(nodoInicial)
        cerrados[inicial.cubo.visualizar()] = 0

        while len(abiertos) > 0:

            nodoActual = min(abiertos, key=lambda x: x.f)
            abiertos.remove(nodoActual)

            actual = nodoActual.estado

            if actual.esFinal():
                return self.reconstruir(nodoActual)

            for operador in actual.operadoresAplicables():
                hijo_estado = actual.aplicarOperador(operador)
                g_hijo = nodoActual.g + 1
                id_hijo = hijo_estado.cubo.visualizar()

                if id_hijo not in cerrados or g_hijo < cerrados[id_hijo]:
                    cerrados[id_hijo] = g_hijo
                    h_hijo = self.heuristica(hijo_estado)
                    nodoHijo = NodoAEstrella(hijo_estado, nodoActual, operador, g_hijo, h_hijo)
                    abiertos.append(nodoHijo)
        return None

    def reconstruir(self, nodo):
        lista = []
        while nodo.padre is not None:
            lista.insert(0, nodo.operador)
            nodo = nodo.padre
        return lista
