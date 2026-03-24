from nodos import *


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

    def heuristica(self, estado):
        return 0  # o tu heurística del cubo


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

                    h_hijo = self.heuristica(hijo_estado)
                    nodoHijo = NodoAEstrella(hijo_estado, nodoActual, operador, g_hijo, h_hijo)

                    abiertos.append(nodoHijo)
                    cerrados[id_hijo] = g_hijo

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
        
        # 1. Creamos el nodo raíz con profundidad (depth) 0
        # Usamos tu clase NodoAcotado
        abiertos.append(NodoAcotado(inicial, None, None, 0))
        
        while not solucion and len(abiertos) > 0:
            # 2. LIFO: pop() saca el último elemento (comportamiento de Pila)
            # Esto es lo que define a la búsqueda en Profundidad
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            
            # 3. Verificamos si el estado del cubo es el objetivo
            if actual.esFinal():
                solucion = True
            else:
                # 4. GESTIÓN DE LA COTA:
                # Si el nodo actual tiene una profundidad menor que la cota, expandimos
                if nodoActual.depth < cotaMax:
                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)
                        
                        # 5. Creamos el nodo hijo aumentando la profundidad en 1
                        # Pasamos: estado, padre, operador, depth
                        nuevoNodo = NodoAcotado(hijo, nodoActual, operador, nodoActual.depth + 1)
                        abiertos.append(nuevoNodo)
        
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
            solucion = self.busqueda_acotada(inicial, cota)
            
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
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()

        # a�adir ESTADO_INICIAL a ABIERTOS
        abiertos.append(NodoVoraz(inicial, None, None))

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
                        abiertos.append(NodoVoraz(hijo, nodoActual, operador))
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

    # -------------------------------
    # HEURÍSTICA (puedes mejorarla luego)
    # -------------------------------
    def heuristica(self, estado):
        mal = 0
        for cara in estado.cubo.caras:
            for casilla in cara.casillas:
                if casilla.color != cara.color:
                    mal += 1
        return mal // 8


    # -------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------
    def buscarSolucion(self, inicial):
        limite = self.heuristica(inicial)

        while True:
            resultado = self._busqueda(inicial, 0, limite, None, None)

            # Si devuelve lista → solución encontrada
            if isinstance(resultado, list):
                return resultado

            # Si no hay solución
            if resultado == float('inf'):
                return None

            # Nueva cota
            limite = resultado


    # -------------------------------
    # BÚSQUEDA RECURSIVA (IDA*)
    # -------------------------------
    def _busqueda(self, estado, g, limite, padre, operador):
        f = g + self.heuristica(estado)

        if f > limite:
            return f

        if estado.esFinal():
            return self._reconstruir_camino(padre, operador)

        minimo = float('inf')

        for op in estado.operadoresAplicables():

            # Evitar deshacer el último movimiento
            if operador is not None and self._es_inverso(op, operador):
                continue

            hijo = estado.aplicarOperador(op)

            resultado = self._busqueda(hijo, g + 1, limite, (padre, operador), op)

            if isinstance(resultado, list):
                return resultado

            if resultado < minimo:
                minimo = resultado

        return minimo


    # -------------------------------
    # EVITAR MOVIMIENTO INVERSO
    # -------------------------------
    def _es_inverso(self, m1, m2):
        return (m1 == m2 + 6) or (m2 == m1 + 6)


    # -------------------------------
    # RECONSTRUIR SOLUCIÓN
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