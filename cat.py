import pygame
import sys
import time

pygame.init()

ANCHO, ALTO = 400, 400
CELDA_SIZE = 80

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

raton_original = pygame.image.load("raton.jpg")
gato_original = pygame.image.load("gato.jpg")
box_original = pygame.image.load("box.jpg")
weed_original = pygame.image.load("weed.jpg")

raton_img = pygame.transform.scale(raton_original, (CELDA_SIZE, CELDA_SIZE))
gato_img = pygame.transform.scale(gato_original, (CELDA_SIZE, CELDA_SIZE))
box_img = pygame.transform.scale(box_original, (CELDA_SIZE, CELDA_SIZE))
weed_img = pygame.transform.scale(weed_original, (CELDA_SIZE, CELDA_SIZE))

class Estado:
    def __init__(self, raton_pos, gato_pos, turno_raton):
        self.raton_pos = raton_pos
        self.gato_pos = gato_pos
        self.turno_raton = turno_raton


def evaluar_estado(estado):
    raton_x, raton_y = estado.raton_pos
    gato_x, gato_y = estado.gato_pos
    distancia = abs(raton_x - gato_x) + abs(raton_y - gato_y)
    return distancia

def generar_movimientos(estado):
    movimientos = []
    x, y = estado.raton_pos if estado.turno_raton else estado.gato_pos
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 5 and 0 <= ny < 5 and (nx, ny) != (2, 2):  # Excluir la posición del obstáculo
            if estado.turno_raton:
                nueva_posicion = (nx, ny)
                movimientos.append(Estado(nueva_posicion, estado.gato_pos, False))
            else:
                nueva_posicion = (nx, ny)
                movimientos.append(Estado(estado.raton_pos, nueva_posicion, True))
                
    return movimientos


def minimax(estado, profundidad, maximizando):
    if profundidad == 0:
        return evaluar_estado(estado)
    
    if maximizando:
        mejor_valor = float('-inf')
        for movimiento in generar_movimientos(estado):
            valor = minimax(movimiento, profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor 
    else:
        mejor_valor = float('inf')
        for movimiento in generar_movimientos(estado):
            valor = minimax(movimiento, profundidad - 1, True)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor


def mejor_movimiento(estado, profundidad):
    mejor_mov = None
    mejor_valor = float('-inf') if estado.turno_raton else float('inf')
    
    for movimiento in generar_movimientos(estado):
        valor = minimax(movimiento, profundidad - 1, not estado.turno_raton)
        if estado.turno_raton and valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = movimiento
        elif not estado.turno_raton and valor < mejor_valor:
            mejor_valor = valor
            mejor_mov = movimiento
    
    return mejor_mov


def dibujar_tablero(screen, escape_x, escape_y):
    for y in range(0, ALTO, CELDA_SIZE):
        for x in range(0, ANCHO, CELDA_SIZE):
            rect = pygame.Rect(x, y, CELDA_SIZE, CELDA_SIZE)
            pygame.draw.rect(screen, BLANCO, rect, 1)
    rect = pygame.Rect(escape_x * CELDA_SIZE, escape_y * CELDA_SIZE, CELDA_SIZE, CELDA_SIZE)
    screen.blit(box_img, (escape_x * CELDA_SIZE, escape_y * CELDA_SIZE))
    # Dibujar el obstáculo en el centro del tablero
    screen.blit(weed_img, (2 * CELDA_SIZE, 2 * CELDA_SIZE))


def dibujar_celda(screen, CELDA_X1, CELDA_Y1, CELDA_X2, CELDA_Y2):
    x1 = CELDA_X1 * CELDA_SIZE
    y1 = CELDA_Y1 * CELDA_SIZE
    screen.blit(raton_img, (x1, y1))

    x2 = CELDA_X2 * CELDA_SIZE
    y2 = CELDA_Y2 * CELDA_SIZE
    screen.blit(gato_img, (x2, y2))


def mostrar_mensaje(screen, mensaje):
    font = pygame.font.Font(None, 36)
    text = font.render(mensaje, True, BLANCO)
    text_rect = text.get_rect(center=(ANCHO // 2, ALTO // 2))
    screen.blit(text, text_rect)


def main():
    max_turnos = 30
    contador_turnos = 0
    
    reloj = pygame.time.Clock()
    espera_gato = False
    tiempo_inicio_espera = 0
    
    CELDA_X1, CELDA_Y1 = 4, 4
    CELDA_X2, CELDA_Y2 = 0, 0
    
    escape_x, escape_y = CELDA_X2, CELDA_Y2
    
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('El Gato y el Ratón')
    
    estado = Estado((CELDA_X1, CELDA_Y1), (CELDA_X2, CELDA_Y2), True)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN and contador_turnos % 2 == 0:
                if event.key == pygame.K_UP:
                    if CELDA_Y1 - 1 >= 0 and (CELDA_X1, CELDA_Y1 - 1) != (2, 2):
                        CELDA_Y1 -= 1
                    else:
                        mostrar_mensaje(screen, "Movimiento no válido")
                        pygame.display.flip()
                        pygame.time.delay(300)
                        continue
                elif event.key == pygame.K_DOWN:
                    if CELDA_Y1 + 1 < 5 and (CELDA_X1, CELDA_Y1 + 1) != (2, 2):
                        CELDA_Y1 += 1
                    else:
                        mostrar_mensaje(screen, "Movimiento no válido")
                        pygame.display.flip()
                        pygame.time.delay(300)
                        continue
                elif event.key == pygame.K_LEFT:
                    if CELDA_X1 - 1 >= 0 and (CELDA_X1 - 1, CELDA_Y1) != (2, 2):
                        CELDA_X1 -= 1
                    else:
                        mostrar_mensaje(screen, "Movimiento no válido")
                        pygame.display.flip()
                        pygame.time.delay(300)
                        continue
                elif event.key == pygame.K_RIGHT:
                    if CELDA_X1 + 1 < 5 and (CELDA_X1 + 1, CELDA_Y1) != (2, 2):
                        CELDA_X1 += 1
                    else:
                        mostrar_mensaje(screen, "Movimiento no válido")
                        pygame.display.flip()
                        pygame.time.delay(300)
                        continue
                
                estado = Estado((CELDA_X1, CELDA_Y1), estado.gato_pos, False)
                contador_turnos += 1
                espera_gato = True
                tiempo_inicio_espera = time.time()
                
        if espera_gato and (time.time() - tiempo_inicio_espera) >= 0.1:
            mejor_mov = mejor_movimiento(estado, 5)
            CELDA_X2, CELDA_Y2 = mejor_mov.gato_pos
            estado = Estado(estado.raton_pos, mejor_mov.gato_pos, True)
            contador_turnos += 1
            espera_gato = False
                
        if CELDA_X1 == escape_x and CELDA_Y1 == escape_y:
            mostrar_mensaje(screen, "¡Has ganado!")
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()
        
        if CELDA_X1 == CELDA_X2 and CELDA_Y1 == CELDA_Y2 and (CELDA_X1 != escape_x or CELDA_Y1 != escape_y):
            mostrar_mensaje(screen, "¡El gato te atrapó!")
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()
                
        if contador_turnos >= max_turnos:
            mostrar_mensaje(screen, "¡Empate!")
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()
                
        screen.fill(NEGRO)
        dibujar_tablero(screen, escape_x, escape_y)
        dibujar_celda(screen, CELDA_X1, CELDA_Y1, CELDA_X2, CELDA_Y2)
        
        pygame.display.flip()
        
        reloj.tick(120)

if __name__ == '__main__':
    main()