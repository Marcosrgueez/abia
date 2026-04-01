import sys
import time
from cubo import Cubo
from problemaRubik import Problema, EstadoRubik
from busqueda import *
from heuristicas import heuristica_mal_colocadas, heuristica_cruz_up

def ejecutar_test():
    # Inicialización del cubo
    mi_cubo = Cubo()
    
    print("ESTADO INICIAL (ORDENADO):")
    print(mi_cubo.visualizar())

    # Aplicamos un movimiento de prueba inicial
    mi_cubo.mover(mi_cubo.F)
    print("ESTADO TRAS MOVIMIENTO 'F':")
    print(mi_cubo.visualizar())

    # Configuración de la mezcla desde argumentos de consola
    num_movimientos = int(sys.argv[1])
    secuencia_mezcla = mi_cubo.mezclar(num_movimientos)

    print(f"MEZCLA ALEATORIA DE {num_movimientos} PASOS:")
    for m in secuencia_mezcla:
        print(mi_cubo.visualizarMovimiento(m), end=" ")
    print("\n")

    print("ESTADO DEL CUBO MEZCLADO:")
    print(mi_cubo.visualizar())

    # Gestión de heurísticas con un mapeo alternativo
    mapa_h = {
        "mal": heuristica_mal_colocadas,
        "cruz": heuristica_cruz_up
    }

    # Selección de heurística por argumento o por defecto
    h_elegida = heuristica_mal_colocadas
    if len(sys.argv) > 2:
        h_elegida = mapa_h.get(sys.argv[2], heuristica_mal_colocadas)

    # Configuración del motor de búsqueda y el problema
    algoritmo = BusquedaAEstrellaWeighted(h_elegida)
    rubik_solver = Problema(EstadoRubik(mi_cubo), algoritmo)

    # Proceso de resolución y cronometraje
    t_inicio = time.time()
    print("--- BUSCANDO SOLUCIÓN ---")
    ruta_solucion = rubik_solver.obtenerSolucion()
    t_final = time.time()

    # Reporte de métricas
    print(f"Cronómetro: {round(t_final - t_inicio, 4)} seg.")
    print(f"Nodos visitados: {algoritmo.nodos_explorados}")
    print(f"Pico de nodos en frontera: {algoritmo.max_abiertos}")

    if ruta_solucion is not None:
        print(f"Longitud de la ruta: {len(ruta_solucion)}")
        print("PASOS A SEGUIR:")
        for paso in ruta_solucion:
            etiqueta = paso.getEtiqueta()
            print(mi_cubo.visualizarMovimiento(etiqueta), end=" ")
            mi_cubo.mover(paso.movimiento)
        
        print("\n\nRESULTADO FINAL:")
        print(mi_cubo.visualizar())
    else:
        print("No se logró hallar una solución para este estado.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python nombre_archivo.py <num_mezclas> [heuristica]")
    else:
        ejecutar_test()
