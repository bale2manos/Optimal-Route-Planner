class Celda:
    def __init__(self, fila: int, columna: int, valor: str):
        self.fila = fila
        self.columna = columna
        self.tipo = valor
        if self.tipo == '1' or self.tipo == '2':
            self.coste = int(self.tipo)
        else:
            self.coste = 1


