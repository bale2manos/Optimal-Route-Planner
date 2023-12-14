import csv
import sys
from mapa import Mapa
import time

def start_timer():
    return time.time()

def stop_timer(start_time):
    elapsed_time = time.time() - start_time
    return elapsed_time

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

def main():
    #timer start
    start_time = start_timer()


    if len(sys.argv) != 3:
        print("Uso: python ASTARTraslados.py <path mapa.csv> <num-h>")
        sys.exit(1)

    archivo_mapa = sys.argv[1]
    num_heuristica = int(sys.argv[2])

    # Validar que num_heuristica sea 1 o 2
    if num_heuristica not in {1, 2, 3, 4, 5,6}:
        print("El parámetro num-h debe ser 1, 2 o 3.")
        sys.exit(1)

    mapa = Mapa(archivo_mapa)
    camino, coste_acumulado, nodos_expandidos = mapa.a_estrella(num_heuristica)
    elapsed_time = stop_timer(start_time)

    if camino:
        # Escribir el camino en un archivo
        # Obtener el nombre del mapa sin el formato del final
        nombre_archivo_mapa = archivo_mapa.split('/')[-1].split('.')[0]
        nombre_archivo = nombre_archivo_mapa + '-' + str(num_heuristica) + '.output'
        with open(nombre_archivo, 'w') as archivo_salida:
            for mapa in camino:
                celda = mapa.get_celda(mapa.ambulancia.celdaX, mapa.ambulancia.celdaY)
                linea = f"({celda.fila},{celda.columna}):{celda.tipo}:{mapa.ambulancia.energia_left}\n"
                archivo_salida.write(linea)
        print("Camino encontrado y escrito en " + nombre_archivo)

        generar_estadisticas(elapsed_time, coste_acumulado, camino, nodos_expandidos, nombre_archivo_mapa, num_heuristica)
    else:
        nombre_archivo_mapa = archivo_mapa.split('/')[-1].split('.')[0]
        nombre_archivo = nombre_archivo_mapa + '-' + str(num_heuristica) + '.output'
        with open(nombre_archivo, 'w') as archivo_salida:
            archivo_salida.write("Insoluble")
        generar_estadisticas(elapsed_time, 'Inalcanzable', [], nodos_expandidos, nombre_archivo_mapa, num_heuristica)

        print("No se encontró un camino.")


    formatted_time = format_time(elapsed_time)
    print(f"Elapsed time: {formatted_time}")


def generar_estadisticas(tiempo_total, coste, camino, nodos_expandidos, archivo_mapa, num_heuristica):

    # Longitud del plan es el número de nodos desde el inicial hasta la solución
    longitud_plan = len(camino)

    archivo_salida = archivo_mapa + '-' + str(num_heuristica) + '.stat'
    # Escribir estadísticas en el archivo
    with open(archivo_salida, 'w') as archivo_estadisticas:
        archivo_estadisticas.write(f"Tiempo total: {tiempo_total}\n")
        archivo_estadisticas.write(f"Coste total: {coste}\n")
        archivo_estadisticas.write(f"Longitud del plan: {longitud_plan}\n")
        archivo_estadisticas.write(f"Nodos expandidos: {nodos_expandidos}\n")



if __name__ == "__main__":
    main()

