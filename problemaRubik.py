from problema import *
from cubo import *
from heuristicas import heuristica_mal_colocadas


# Clase que representa un estado concreto del cubo de Rubik dentro del problema de búsqueda.
# Básicamente es un "wrapper" del objeto Cubo para adaptarlo a la interfaz Estado.
class EstadoRubik(Estado):

    def __init__(self, cubo):
        
        # Generamos todos los operadores posibles (todos los movimientos del cubo)
        self.listaOperadoresAplicables=[]
        for m in Cubo.movimientosPosibles:
            self.listaOperadoresAplicables.append(OperadorRubik(m))

        # Guardamos el cubo actual
        self.cubo=cubo


    # Devuelve todos los movimientos que se pueden aplicar desde este estado
    def operadoresAplicables(self):
        return self.listaOperadoresAplicables


    # Comprueba si el cubo ya está resuelto
    def esFinal(self):
        return self.cubo.esConfiguracionFinal()

    # Aplica un movimiento y devuelve un nuevo estado (sin modificar el original)
    def aplicarOperador(self,o):
        nuevo=self.cubo.clonar()
        nuevo.mover(o.movimiento)
        return EstadoRubik(nuevo)

    # Compara si dos estados son iguales (comparando sus cubos)
    def equals(self,e):
        return self.cubo.equals(e.cubo)

    # Calcula el valor heurístico del estado (para algoritmos como A*)
    def heuristica(self):
        return heuristica_mal_colocadas(self)


# Clase que representa un operador concreto (un giro del cubo)
class OperadorRubik(Operador):
    def __init__(self, movimiento):
        self.movimiento=movimiento

    # Devuelve el identificador del movimiento
    def getEtiqueta(self):
        return self.movimiento

    # Todos los movimientos cuestan lo mismo (coste uniforme = 1)
    def getCoste(self):
        return 1