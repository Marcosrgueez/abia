# Interfaz base para representar estados dentro de un problema de búsqueda
from abc import abstractmethod
from abc import ABCMeta


class Estado(metaclass=ABCMeta):
    # Devuelve la lista de operadores que se pueden aplicar en este estado
    @abstractmethod
    def operadoresAplicables(self):
        pass

    # Indica si este estado ya es solución (estado final)
    @abstractmethod
    def esFinal(self):
        pass

    # Genera un nuevo estado al aplicar un operador sobre el estado actual
    @abstractmethod
    def aplicarOperador(self,operador):
        pass


# Interfaz base para representar operadores (acciones)
class Operador(metaclass=ABCMeta):
    # Devuelve el nombre o etiqueta del operador
    @abstractmethod
    def getEtiqueta(self):
        pass

    # Devuelve el coste de aplicar el operador
    @abstractmethod
    def getCoste(self):
        pass


# Clase genérica que representa un problema de búsqueda.
# Tiene un estado inicial y un algoritmo de búsqueda asociado.
class Problema:
    def __init__(self,inicial,buscador):
        self.inicial=inicial
        self.buscador=buscador

    # Ejecuta el algoritmo de búsqueda para resolver el problema.
    # Devuelve la secuencia de operadores que llevan desde el estado inicial a uno final.
    def obtenerSolucion(self):
        return self.buscador.buscarSolucion(self.inicial)