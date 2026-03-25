def _extraer_cubo(estado_o_cubo):
    if hasattr(estado_o_cubo, "cubo"):
        return estado_o_cubo.cubo
    return estado_o_cubo


def heuristica_mal_colocadas(estado_o_cubo):
    cubo = _extraer_cubo(estado_o_cubo)
    mal = 0
    for cara in cubo.caras:
        for i, casilla in enumerate(cara.casillas):
            if i == 8:
                continue
            if casilla.color != cara.color:
                mal += 1
    return mal


def heuristica_cero(estado_o_cubo):
    return 0
