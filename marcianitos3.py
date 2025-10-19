import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders con Enemigos")

# Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()


# -----------------------------------------------------
# 🧱 Clase base Actor
# -----------------------------------------------------
class Actor:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def actualizar(self):
        pass

    def dibujar(self, superficie):
        pass


# -----------------------------------------------------
# 🚀 Clase de la Nave del Jugador
# -----------------------------------------------------
class NaveJugador(Actor):
    def __init__(self, x, y, ancho=60, alto=20, color=VERDE, velocidad=7):
        super().__init__(x, y, color)
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.x < ANCHO - self.ancho:
            self.x += self.velocidad

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))


# -----------------------------------------------------
# 💥 Clase Bala
# -----------------------------------------------------
class Bala(Actor):
    def __init__(self, x, y, color=BLANCO, radio=3, velocidad=-10):
        super().__init__(x, y, color)
        self.radio = radio
        self.velocidad = velocidad

    def actualizar(self):
        self.y += self.velocidad

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)

    def colisiona_con(self, enemigo):
        # Colisión simple por distancia (círculo vs rectángulo)
        return (enemigo.x < self.x < enemigo.x + enemigo.ancho and
                enemigo.y < self.y < enemigo.y + enemigo.alto)


# -----------------------------------------------------
# 👾 Clase Enemigo
# -----------------------------------------------------
class Enemigo(Actor):
    def __init__(self, x, y, ancho=40, alto=20, color=ROJO, velocidad=3):
        super().__init__(x, y, color)
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
        self.direccion = 1  # 1 = derecha, -1 = izquierda

    def actualizar(self):
        self.x += self.velocidad * self.direccion
        # Cambiar de dirección al tocar los bordes
        if self.x <= 0 or self.x + self.ancho >= ANCHO:
            self.direccion *= -1
            self.y += 20  # Baja un poco

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))


# -----------------------------------------------------
# 🎮 Bucle principal del juego
# -----------------------------------------------------
def main():
    jugador = NaveJugador(ANCHO // 2 - 30, ALTO - 50)
    balas = []
    enemigos = []

    # Crear enemigos iniciales
    filas = 3
    columnas = 8
    espaciado = 80
    for fila in range(filas):
        for col in range(columnas):
            x = 100 + col * espaciado
            y = 80 + fila * 50
            enemigos.append(Enemigo(x, y))

    ejecutando = True
    while ejecutando:
        clock.tick(FPS)
        VENTANA.fill(NEGRO)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    # Crear bala en el centro de la nave
                    bala_x = jugador.x + jugador.ancho // 2
                    bala_y = jugador.y
                    balas.append(Bala(bala_x, bala_y))

        # Movimiento jugador
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        # Actualizar balas
        for bala in balas:
            bala.actualizar()
        balas = [b for b in balas if b.y > 0]

        # Actualizar enemigos
        for enemigo in enemigos:
            enemigo.actualizar()

        # Detectar colisiones bala-enemigo
        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if bala.colisiona_con(enemigo):
                    enemigos.remove(enemigo)
                    balas.remove(bala)
                    break

        # Dibujar todos los elementos
        jugador.dibujar(VENTANA)
        for bala in balas:
            bala.dibujar(VENTANA)
        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)

        # Mostrar si ganaste
        if not enemigos:
            fuente = pygame.font.Font(None, 60)
            texto = fuente.render("¡GANASTE!", True, BLANCO)
            VENTANA.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
