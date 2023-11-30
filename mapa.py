import copy

from celda import Celda
from ambulancia import Ambulancia
from nodo import Nodo
from queue import PriorityQueue

class Mapa:
    def __init__(self, archivo):
        self.pacientes_restantes = 0
        self.max_rows = 0
        self.max_columns = 0
        self.celdas = self.cargar_mapa(archivo)
        self.acciones_posibles = ['recargar_energia', 'recoger_paciente', 'descargar_pacientes', 'mover_arriba', 'mover_abajo', 'mover_izquierda', 'mover_derecha']
        self.ambulancia = self.crear_ambulancia()

    def mostrar_mapa(self):
        for celda in self.celdas:
            print(celda.tipo, end='')

    def cargar_mapa(self, archivo):
        with open(archivo, 'r') as file:
            mapa = [line.strip().split(';') for line in file.readlines()]

        celdas = []
        self.max_rows = len(mapa)
        self.max_columns = len(mapa[0])
        for fila in range(len(mapa)):
            for columna in range(len(mapa[fila])):
                celdas.append(Celda(fila+1, columna+1, mapa[fila][columna]))
                if mapa[fila][columna] == 'N' or mapa[fila][columna] == 'C':
                    self.pacientes_restantes += 1

        return celdas

    def crear_ambulancia(self):
        for celda in self.celdas:
            if celda.tipo == 'P':
                return Ambulancia(celda.fila, celda.columna)

    def get_celda(self, fila, columna):
        if fila < 1 or fila > self.max_rows or columna < 1 or columna > self.max_columns:
            return None # Celda fuera de los límites del mapa

        return self.celdas[(fila-1)*self.max_columns + (columna-1)]

    def recargar_energia(self):
        ambulanciaX = self.ambulancia.celdaX
        ambulanciaY = self.ambulancia.celdaY
        if self.get_celda(ambulanciaX, ambulanciaY).tipo == 'P' and self.ambulancia.energia_left < 50:
            self.ambulancia.recargar_energia()
            return 0
        return -1

    def recoger_paciente(self):
        ambulanciaX = self.ambulancia.celdaX
        ambulanciaY = self.ambulancia.celdaY
        celda_ambulancia = self.get_celda(ambulanciaX, ambulanciaY)

        if celda_ambulancia.tipo == 'N' or celda_ambulancia.tipo == 'C':
            self.ambulancia.recoger_paciente(celda_ambulancia.tipo)
            celda_ambulancia.tipo = '1'
            self.pacientes_restantes -= 1
            return 0
        return -1

    def descargar_pacientes(self):
        ambulanciaX = self.ambulancia.celdaX
        ambulanciaY = self.ambulancia.celdaY
        celda_ambulancia = self.get_celda(ambulanciaX, ambulanciaY)

        if (celda_ambulancia.tipo == 'CC' and self.ambulancia.pacientesC > 0) or (celda_ambulancia.tipo == 'CN' and self.ambulancia.pacientesN > 0):
            self.ambulancia.descargar_pacientes(celda_ambulancia.tipo)
            return 0
        return -1

    def mover_arriba(self):
        ambulanciaX = self.ambulancia.celdaX
        ambulanciaY = self.ambulancia.celdaY
        celda_arriba = self.get_celda(ambulanciaX-1, ambulanciaY)
        if celda_arriba:
            potencial_energia_restante = self.ambulancia.energia_left - celda_arriba.coste
            if celda_arriba.tipo != 'X' and potencial_energia_restante >= 0:
                self.ambulancia.mover_a(celda_arriba, potencial_energia_restante)
                return celda_arriba.coste
        return -1

    def mover_abajo(self):
        ambulanciaX = self.ambulancia.celdaX
        ambulanciaY = self.ambulancia.celdaY
        celda_abajo = self.get_celda(ambulanciaX+1, ambulanciaY)
        if celda_abajo:
            potencial_energia_restante = self.ambulancia.energia_left - celda_abajo.coste
            if celda_abajo.tipo != 'X' and potencial_energia_restante >= 0:
                self.ambulancia.mover_a(celda_abajo, potencial_energia_restante)
                return celda_abajo.coste
        return -1

    def mover_izquierda(self):
        ambulanciaX = self.ambulancia.celdaX
        ambulanciaY = self.ambulancia.celdaY
        celda_izquierda = self.get_celda(ambulanciaX, ambulanciaY-1)
        if celda_izquierda:
            potencial_energia_restante = self.ambulancia.energia_left - celda_izquierda.coste
            if celda_izquierda.tipo != 'X' and potencial_energia_restante >= 0:
                self.ambulancia.mover_a(celda_izquierda, potencial_energia_restante)
                return celda_izquierda.coste
        return -1

    def mover_derecha(self):
        ambulanciaX = self.ambulancia.celdaX
        ambulanciaY = self.ambulancia.celdaY
        celda_derecha = self.get_celda(ambulanciaX, ambulanciaY+1)
        if celda_derecha:
            potencial_energia_restante = self.ambulancia.energia_left - celda_derecha.coste
            if celda_derecha.tipo != 'X' and potencial_energia_restante >= 0:
                self.ambulancia.mover_a(celda_derecha, potencial_energia_restante)
                return celda_derecha.coste
        return -1

    def a_estrella(self, heuristica):
        inicio = copy.deepcopy(self)
        cola_prioridad = PriorityQueue()
        cola_prioridad.put(Nodo(inicio, 0, 0, [inicio], 'Inicio', 0))
        costos_acumulados = {inicio: 0}
        i = 1
        while not cola_prioridad.empty():
            nodo_actual = cola_prioridad.get()


            print('Nodo actual: ', i, ' - ', nodo_actual.accion_previa, ' - ', nodo_actual.mapa.pacientes_restantes)
            print('Coste acumulado: ', nodo_actual.coste_acumulado)
            print('Heuristica: ', self.calcular_heuristica(nodo_actual.mapa, 1))
            print('Prioridad: ', nodo_actual.prioridad)
            print('Ambulancia: ', nodo_actual.mapa.ambulancia.celdaX, nodo_actual.mapa.ambulancia.celdaY, ' energía - ', nodo_actual.mapa.ambulancia.energia_left)



            if self.objetivo_cumplido(nodo_actual):
                # Reconstruir el camino y devolverlo
                return nodo_actual.camino_recorrido

            for accion, nuevo_estado, coste_accion in self.obtener_sucesores_y_coste(nodo_actual):
                nuevo_coste_acumulado = nodo_actual.coste_acumulado + coste_accion
                if nuevo_estado not in costos_acumulados or nuevo_coste_acumulado < costos_acumulados[nuevo_estado]:
                    costos_acumulados[nuevo_estado] = nuevo_coste_acumulado
                    heuristica = self.calcular_heuristica(nuevo_estado, heuristica)
                    prioridad = nuevo_coste_acumulado + heuristica
                    nuevo_camino = nodo_actual.camino_recorrido + [nuevo_estado]
                    cola_prioridad.put(Nodo(nuevo_estado, nuevo_coste_acumulado, prioridad, nuevo_camino, accion, i))
            i += 1

        # No hay camino posible
        return None

    def obtener_sucesores_y_coste(self, nodo):
        # Devuelve las acciones posibles y los nuevos estados alcanzables desde el estado dado
        # Puedes modificar esto según tu implementación específica
        acciones_y_sucesores = []
        for accion in self.acciones_posibles:
            # crear una copia en cada iteracion del nodo, que no se modificara en la siguiente iteracion
            nuevo_mapa = copy.deepcopy(nodo.mapa)
            coste_accion = -1

            if accion == 'recargar_energia':
                coste_accion = nuevo_mapa.recargar_energia()
            elif accion == 'recoger_paciente':
                coste_accion = nuevo_mapa.recoger_paciente()
            elif accion == 'descargar_pacientes':
                coste_accion = nuevo_mapa.descargar_pacientes()
            elif accion == 'mover_arriba':
                coste_accion = nuevo_mapa.mover_arriba()
            elif accion == 'mover_abajo':
                coste_accion = nuevo_mapa.mover_abajo()
            elif accion == 'mover_izquierda':
                coste_accion = nuevo_mapa.mover_izquierda()
            elif accion == 'mover_derecha':
                coste_accion = nuevo_mapa.mover_derecha()

            if coste_accion != -1:
                acciones_y_sucesores.append((accion, nuevo_mapa, coste_accion))

        return acciones_y_sucesores

    def calcular_heuristica(self, estado_actual, heuristica):
        #if heuristica == 1:
            # Calcula la heurística según el número de pacientes restantes
            pacientes_restantes = estado_actual.pacientes_restantes + estado_actual.ambulancia.pacientesN + estado_actual.ambulancia.pacientesC
            return pacientes_restantes

    def objetivo_cumplido(self, nodo):
        # Verifica si el estado cumple con el objetivo
        pacientes_restantes = nodo.mapa.pacientes_restantes
        pacientes_en_ambulancia = nodo.mapa.ambulancia.pacientesN + nodo.mapa.ambulancia.pacientesC
        return pacientes_restantes == 0 and pacientes_en_ambulancia == 0



