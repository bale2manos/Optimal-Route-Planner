import csv


def read_coordinates_from_file(file_path):
    coordinates_list = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Extract coordinates from each line
        coordinates = tuple(map(int, line.strip().split(':')[0].lstrip('(').rstrip(')').split(',')))
        coordinates_list.append(coordinates)

    return coordinates_list

def get_rows_and_columns(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
        num_rows = len(rows)
        num_columns = len(rows[0]) if rows else 0  # Assuming all rows have the same length

    return num_rows, num_columns


def create_grid(coordinates, num_columns, num_rows):
    # Create grid
    global grid
    all_paths = []

    # Mark path and handle opposite directions
    initial_step = True
    previous_start = coordinates[0]
    start = None
    action = None
    step = 0
    while step < len(coordinates):
        x, y = coordinates[step]
        if initial_step:
            grid = create_empty_grid(num_rows, num_columns)
            all_paths.append(grid)
            initial_step = False

        if previous_start:
            grid[2 * (previous_start[0] - 1)][2 * (previous_start[1] - 1)] = 'S'
            if start is not None:
                grid[2 * (start[0] - 1)][2 * (start[1] - 1)] = '@'
                if action == '↑':
                    grid[2 * (start[0] - 1) + 1][2 * (start[1] - 1)] = '↑'
                elif action == '↓':
                    grid[2 * (start[0] - 1) - 1][2 * (start[1] - 1)] = '↓'
                elif action == '←':
                    grid[2 * (start[0] - 1)][2 * (start[1] - 1) + 1] = '←'
                elif action == '→':
                    grid[2 * (start[0] - 1)][2 * (start[1] - 1) - 1] = '→'
                start = None
        else:
            if grid[2 * (x - 1)][2 * (y - 1)] == '@':
                # Stay in the same place
                grid[2 * (x - 1)][2 * (y - 1)] = 'X'
            elif grid[2 * (x - 1)][2 * (y - 1)] == 'S':
                # Stay in the same place
                grid[2 * (x - 1)][2 * (y - 1)] = 'S'
            else:
                grid[2 * (x - 1)][2 * (y - 1)] = '@'

            if step > 0:
                prev_x, prev_y = coordinates[step - 1]
                if x < prev_x:  # Moving up
                    if grid[2 * (x - 1) + 1][2 * (y - 1)] == ' ':
                        grid[2 * (x - 1) + 1][2 * (y - 1)] = '↑'
                    else:
                        initial_step = True
                        previous_start = (prev_x, prev_y)
                        start = (x, y)
                        action = '↑'
                        continue
                elif x > prev_x:  # Moving down
                    if step == 21:
                        print('hola')
                    if grid[2 * (x - 1) - 1][2 * (y - 1)] == ' ':
                        grid[2 * (x - 1) - 1][2 * (y - 1)] = '↓'
                    else:
                        initial_step = True
                        previous_start = (prev_x, prev_y)
                        start = (x, y)
                        action = '↓'
                        continue
                elif y < prev_y:  # Moving left
                    if grid[2 * (x - 1)][2 * (y - 1) + 1] == ' ':
                        grid[2 * (x - 1)][2 * (y - 1) + 1] = '←'
                    else:
                        initial_step = True
                        previous_start = (prev_x, prev_y)
                        start = (x, y)
                        action = '←'
                        continue
                elif y > prev_y:  # Moving right
                    if grid[2 * (x - 1)][2 * (y - 1) - 1] == ' ':
                        grid[2 * (x - 1)][2 * (y - 1) - 1] = '→'
                    else:
                        initial_step = True
                        previous_start = (prev_x, prev_y)
                        start = (x, y)
                        action = '→'
                        continue

        if step == len(coordinates) - 1:
            grid[2 * (x - 1)][2 * (y - 1)] = 'E'
        previous_start = None
        start = None
        step += 1
    return all_paths


def create_empty_grid(num_rows, num_columns):
    grid = []
    cell = True
    row = True
    for i in range(2 * num_rows - 1):
        grid.append([])
        cell = True
        for j in range(2 * num_columns - 1):
            if row:
                if cell:
                    grid[i].append('.')
                else:
                    grid[i].append(' ')
                cell = not cell
            else:
                grid[i].append(' ')
        row = not row
    return grid

def formatear_lista(lista):
    return ' '.join(elemento if isinstance(elemento, str) else elemento[0] for elemento in lista)

def procesar_lista_de_listas(lista_de_listas, num_columns):
    resultado = []
    separacion = '-' * num_columns*4
    for sublistas in lista_de_listas:
        for sublista in sublistas:
            resultado.append(formatear_lista(sublista))
        resultado.append(separacion)
    return '\n'.join(resultado[:-1])  # Elimina el último separador




# Example usage
coordinates = read_coordinates_from_file('mapa-not-so-big-3.output')
num_rows, num_columns = get_rows_and_columns('mapa-not-so-big.csv')

all_paths = create_grid(coordinates, num_columns, num_rows)
output = procesar_lista_de_listas(all_paths, num_columns)

print(output)
with open('camino.txt', 'w', encoding='utf-8') as file:
    file.write(output)
