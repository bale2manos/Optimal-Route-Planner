class Celda:
    def __init__(self, fila: int, columna: int, valor: str):
        self.fila = fila
        self.columna = columna
        self.tipo = valor
        if self.tipo == '1' or self.tipo == '2':
            self.coste = int(self.tipo)
        else:
            self.coste = 1

    def __str__(self):
        return f"({self.fila}, {self.columna}): {self.tipo}"

    def __hash__(self):
        return hash((self.fila, self.columna, self.tipo))

    def __eq__(self, other):
        return (self.fila, self.columna, self.tipo) == (other.fila, other.columna, other.tipo)


from queue import PriorityQueue


class Nodo:
    def __init__(self, mapa, coste_acumulado, heuristica, camino_recorrido):
        self.mapa = mapa
        self.coste_acumulado = coste_acumulado
        self.heuristica = heuristica
        self.prioridad = coste_acumulado + heuristica  # f(n) = g(n) + h(n)
        self.camino_recorrido = camino_recorrido  # Nueva variable para almacenar el camino

    def __eq__(self, other):
        if not isinstance(other, Nodo):
            return False

        return self.mapa == other.mapa

    def __hash__(self):
        celdas = ''
        for celda in self.mapa.celdas:
            celdas += str(celda) + ';'
        ambulancia = str(self.mapa.ambulancia)
        return hash(celdas + 'Ambulance: ' + ambulancia)

    def __lt__(self, other):
        return self.prioridad < other.prioridad

    def __str__(self):
        celdas = ''
        for celda in self.mapa.celdas:
            celdas += str(celda) + ';'
        ambulancia = str(self.mapa.ambulancia)
        return celdas + 'Ambulance: ' + ambulancia



