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



