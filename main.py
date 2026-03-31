import sys
from cubo import *
from problemaRubik import *
from busqueda import *
from heuristicas import heuristica_mal_colocadas, heuristica_cruz_up
import time


cubo = Cubo()

print("CUBO INICIAL SIN MEZCLAR:\n" + cubo.visualizar())

movs = int(sys.argv[1])

heuristicas = {
    "mal": heuristica_mal_colocadas,
    "cruz": heuristica_cruz_up
}

heuristica = heuristica_mal_colocadas
if len(sys.argv) > 2:
    heuristica = heuristicas.get(sys.argv[2], heuristica_mal_colocadas)

movsMezcla = cubo.mezclar(movs)

print("MOVIMIENTOS ALEATORIOS:", movs)
for m in movsMezcla:
    print(cubo.visualizarMovimiento(m) + " ")
print()

print("CUBO INICIAL (MEZCLADO):\n" + cubo.visualizar())


# Creación de un problema
busqueda = BusquedaVoraz(heuristica)
problema = Problema(EstadoRubik(cubo), busqueda)

inicio = time.time()
print("SOLUCION:")
opsSolucion = problema.obtenerSolucion()
fin = time.time()

print("Tiempo:", fin - inicio, "segundos")

if opsSolucion != None:
    print("Longitud solucion:", len(opsSolucion))

    # métricas nuevas
    print("Nodos explorados:", busqueda.nodos_explorados)
    print("Max abiertos:", busqueda.max_abiertos)

    for o in opsSolucion:
        print(cubo.visualizarMovimiento(o.getEtiqueta()) + " ")
        cubo.mover(o.movimiento)

    print()
    print("CUBO FINAL:\n" + cubo.visualizar())
else:
    print("no se ha encontrado solución")