from queue import PriorityQueue

class Nodo:
    def __init__(self, mapa, coste_acumulado, prioridad, camino_recorrido, accion_previa, numero_nodo):
        self.mapa = mapa
        self.coste_acumulado = coste_acumulado
        self.prioridad = prioridad                   # f(n) = g(n) + h(n)
        self.camino_recorrido = camino_recorrido  # Nueva variable para almacenar el camino
        self.numero_nodo = numero_nodo
        self.accion_previa = accion_previa

    def __lt__(self, other):
        return self.prioridad < other.prioridad

    def __str__(self):
        return "Coste acumulado: " + str(self.coste_acumulado) + " Prioridad: " + str(self.prioridad)