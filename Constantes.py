# Dimensiones de la ventana
CELL_SIZE = 40
GRID_SIZE = 5  # Tamaño de la matriz (6x6)
GAME_AREA_WIDTH, GAME_AREA_HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Cambia el tamaño de la ventana para hacerla más ancha
HEIGHT = 750
WIDTH = 1240  # Ajusta para que la ventana sea más ancha
#GAME_AREA_WIDTH = WIDTH - 300  # Área del juego

# Cambia la inicialización de la ventana
#window = pygame.display.set_mode((WIDTH, HEIGHT))


# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)

# Tipos de terreno
EMPTY = 0
WALL = 1
TURBO = 2
ENEMY = 3
GOAL = 4

# arboles
node_radius = 15
node_color = (0, 0, 255)  # Azul para los nodos
line_color = (0, 0, 0)  # Negro para las líneas

# Posición inicial del árbol en pantalla (ajusta según el espacio disponible)
x_offset = GAME_AREA_WIDTH + 50
y_offset = 750
node_spacing_x = 55
node_spacing_y = 45