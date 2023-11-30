
class Ambulancia:
    def __init__(self, celdaX: int, celdaY: int,):
        self.pacientesN = 0
        self.pacientesC = 0
        self.celdaX = celdaX
        self.celdaY = celdaY
        self.energia_left = 50

    def recargar_energia(self):
        self.energia_left = 50

    def recoger_paciente(self, celda_ambulancia):
        if celda_ambulancia == 'N':
            if self.pacientesN + self.pacientesC < 10:
                self.pacientesN += 1
        else:
            if self.pacientesC < 2:
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

