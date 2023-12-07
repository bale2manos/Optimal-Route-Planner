ENERGY_REFILL = 50
class Ambulancia:
    def __init__(self, celdaX: int, celdaY: int, ):
        self.pacientesN = 0
        self.pacientesC = 0
        self.celdaX = celdaX
        self.celdaY = celdaY
        self.energia_left = ENERGY_REFILL

    def __eq__(self, other):
        return (self.celdaX, self.celdaY, self.energia_left, self.pacientesN, self.pacientesC) == (
        other.celdaX, other.celdaY, other.energia_left, other.pacientesN, other.pacientesC)

    def __str__(self):
        return f"({self.celdaX}, {self.celdaY}): {self.energia_left}, {self.pacientesN}, {self.pacientesC}"

    def __hash__(self):
        return hash((self.celdaX, self.celdaY, self.energia_left, self.pacientesN, self.pacientesC))

    def recargar_energia(self):
        self.energia_left = 50

    def recoger_paciente(self, celda_ambulancia):
        if celda_ambulancia == 'N':
            self.pacientesN += 1
        else:
            self.pacientesC += 1

    def descargar_pacientes(self, celda_ambulancia):
        if celda_ambulancia == 'CN':
            self.pacientesN = 0
        else:
            self.pacientesC = 0

    def mover_a(self, celda, nueva_energia):
        self.celdaX = celda.fila
        self.celdaY = celda.columna
        self.energia_left = nueva_energia
