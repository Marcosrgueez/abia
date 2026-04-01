from nodos import *
from heuristicas import heuristica_mal_colocadas

from abc import abstractmethod
from abc import ABCMeta

class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass

class BusquedaAnchura(Busqueda):

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        self.nodos_explorados = 0
        self.max_abiertos = 0

        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()] = inicial

        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            self.nodos_explorados += 1
            if len(abiertos) > self.max_abiertos:
                self.max_abiertos = len(abiertos)

            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None


class BusquedaProfundidad(Busqueda):

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        self.nodos_explorados = 0
        self.max_abiertos = 0

        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()] = inicial

        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            self.nodos_explorados += 1
            if len(abiertos) > self.max_abiertos:
                self.max_abiertos = len(abiertos)

            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None


class BusquedaProfundidadAcotada(Busqueda):

    def buscarSolucion(self, inicial, cotaMax=6):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        self.nodos_explorados = 0
        self.max_abiertos = 0

        cerrados[inicial.cubo.visualizar()] = 0
        abiertos.append(NodoAcotado(inicial, None, None, 0))

        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            self.nodos_explorados += 1
            if len(abiertos) > self.max_abiertos:
                self.max_abiertos = len(abiertos)

            if nodoActual.depth <= cotaMax:
                if actual.esFinal():
                    solucion = True
                else:
                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)
                        if hijo.cubo.visualizar() not in cerrados.keys() or nodoActual.depth + 1 < cerrados[hijo.cubo.visualizar()]:
                            abiertos.append(NodoAcotado(hijo, nodoActual, operador, nodoActual.depth + 1))
                            cerrados[hijo.cubo.visualizar()] = nodoActual.depth + 1

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
        cota = 0
        self.nodos_explorados = 0
        self.max_abiertos = 0

        while True:
            acotada = BusquedaProfundidadAcotada()
            solucion = acotada.buscarSolucion(inicial, cota)
            self.nodos_explorados += acotada.nodos_explorados
            if acotada.max_abiertos > self.max_abiertos:
                self.max_abiertos = acotada.max_abiertos

            if solucion is not None:
                return solucion

            cota += 1


class BusquedaVoraz(Busqueda):

    def __init__(self, heuristica_fn=heuristica_mal_colocadas):
        self.heuristica_fn = heuristica_fn

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        self.nodos_explorados = 0
        self.max_abiertos = 0

        abiertos.append(NodoVoraz(inicial, None, None, self.heuristica_fn))
        cerrados[inicial.cubo.visualizar()] = inicial

        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            self.nodos_explorados += 1
            if len(abiertos) > self.max_abiertos:
                self.max_abiertos = len(abiertos)

            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoVoraz(hijo, nodoActual, operador, self.heuristica_fn))
                        cerrados[hijo.cubo.visualizar()] = hijo
                abiertos.sort(key=lambda x: x.heuristica)

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:
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
        self.nodos_explorados = 0
        self.max_abiertos = 0

        h0 = self.heuristica(inicial)
        nodoInicial = NodoAEstrella(inicial, None, None, 0, h0)
        abiertos.append(nodoInicial)
        cerrados[inicial.cubo.visualizar()] = 0

        while len(abiertos) > 0:
            nodoActual = min(abiertos, key=lambda x: x.f)
            abiertos.remove(nodoActual)
            actual = nodoActual.estado
            self.nodos_explorados += 1
            if len(abiertos) > self.max_abiertos:
                self.max_abiertos = len(abiertos)

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


class BusquedaIDAEstrella(Busqueda):

    def __init__(self, heuristica_fn=heuristica_mal_colocadas):
        self.heuristica_fn = heuristica_fn

    def heuristica(self, estado):
        return self.heuristica_fn(estado)

    def buscarSolucion(self, inicial):
        cota = self.heuristica(inicial)
        self.nodos_explorados = 0
        self.max_abiertos = 0

        while True:
            solucion = self.busqueda_acotada(inicial, cota)

            if solucion is not None:
                return solucion

            cota += 1

    def busqueda_acotada(self, inicial, cotaMax):
        abiertos = []
        abiertos.append(NodoAcotado(inicial, None, None, 0))

        while len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            self.nodos_explorados += 1
            if len(abiertos) > self.max_abiertos:
                self.max_abiertos = len(abiertos)

            if actual.esFinal():
                lista = []
                nodo = nodoActual
                while nodo.padre is not None:
                    lista.insert(0, nodo.operador)
                    nodo = nodo.padre
                return lista

            g_actual = nodoActual.depth
            f_actual = g_actual + self.heuristica(actual)

            if f_actual <= cotaMax:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    nuevoNodo = NodoAcotado(hijo, nodoActual, operador, g_actual + 1)
                    abiertos.append(nuevoNodo)

        return None


<<<<<<< HEAD
class BusquedaAEstrellaWeighted(Busqueda):

    W = 1.5

    def __init__(self, heuristica_fn=heuristica_mal_colocadas):
        self.heuristica_fn = heuristica_fn

    def heuristica(self, estado):
        return self.heuristica_fn(estado)

    def buscarSolucion(self, inicial):
        abiertos = []
        cerrados = dict()
        self.nodos_explorados = 0
        self.max_abiertos = 0

        h0 = self.heuristica(inicial)
        nodoInicial = NodoAEstrella(inicial, None, None, g=0, h=self.W * h0)
        abiertos.append(nodoInicial)
        cerrados[inicial.cubo.visualizar()] = 0

        while len(abiertos) > 0:
            nodoActual = min(abiertos, key=lambda x: x.f)
            abiertos.remove(nodoActual)
            actual = nodoActual.estado
            self.nodos_explorados += 1
            if len(abiertos) > self.max_abiertos:
                self.max_abiertos = len(abiertos)
=======
    # -------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------
    def buscarSolucion(self, inicial):
        limite = self.heuristica(inicial)

        while True:
            resultado = self._busqueda(inicial, 0, limite, None, None)

            if isinstance(resultado, list):
                return resultado

            if resultado == float('inf'):
                return None

            limite = resultado


    # -------------------------------
    # BÚSQUEDA RECURSIVA (IDA*)
    # -------------------------------
    def _busqueda(self, estado, g, limite, padre, operador):

        f = g + self.heuristica(estado)

        # poda por límite
        if f > limite:
            return f

        # objetivo
        if estado.esFinal():
            return self._reconstruir_camino(padre, operador)

        minimo = float('inf')

        for op in estado.operadoresAplicables():

            # evitar deshacer movimiento
            if operador is not None and self._es_inverso(op, operador):
                continue

            # evitar repetir misma cara
            if operador is not None and (op.movimiento % 6 == operador.movimiento % 6):
                continue

            hijo = estado.aplicarOperador(op)

            resultado = self._busqueda(hijo, g + 1, limite, (padre, operador), op)

            if isinstance(resultado, list):
                return resultado

            if resultado < minimo:
                minimo = resultado

        return minimo


    # -------------------------------
    # DETECTAR MOVIMIENTO INVERSO
    # -------------------------------
    def _es_inverso(self, m1, m2):
        return abs(m1.movimiento - m2.movimiento) == 6


    # -------------------------------
    # RECONSTRUIR CAMINO
    # -------------------------------
    def _reconstruir_camino(self, padre_info, operador_final):
        lista = []

        if operador_final is not None:
            lista.insert(0, operador_final)

        while padre_info is not None:
            padre, op = padre_info
            if op is not None:
                lista.insert(0, op)
            padre_info = padre

        return lista
    class BusquedaAEstrellaWeighted(Busqueda):

        W = 1.5

        def heuristica(self, estado):
            return 0

        def buscarSolucion(self, inicial):

            abiertos = []
            cerrados = dict()

            h0 = self.heuristica(inicial)
            nodoInicial = NodoAEstrella(inicial, None, None, g=0, h=self.W * h0)

            abiertos.append(nodoInicial)
            cerrados[inicial.cubo.visualizar()] = 0
>>>>>>> parent of 2530a41 (CAMBIO)

            while len(abiertos) > 0:

                nodoActual = min(abiertos, key=lambda x: x.f)
                abiertos.remove(nodoActual)

<<<<<<< HEAD
                if id_hijo not in cerrados or g_hijo < cerrados[id_hijo]:
                    cerrados[id_hijo] = g_hijo
                    h_hijo = self.heuristica(hijo_estado)
                    nodoHijo = NodoAEstrella(hijo_estado, nodoActual, operador, g_hijo, self.W * h_hijo)
                    abiertos.append(nodoHijo)
=======
                actual = nodoActual.estado
>>>>>>> parent of 2530a41 (CAMBIO)

                if actual.esFinal():
                    return self.reconstruir(nodoActual)

                for operador in actual.operadoresAplicables():

                    hijo_estado = actual.aplicarOperador(operador)
                    g_hijo = nodoActual.g + 1
                    id_hijo = hijo_estado.cubo.visualizar()

                    if id_hijo not in cerrados or g_hijo < cerrados[id_hijo]:

                        h_hijo = self.heuristica(hijo_estado)
                        nodoHijo = NodoAEstrella(hijo_estado, nodoActual, operador, g=g_hijo, h=self.W * h_hijo)

                        abiertos.append(nodoHijo)
                        cerrados[id_hijo] = g_hijo

            return None

        def reconstruir(self, nodo):
            lista = []
            while nodo.padre is not None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista