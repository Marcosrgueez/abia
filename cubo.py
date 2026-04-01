from random import *

seed(1010)

# Esta clase representa una cara del cubo de Rubik.
# Cada cara tiene un color (que coincide con su índice en el cubo)
# y contiene 9 casillas colocadas en forma de "espiral".
class Cara:
    def __init__(self, color):
        self.color=color
        self.casillas = []
        for i in range(0, 9):
            self.casillas.append(Casilla(color, i))

    # Comprueba si esta cara es igual a otra
    def equal(self, cara):
        for i,c in enumerate(cara):
            if c.color != self.casillas[i].color:
                return False
        return True


# Esta clase representa una casilla individual del cubo.
# Guarda el color actual y cuál sería su posición correcta en el estado final.
class Casilla:
    def __init__(self, color, pos):
        self.color=color
        self.posicionCorrecta=pos

    # Compara si dos casillas son exactamente iguales
    def equal(self,casilla):
        if self.color != casilla.color or self.posicionCorrecta != casilla.posicionCorrecta: return False
        return True


# Clase principal que representa todo el cubo de Rubik.
# Internamente guarda 6 caras, cada una con sus 9 casillas.
# También define constantes y estructuras auxiliares para saber
# cómo se relacionan las caras entre sí.
class Cubo:
    """

    Distribución de las caras:
       0
     1 2 3 4
       5
    
    Índices de las casillas en cada cara:
           012
           783
           654
     
      012  012  012  012
      783  783  783  783
      654  654  654  654
    
           012
           783    
           654
    """

    # Identificadores de las caras
    UP = 0
    LEFT = 1
    FRONT = 2
    RIGHT = 3
    BACK = 4
    DOWN = 5

    # Identificadores de colores
    ids_colores = [0, 1, 2, 3, 4, 5]

    # Etiquetas visuales de los colores
    etq_colores = ["W", "B", "O", "G", "R", "Y"]

    # Para cada cara, indicamos cuál es su vecina al norte
    vecinoNorte = [4, 0, 0, 0, 0, 2]

    # Vecinos al este
    vecinoEste  = [3, 2, 3, 4, 1, 3]

    # Vecinos al sur
    vecinoSur   = [2, 5, 5, 5, 5, 4]

    # Vecinos al oeste
    vecinoOeste = [1, 4, 1, 2, 3, 1]

    # Índices de las casillas que se mueven en cada giro (zona norte)
    idxNorte = [[2, 1, 0],
                [0, 7, 6],
                [6, 5, 4],
                [4, 3, 2],
                [2, 1, 0],
                [6, 5, 4]]

    # Zona este
    idxEste = [[2, 1, 0],
               [0, 7, 6],
               [0, 7, 6],
               [0, 7, 6],
               [0, 7, 6],
               [6, 5, 4]]

    # Zona sur
    idxSur = [[2, 1, 0],
              [0, 7, 6],
              [2, 1, 0],
              [4, 3, 2],
              [6, 5, 4],
              [6, 5, 4]]

    # Zona oeste
    idxOeste = [[2, 1, 0],
                [4, 3, 2],
                [4, 3, 2],
                [4, 3, 2],
                [4, 3, 2],
                [6, 5, 4]]

    # Definición de movimientos (horario y antihorario)
    U = UP
    Ui = U + 6
    L = LEFT
    Li = L + 6
    F = FRONT
    Fi = F + 6
    R = RIGHT
    Ri = R + 6
    B = BACK
    Bi = B + 6
    D = DOWN
    Di = D + 6

    movimientosPosibles = [U, Ui, L, Li, F, Fi, R, Ri, B, Bi, D, Di]

    # Representación corta de los movimientos
    etq_corta = ["U", "L", "F", "R", "B", "D","Ui", "Li", "Fi", "Ri", "Bi", "Di"]

    # Constructor: crea un cubo resuelto
    def __init__(self):
        self.caras=[]
        for i in range(0, 6):
            self.caras.append(Cara(i))

    # Crea una copia del cubo (para no modificar el original)
    def clonar(self):
        c=Cubo()
        for i in range(0,6):
            c.caras[i].color=self.caras[i].color
            for j in range(0,9): 
                c.caras[i].casillas[j].color=self.caras[i].casillas[j].color
        return c

    # Comprueba si el cubo está resuelto
    def esConfiguracionFinal(self):
        for c in self.caras:
            for n in c.casillas:
                if n.color != c.color:
                    return False
        return True

    # Mezcla el cubo con un número aleatorio de movimientos
    def mezclar(self):
        return self.mezclar(randint(0, 30))

    # Mezcla el cubo con un número concreto de movimientos
    def mezclar(self,pasos):
        listaMovs=[]
        for i in range(0, pasos):
            idMov = randint(0,len(self.movimientosPosibles)-1)
            self.mover(self.movimientosPosibles[idMov])
            listaMovs.append(self.movimientosPosibles[idMov])
        return listaMovs

    # Aplica un movimiento al cubo
    def mover(self,movimiento):
        if movimiento < 6:
            self.girarHorario(movimiento)
        else:
            self.girarAntiHorario(movimiento-6)

    # Aplica una lista de movimientos
    def moverListaMovs(self,listaMovimientos):
        for mov in listaMovimientos:
            self.mover(mov)

    # Giro en sentido horario (incluye caras vecinas)
    def girarHorario(self,idxCara):
        aux1 = None
        aux2 = None
        aux3 = None
        self.girarCaraHorario(self.caras[idxCara])
        for i in range(0,3):
            aux1 = self.caras[self.vecinoEste[idxCara]].casillas[self.idxEste[idxCara][i]]
            self.caras[self.vecinoEste[idxCara]].casillas[self.idxEste[idxCara][i]] = self.caras[self.vecinoNorte[idxCara]].casillas[self.idxNorte[idxCara][i]]

            aux2 = self.caras[self.vecinoSur[idxCara]].casillas[self.idxSur[idxCara][i]]
            self.caras[self.vecinoSur[idxCara]].casillas[self.idxSur[idxCara][i]] = aux1

            aux3 = self.caras[self.vecinoOeste[idxCara]].casillas[self.idxOeste[idxCara][i]]
            self.caras[self.vecinoOeste[idxCara]].casillas[self.idxOeste[idxCara][i]] = aux2

            self.caras[self.vecinoNorte[idxCara]].casillas[self.idxNorte[idxCara][i]] = aux3

    # Giro en sentido antihorario
    def girarAntiHorario(self,idxCara):
        aux1 = None
        aux2 = None
        aux3 = None
        self.girarCaraAntiHorario(self.caras[idxCara])
        for i in range(0,3):
            aux1 = self.caras[self.vecinoOeste[idxCara]].casillas[self.idxOeste[idxCara][i]]
            self.caras[self.vecinoOeste[idxCara]].casillas[self.idxOeste[idxCara][i]] = self.caras[self.vecinoNorte[idxCara]].casillas[self.idxNorte[idxCara][i]]

            aux2 = self.caras[self.vecinoSur[idxCara]].casillas[self.idxSur[idxCara][i]]
            self.caras[self.vecinoSur[idxCara]].casillas[self.idxSur[idxCara][i]] = aux1

            aux3 = self.caras[self.vecinoEste[idxCara]].casillas[self.idxEste[idxCara][i]]
            self.caras[self.vecinoEste[idxCara]].casillas[self.idxEste[idxCara][i]] = aux2

            self.caras[self.vecinoNorte[idxCara]].casillas[self.idxNorte[idxCara][i]] = aux3

    # Gira solo la cara (sin afectar a otras)
    def girarCaraHorario(self,cara):
        copia = []
        for c in cara.casillas:
            copia.append(c)
        for i in range(0,8):
            cara.casillas[(i+2)%8]=copia[i]

    # Giro antihorario de una cara
    def girarCaraAntiHorario(self,cara):
        copia = []
        for c in cara.casillas:
            copia.append(c)
        for i in range(0,8):
            cara.casillas[i]=copia[(i+2)%8]

    # Compara dos cubos completos
    def equals(self,cubo):
        for i in range(0,6):
            if not self.caras[i].equals(cubo.caras[i]):
                return False
        return True

    # Devuelve un string con el cubo dibujado
    def visualizar(self):
        resultado = "    " + self.stringFila1(self.caras[0]) + "\n" +"    " + self.stringFila2(self.caras[0]) + "\n" +"    " + self.stringFila3(self.caras[0]) + "\n\n"

        resultado += self.stringFila1(self.caras[1]) + " " + self.stringFila1(self.caras[2]) + " " + self.stringFila1(self.caras[3]) + " " + self.stringFila1(self.caras[4]) + "\n" + self.stringFila2(self.caras[1]) + " " + self.stringFila2(self.caras[2]) + " " +self.stringFila2(self.caras[3]) + " " + self.stringFila2(self.caras[4]) + "\n" +self.stringFila3(self.caras[1]) + " " + self.stringFila3(self.caras[2]) + " " +self.stringFila3(self.caras[3]) + " " + self.stringFila3(self.caras[4]) + "\n\n"

        resultado += "    " + self.stringFila1(self.caras[5]) + "\n" + "    " + self.stringFila2(self.caras[5]) + "\n" + "    " + self.stringFila3(self.caras[5]) + "\n\n"
        return resultado

    def  stringFila1(self,cara):
        return self.etq_colores[cara.casillas[0].color] + self.etq_colores[cara.casillas[1].color] + self.etq_colores[cara.casillas[2].color]

    def  stringFila2(self,cara):
        return self.etq_colores[cara.casillas[7].color] + self.etq_colores[cara.casillas[8].color] + self.etq_colores[cara.casillas[3].color]

    def  stringFila3(self,cara):
        return self.etq_colores[cara.casillas[6].color] + self.etq_colores[cara.casillas[5].color] + self.etq_colores[cara.casillas[4].color]

    # Devuelve el nombre corto del movimiento (U, R, etc.)
    def visualizarMovimiento(self,tipo):
        return self.etq_corta[tipo]