class IDAStar:
    
    def __init__(self):
        pass


    # -------------------------------
    # HEURÍSTICA
    # -------------------------------
    def heuristica(self, cubo):
        mal = 0
        for cara in cubo.caras:
            for casilla in cara.casillas:
                if casilla.color != cara.color:
                    mal += 1
        return mal // 8  # aproximación


    # -------------------------------
    # MOVIMIENTO INVERSO
    # -------------------------------
    def es_inverso(self, m1, m2):
        return (m1 == m2 + 6) or (m2 == m1 + 6)


    # -------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------
    def resolver(self, cubo):
        limite = self.heuristica(cubo)

        while True:
            print("Límite actual:", limite)

            resultado = self._busqueda(cubo, 0, limite, [])

            if isinstance(resultado, list):
                return resultado

            if resultado == float('inf'):
                return None

            limite = resultado


    # -------------------------------
    # BÚSQUEDA RECURSIVA (IDA*)
    # -------------------------------
    def _busqueda(self, cubo, g, limite, camino):
        f = g + self.heuristica(cubo)

        if f > limite:
            return f

        if cubo.esConfiguracionFinal():
            return camino

        minimo = float('inf')

        for mov in Cubo.movimientosPosibles:

            # Evitar deshacer el último movimiento
            if len(camino) > 0 and self.es_inverso(mov, camino[-1]):
                continue

            nuevo = cubo.clonar()
            nuevo.mover(mov)

            resultado = self._busqueda(nuevo, g + 1, limite, camino + [mov])

            if isinstance(resultado, list):
                return resultado

            if resultado < minimo:
                minimo = resultado

        return minimo