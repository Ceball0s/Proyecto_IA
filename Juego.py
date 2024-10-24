import pygame
import time
import sys
import random
import pygame_gui
from Proyecto import *
from Juego_herramientas import *
from Constantes import *

# Dibujar la matriz
def draw_grid(grid, player_pos):
    GRID_SIZE = len(grid)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[x][y] == EMPTY:
                pygame.draw.rect(window, WHITE, rect)
            elif grid[x][y] == WALL:
                pygame.draw.rect(window, GRAY, rect)
            elif grid[x][y] == TURBO:
                pygame.draw.rect(window, BLUE, rect)
            elif grid[x][y] == ENEMY:
                pygame.draw.rect(window, YELLOW, rect)
            elif grid[x][y] == GOAL:
                pygame.draw.rect(window, GREEN, rect)
            pygame.draw.rect(window, BLACK, rect, 1)  # Bordes de las celdas

    # Dibujar al jugador
    player_rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(window, RED, player_rect)

# Función para dibujar el árbol de nodos creado por BFS
def draw_tree(arbol, start_pos, inx_estra):
    """
    tree: un diccionario donde las llaves son nodos y los valores son sus vecinos.
    start_pos: la posición inicial del nodo raíz en la pantalla.
    """

    # Empezar en la raíz del árbol
    while arbol.padre:
        arbol = arbol.padre
    def dibujar_arbol():
        lista_nodos_previa = []  # Guardará los nodos del nivel anterior
        lista_padres_previa = []
        for profundidad in range(0, 25):  # Iterar sobre las profundidades
            lista_profundiad = arbol.obtener_hijos_a_profundidad(profundidad)
            if lista_profundiad is None or len(lista_profundiad) == 0:
                break

            num_nodos = len(lista_profundiad)  # Número de nodos en este nivel

            # Ajuste para centrar los nodos en cada nivel
            total_width = num_nodos * node_spacing_x
            x_start = ((GAME_AREA_WIDTH - total_width) // 2 ) + (x_offset + (x_offset / 2))  # Punto inicial para centrar los nodos

            lista_nodos_actual = []  # Guardará las posiciones de los nodos en este nivel
            lista_padres_actual = []
            for i,  (estado, padre, nodo) in enumerate(lista_profundiad):
                # Calcular la posición del nodo
                y_pos = (profundidad * node_spacing_y) + 20  # Ajusta el espacio entre niveles
                x_pos = GAME_AREA_WIDTH + x_start + i * node_spacing_x  # Espaciado ajustado entre nodos

                if not not nodo.hijos:
                    node_color = BLUE
                else:
                    node_color = YELLOW
                # Dibujar el nodo (círculo azul)
                pygame.draw.circle(window, node_color, (x_pos, y_pos), node_radius)

                # Añadir el estado como texto
                font = pygame.font.Font(None, 12)  # Tamaño de fuente más pequeño
                text_surface = font.render(str(estado), True, (255, 255, 255))
                window.blit(text_surface, (x_pos - 10, y_pos - 10))  # Centra el texto en el nodo

                # Guardar la posición del nodo actual
                lista_nodos_actual.append((x_pos, y_pos))
                lista_padres_actual.append(nodo)
                if lista_padres_previa != []:
                    indice_padre = 0
                    for idx, nodos in enumerate(lista_padres_previa):
                        if nodos == nodo.padre:
                            indice_padre = idx
                            break

                    padre_pos = lista_nodos_previa[indice_padre]
                    pygame.draw.line(window, line_color, padre_pos, (x_pos, y_pos), 2)
                
            # Actualizar la lista de nodos previa para la siguiente iteración
            lista_nodos_previa = lista_nodos_actual
            lista_padres_previa = lista_padres_actual

    # Llamada inicial para dibujar el árbol
    dibujar_arbol()

    #dibujar estrategia
    # Nombre de la estrategia actual basada en `idx_func` y la pila
    estrategias = [
        "Búsqueda en\n Anchura (BFS)", 
        "Búsqueda en\n Profundidad (DFS)", 
        "Búsqueda de\n Costo Uniforme (UCS)", 
        "Búsqueda \nAvara", 
        "Búsqueda en\n Profundidad Iterativa (IDS)"
    ]
    nombre_estrategia = estrategias[inx_estra]  # Obtener el nombre de la estrategia en uso
    font = pygame.font.Font(None, 36)  # Tamaño de fuente 36, puedes ajustar si prefieres otro tamaño
    # Renderizar el texto
    texto_estrategia = font.render(f"Estrategia: {nombre_estrategia}", True, (0, 0, 0))  # Texto negro
    window.blit(texto_estrategia, (WIDTH - 350, 10))  # Posición arriba a la derecha


def Verificar_grid(verificación=False):
    contador = 0
    while True:
        grid = generate_grid(GRID_SIZE)
        print("generando grid posible intento #",contador,end="\r")
        camino = avara(Nodo((0,0)),(GRID_SIZE-1,GRID_SIZE-1),grid,sys.maxsize)
        if camino or verificación:
            break
        contador += 1
    print()
    return grid

def movimiento(temp_arbol,grid,idx_func):
    lista_funciones = [bfs,dfs,ucs,avara,ids]
    return lista_funciones[idx_func](temp_arbol,(GRID_SIZE-1,GRID_SIZE-1),grid,1)

def Juego():
    # Configuración inicial del juego
    grid = Verificar_grid(True)
    player_pos = (0, 0)
    total_cost = 0
    arbol = Nodo((0, 0))
    pila = list(range(5))
    random.shuffle(pila)

    # Crear el área de texto para ingresar la cantidad de pasos
    text_input_rect = pygame.Rect((10, HEIGHT - 150), (200, 50))
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=text_input_rect, manager=manager)
    text_input.set_text('Cantidad de pasos')

    # Crear el botón que actúa como una casilla de verificación
    checkbox_rect = pygame.Rect((10, HEIGHT - 100), (200, 50))
    checkbox_button = pygame_gui.elements.UIButton(relative_rect=checkbox_rect,
                                                text="Verificar solución (marcado)",
                                                manager=manager)
    solucion_posible = False  # Variable que actúa como el estado de la casilla de verificación

    # Crear el botón de inicio
    start_button_rect = pygame.Rect((250, HEIGHT - 100), (150, 50))
    start_button = pygame_gui.elements.UIButton(relative_rect=start_button_rect,
                                                text="Iniciar Juego",
                                                manager=manager)

    # Reloj para controlar los FPS
    clock = pygame.time.Clock()

    # Bucle principal del juego
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0  # Tiempo entre cada frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Actualizar los eventos de la interfaz (pygame_gui)
            manager.process_events(event)

            # Verificar si el botón de inicio fue presionado
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # Verificar si se presionó el botón de la casilla de verificación
                    if event.ui_element == checkbox_button:
                        # Alternar el estado de la casilla de verificación
                        solucion_posible = not solucion_posible
                        if solucion_posible:
                            checkbox_button.set_text("Verificar solución (No marcado)")
                        else:
                            checkbox_button.set_text("Verificar solución (marcado)")

                    # Verificar si se presionó el botón de iniciar
                    if event.ui_element == start_button:
                        try:
                            pasos = int(text_input.get_text())  # Obtener la cantidad de pasos
                        except ValueError:
                            print("Ingrese una cantidad numérica")
                            break

                        # Aquí puedes agregar la lógica para verificar el grid y arrancar el juego
                        print(f"Iniciar juego con {pasos} pasos.")
                        if solucion_posible:
                            print("Verificando si el grid tiene solución.")
                        running = False
                        continue
                        # Lógica del juego: mover el jugador, verificar soluciones, etc.
                        # Aquí continúa el resto de tu lógica del juego...

        # Controlar el framerate y actualizar el manager
        manager.update(time_delta)
        window.fill(WHITE)
        manager.draw_ui(window)
        pygame.display.update()
    running = True
    contador = 0
    grid = Verificar_grid(solucion_posible)
    while running:

        # Verificar si el jugador llegó a la meta
        if grid[player_pos[0]][player_pos[1]] == GOAL or not arbol:
            print(f"¡Termino! Costo total: {total_cost}")
            time.sleep(5)
            player_pos = (0,0)
            total_cost = 0
            grid = Verificar_grid(solucion_posible)
            arbol = Nodo((0,0))
            
            #running = False

        # Dibujar el mapa y el jugador
        window.fill(WHITE)
        while arbol.padre:
            arbol = arbol.padre
        if pasos == contador:
            pila.pop()
            contador = 0
        else:
            contador += 1
        if len(pila) == 0:
            # Crear una lista con los números del 0 al 4
            pila = list(range(5))
            # Mezclar los números de forma aleatoria
            random.shuffle(pila)

        salida = movimiento(arbol, grid,4)

        if not salida:
            print("no tiene solucion")
            player_pos = (0,0)
            draw_tree(arbol, (GRID_SIZE, GRID_SIZE),4)
            arbol = salida
        else:
            #mostrar_arbol(arbol)
            arbol = salida
            player_pos = arbol.estado
            draw_tree(arbol, (GRID_SIZE, GRID_SIZE),4)    
        draw_grid(grid, player_pos)
        
        pygame.display.flip()
        time.sleep(2)
        
        # Controlar el framerate y actualizar el manager
        manager.update(time_delta)
        window.fill(WHITE)
        #manager.draw_ui(window)
        pygame.display.update()

    # Salir de Pygame
    pygame.quit()



if __name__ == "__main__":
    # Inicializar Pygame
    # Inicialización
    pygame.init()

    # Crear la ventana y el administrador de UI
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Juego de Estrategias')
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    Juego()
    

    