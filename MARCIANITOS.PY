import pygame
import sys

# Inicializar pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini Space Invaders - Solo Nave")

# Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)

# Reloj para controlar FPS
FPS = 60
clock = pygame.time.Clock()

# Propiedades de la nave
nave_ancho = 60
nave_alto = 20
nave_x = ANCHO // 2 - nave_ancho // 2
nave_y = ALTO - 50
velocidad_nave = 7

# Balas
balas = []
velocidad_bala = -10
radio_bala = 3

# Bucle principal del juego
ejecutando = True
while ejecutando:
    clock.tick(FPS)
    VENTANA.fill(NEGRO)

    # --- Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Crear una bala en el centro de la nave
                bala_x = nave_x + nave_ancho // 2
                bala_y = nave_y
                balas.append([bala_x, bala_y])

    # --- Movimiento de la nave ---
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and nave_x > 0:
        nave_x -= velocidad_nave
    if teclas[pygame.K_RIGHT] and nave_x < ANCHO - nave_ancho:
        nave_x += velocidad_nave

    # --- Movimiento de las balas ---
    for bala in balas:
        bala[1] += velocidad_bala
    # Eliminar balas que salen de la pantalla
    balas = [b for b in balas if b[1] > 0]

    # --- Dibujar todo ---
    # Dibujar nave
    pygame.draw.rect(VENTANA, VERDE, (nave_x, nave_y, nave_ancho, nave_alto))
    # Dibujar balas
    for bala in balas:
        pygame.draw.circle(VENTANA, BLANCO, (bala[0], bala[1]), radio_bala)

    # Actualizar pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()
