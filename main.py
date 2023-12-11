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
    if num_heuristica not in {1, 2}:
        print("El parámetro num-h debe ser 1 o 2.")
        sys.exit(1)

    mapa = Mapa(archivo_mapa)
    camino = mapa.a_estrella(num_heuristica)

    if camino:
        # Escribir el camino en un archivo
        with open('camino_solucion.txt', 'w') as archivo_salida:
            for mapa in camino:
                celda = mapa.get_celda(mapa.ambulancia.celdaX, mapa.ambulancia.celdaY)
                linea = f"({celda.fila},{celda.columna}):{celda.tipo}:{mapa.ambulancia.energia_left}\n"
                archivo_salida.write(linea)
        print("Camino encontrado y escrito en 'camino_solucion.txt'")
    else:
         print("No se encontró un camino.")

    elapsed_time = stop_timer(start_time)
    formatted_time = format_time(elapsed_time)
    print(f"Elapsed time: {formatted_time}")


if __name__ == "__main__":
    main()

