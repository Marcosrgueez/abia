from nodos import *


from abc import abstractmethod
from abc import ABCMeta


#Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass

##hola caracola



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
        abiertos.append(NodoProfundidad(inicial, None, None))
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
    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoVoraz(inicial, None, None))
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
                        abiertos.append(NodoVoraz(hijo, nodoActual, operador))
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

    # h(n). Si no tienes heurística todavía, devuelve 0
    def heuristica(self, estado):
        return 0

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False

        abiertos = []
        cerrados = dict()

        # En A*: cerrados guarda el mejor coste g de cada estado
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()] = 0

        while not solucion and len(abiertos) > 0:

            # Seleccionar el nodo de ABIERTOS con menor f = g + h
            nodoActual = abiertos[0]
            for nodo in abiertos[1:]:
                f_nodo = cerrados[nodo.estado.cubo.visualizar()] + self.heuristica(nodo.estado)
                f_actual = cerrados[nodoActual.estado.cubo.visualizar()] + self.heuristica(nodoActual.estado)
                if f_nodo < f_actual:
                    nodoActual = nodo

            abiertos.remove(nodoActual)
            actual = nodoActual.estado

            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    g_hijo = cerrados[actual.cubo.visualizar()] + 1  # coste por movimiento = 1

                    # Meter si es nuevo o si encontramos un camino mejor
                    if (hijo.cubo.visualizar() not in cerrados.keys()) or (g_hijo < cerrados[hijo.cubo.visualizar()]):
                        cerrados[hijo.cubo.visualizar()] = g_hijo
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None




