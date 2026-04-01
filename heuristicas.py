def _extraer_cubo(estado_o_cubo):
    if hasattr(estado_o_cubo, "cubo"):
        return estado_o_cubo.cubo
    return estado_o_cubo


def heuristica_mal_colocadas(estado_cubo):
    cubo = _extraer_cubo(estado_cubo)
    mal = 0
    for cara in cubo.caras:
        for i, casilla in enumerate(cara.casillas):
            if i == 8:
                continue
            if casilla.color != cara.color:
                mal += 1
    return mal




def heuristica_cruz_up(estado_cubo):
    cubo = _extraer_cubo(estado_cubo)
    cara_up = cubo.caras[0]
    indices_aristas = [1, 3, 5, 7]
    aciertos = 0
    for idx in indices_aristas:
        if cara_up.casillas[idx].color == cara_up.color:
            aciertos += 1
    return 4 - aciertos
