import sys
from cubo import *
from problemaRubik import *
from busqueda import *
from heuristicas import heuristica_mal_colocadas, heuristica_cruz_up




cubo = Cubo()

print("CUBO INICIAL SIN MEZCLAR:\n" + cubo.visualizar())


#Mover frontal face
cubo.mover(cubo.F)

print("CUBO resultado del movimiento F:\n" + cubo.visualizar())

movs=int(sys.argv[1])

heuristicas = {
    "mal": heuristica_mal_colocadas,
    "cruz": heuristica_cruz_up
}

heuristica = heuristica_mal_colocadas
if len(sys.argv) > 2:
    heuristica = heuristicas.get(sys.argv[2], heuristica_mal_colocadas)

movsMezcla = cubo.mezclar(movs)

print("MOVIMIENTOS ALEATORIOS:",movs)
for m in movsMezcla:
    print(cubo.visualizarMovimiento(m) + " ")
print()

print("CUBO INICIAL (MEZCLADO):\n" + cubo.visualizar())





#Creación de un problema
problema = Problema(EstadoRubik(cubo), BusquedaAEstrellaWeighted(heuristica))


print("SOLUCION:")
opsSolucion = problema.obtenerSolucion()

if opsSolucion != None:
    for o in opsSolucion:
        print(cubo.visualizarMovimiento(o.getEtiqueta()) + " ")
        cubo.mover(o.movimiento)
    print()
    print("CUBO FINAL:\n" + cubo.visualizar())
else:
    print("no se ha encontrado solución")


