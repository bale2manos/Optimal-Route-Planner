import csv
import sys
from mapa import Mapa



def main():
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
            for nodo in camino:
                celda = nodo.mapa.get_celda(nodo.ambulancia.celdaX, nodo.ambulancia.celdaY)
                linea = f"({celda.fila},{celda.columna}):{celda.tipo}:{nodo.ambulancia.energia_left}\n"
                archivo_salida.write(linea)
        print("Camino encontrado y escrito en 'camino_solucion.txt'")
    else:
        print("No se encontró un camino.")

if __name__ == "__main__":
    main()

