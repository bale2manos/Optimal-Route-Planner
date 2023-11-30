from queue import PriorityQueue

class Nodo:
    def __init__(self, mapa, coste_acumulado, prioridad, camino_recorrido):
        self.mapa = mapa
        self.coste_acumulado = coste_acumulado
        self.prioridad = prioridad
        self.camino_recorrido = camino_recorrido  # Nueva variable para almacenar el camino

    def __lt__(self, other):
        return self.prioridad < other.prioridad