import random
from Constantes import *
# Crear la matriz (mapa)
def generate_grid(size):
    grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    # Agregar paredes, turbo, enemigos y la meta
    for _ in range(random.randint(int((size*size)/4), size*size)):  # Número aleatorio de paredes
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        grid[x][y] = WALL
    #for _ in range(random.randint(4, size)):  # Agregar algunos turbos
    #    x, y = random.randint(0, size-1), random.randint(0, size-1)
    #    grid[x][y] = TURBO
    #for _ in range(random.randint(4, size)):  # Agregar algunos enemigos
    #    x, y = random.randint(0, size-1), random.randint(0, size-1)
    #    grid[x][y] = ENEMY
    grid[0][0] = 0
    if grid[1][0] == 1:
        grid[1][0] = 0
    elif grid[0][1] == 1:
        grid[0][1] = 0
    grid[size-2][size-1] = 0
    grid[size-1][size-2] = 0
    grid[size-1][size-1] = GOAL  # Meta en la esquina inferior derecha
    for i in grid:
        print(i)
    #grid = [[0, 0, 0, 0, 0]]
    #grid.append([0, 0, 0, 0, 0])
    #grid.append([0, 0, 0, 0, 0])
    #grid.append([0, 0, 0, 0, 0])
    #grid.append([0, 0, 0, 0, 4])
    
    return grid


# Movimiento del jugador
def move_player(player_pos, direction, grid):
    x, y = player_pos
    if direction == 'UP' and y > 0 and grid[y-1][x] != WALL:
        y -= 1
    elif direction == 'DOWN' and y < GRID_SIZE - 1 and grid[y+1][x] != WALL:
        y += 1
    elif direction == 'LEFT' and x > 0 and grid[y][x-1] != WALL:
        x -= 1
    elif direction == 'RIGHT' and x < GRID_SIZE - 1 and grid[y][x+1] != WALL:
        x += 1
    return (x, y)

# Costo de moverse a una casilla
def get_move_cost(x, y, grid):
    if grid[y][x] == TURBO:
        return 0.5  # Menor costo en turbo
    elif grid[y][x] == ENEMY:
        return 2.0  # Mayor costo cerca de enemigos
    return 1.0  # Costo normal


def obtener_vecinos(player_pos,grid):
    x, y = player_pos
    vecinos = []
    
    
    if  x > 0 and grid[y][x-1] != WALL:
        vecinos.append(("izquierda",(x-1, y),get_move_cost(x-1,y,grid)))
    if  y > 0 and grid[y-1][x] != WALL:
        vecinos.append(("arriba",(x, y-1),get_move_cost(x,y-1,grid)))
    if  x < len(grid) - 1 and grid[y][x+1] != WALL:
        vecinos.append(("derecha",(x+1, y),get_move_cost(x+1,y,grid)))
    if  y < len(grid) - 1 and grid[y+1][x] != WALL:
        vecinos.append(("abajo",(x, y+1),get_move_cost(x,y+1,grid)))
    return vecinos