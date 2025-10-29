import pygame
import sys
import random
import os

# Inicializar pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders con Balas Heredadas")

# Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
AZUL = (0, 150, 255)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Archivo de puntuación máxima
HIGHSCORE_FILE = "highscore.txt"

def cargar_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def guardar_highscore(puntaje):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(puntaje))

# Clase base Actor
class Actor:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def actualizar(self):
        pass

    def dibujar(self, superficie):
        pass

# Clase de la Nave del Jugador
class NaveJugador(Actor):
    def __init__(self, x, y, ancho=60, alto=20, color=VERDE, velocidad=7, tiempo_recarga=500):
        super().__init__(x, y, color)
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
        self.tiempo_recarga = tiempo_recarga
        self.ultimo_disparo = 0
        self.buff_activo = False  # Para disparo en ráfaga

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.x < ANCHO - self.ancho:
            self.x += self.velocidad

    def puede_disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        return tiempo_actual - self.ultimo_disparo >= self.tiempo_recarga

    def disparar(self, x_offset=0):
        bala_x = self.x + self.ancho // 2 + x_offset
        bala_y = self.y
        return BalaJugador(bala_x, bala_y)

    def activar_buff(self):
        self.buff_activo = True
        self.tiempo_recarga = 100  # Disparo rápido

    def desactivar_buff(self):
        self.buff_activo = False
        self.tiempo_recarga = 500

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))
        if self.buff_activo:
            # Dibuja un indicador visual del buff
            pygame.draw.rect(superficie, AZUL, (self.x - 5, self.y - 5, self.ancho + 10, 5))

# Clase base Bala
class Bala(Actor):
    def __init__(self, x, y, color, radio=3, velocidad=-10):
        super().__init__(x, y, color)
        self.radio = radio
        self.velocidad = velocidad

    def actualizar(self):
        self.y += self.velocidad

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)

    def fuera_de_pantalla(self):
        return self.y < 0 or self.y > ALTO

# Bala del jugador
class BalaJugador(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, BLANCO, radio=4, velocidad=-8)

    def colisiona_con(self, enemigo):
        return (enemigo.x < self.x < enemigo.x + enemigo.ancho and
                enemigo.y < self.y < enemigo.y + enemigo.alto)

# Bala del enemigo
class BalaEnemigo(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, AMARILLO, radio=4, velocidad=5)

# Clase Enemigo
class Enemigo(Actor):
    def __init__(self, x, y, ancho=40, alto=20, color=ROJO, velocidad=3, prob_disparo=0.001):
        super().__init__(x, y, color)
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
        self.direccion = 1
        self.prob_disparo = prob_disparo

    def actualizar(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= ANCHO:
            self.direccion *= -1
            self.y += 20

    def disparar(self):
        if random.random() < self.prob_disparo:
            bala_x = self.x + self.ancho // 2
            bala_y = self.y + self.alto
            return BalaEnemigo(bala_x, bala_y)
        return None

    def colisiona_con_jugador(self, jugador):
        return (jugador.x < self.x + self.ancho and
                jugador.x + jugador.ancho > self.x and
                jugador.y < self.y + self.alto and
                jugador.y + jugador.alto > self.y)

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))

# Función para mostrar texto centrado
def mostrar_texto(texto, tamano, color, y_offset=0):
    fuente = pygame.font.Font(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(ANCHO // 2, ALTO // 2 + y_offset))
    VENTANA.blit(superficie, rect)

# Menú principal
def menu_principal():
    while True:
        VENTANA.fill(NEGRO)
        mostrar_texto("SPACE INVADERS", 72, BLANCO, -100)
        mostrar_texto("1. JUGAR", 48, BLANCO, -20)
        mostrar_texto("2. DEMO", 48, BLANCO, 30)
        mostrar_texto("3. SALIR", 48, BLANCO, 80)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return "jugar"
                elif evento.key == pygame.K_2:
                    return "demo"
                elif evento.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

# Modo demo (IA simple)
def modo_demo():
    jugador = NaveJugador(ANCHO // 2 - 30, ALTO - 50)
    balas_jugador = []
    balas_enemigas = []
    enemigos = []
    puntuacion = 0
    highscore = cargar_highscore()
    tiempo_demo = 0

    # Crear enemigos
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
        tiempo_demo += 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return

        # IA simple: moverse hacia el enemigo más bajo
        if enemigos:
            objetivo_x = sum(e.x for e in enemigos) / len(enemigos)
            if jugador.x + jugador.ancho // 2 < objetivo_x - 10:
                jugador.x += jugador.velocidad
            elif jugador.x + jugador.ancho // 2 > objetivo_x + 10:
                jugador.x -= jugador.velocidad

        # Disparar ocasionalmente
        if jugador.puede_disparar() and random.random() < 0.02:
            balas_jugador.append(jugador.disparar())

        # Actualizar balas
        for bala in balas_jugador:
            bala.actualizar()
        for bala in balas_enemigas:
            bala.actualizar()

        balas_jugador = [b for b in balas_jugador if not b.fuera_de_pantalla()]
        balas_enemigas = [b for b in balas_enemigas if not b.fuera_de_pantalla()]

        # Actualizar enemigos
        for enemigo in enemigos:
            enemigo.actualizar()
            nueva_bala = enemigo.disparar()
            if nueva_bala:
                balas_enemigas.append(nueva_bala)

        # Colisiones: balas jugador vs enemigos
        for bala in balas_jugador[:]:
            for enemigo in enemigos[:]:
                if bala.colisiona_con(enemigo):
                    enemigos.remove(enemigo)
                    if bala in balas_jugador:
                        balas_jugador.remove(bala)
                    puntuacion += 1
                    break

        # Colisiones: balas enemigas vs jugador
        for bala in balas_enemigas[:]:
            if (jugador.x < bala.x < jugador.x + jugador.ancho and
                jugador.y < bala.y < jugador.y + jugador.alto):
                balas_enemigas.remove(bala)
                ejecutando = False

        # Colisiones: enemigos vs jugador
        for enemigo in enemigos[:]:
            if enemigo.colisiona_con_jugador(jugador):
                ejecutando = False

        # Dibujar
        jugador.dibujar(VENTANA)
        for bala in balas_jugador:
            bala.dibujar(VENTANA)
        for bala in balas_enemigas:
            bala.dibujar(VENTANA)
        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)

        # Mostrar puntuación
        fuente = pygame.font.Font(None, 36)
        texto_puntaje = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        texto_high = fuente.render(f"Récord: {highscore}", True, AMARILLO)
        VENTANA.blit(texto_puntaje, (10, 10))
        VENTANA.blit(texto_high, (10, 50))

        # Ganar
        if not enemigos:
            mostrar_texto("¡GANASTE!", 60, BLANCO)
            pygame.display.flip()
            pygame.time.delay(2000)
            break

        pygame.display.flip()

        # Salir después de un tiempo
        if tiempo_demo > FPS * 30:  # 30 segundos
            break

# Bucle principal del juego
def main():
    modo = menu_principal()
    if modo == "demo":
        modo_demo()
        main()  # Volver al menú

    jugador = NaveJugador(ANCHO // 2 - 30, ALTO - 50)
    balas_jugador = []
    balas_enemigas = []
    enemigos = []
    puntuacion = 0
    highscore = cargar_highscore()

    # Crear enemigos
    filas = 3
    columnas = 8
    espaciado = 80
    for fila in range(filas):
        for col in range(columnas):
            x = 100 + col * espaciado
            y = 80 + fila * 50
            enemigos.append(Enemigo(x, y))

    ejecutando = True
    game_over = False
    ganaste = False

    while ejecutando:
        clock.tick(FPS)
        VENTANA.fill(NEGRO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and jugador.puede_disparar():
                    balas_jugador.append(jugador.disparar())
                if evento.key == pygame.K_z and jugador.puede_disparar():
                    # Disparo en ráfaga (buff)
                    offsets = [-10, 0, 10]
                    for offset in offsets:
                        balas_jugador.append(jugador.disparar(offset))
                    jugador.ultimo_disparo = pygame.time.get_ticks()
                if game_over or ganaste:
                    if evento.key == pygame.K_r:
                        main()  # Reiniciar
                    elif evento.key == pygame.K_m:
                        main()  # Volver al menú

        if not game_over and not ganaste:
            # Movimiento jugador
            teclas = pygame.key.get_pressed()
            jugador.mover(teclas)

            # Actualizar balas
            for bala in balas_jugador:
                bala.actualizar()
            for bala in balas_enemigas:
                bala.actualizar()

            balas_jugador = [b for b in balas_jugador if not b.fuera_de_pantalla()]
            balas_enemigas = [b for b in balas_enemigas if not b.fuera_de_pantalla()]

            # Actualizar enemigos
            for enemigo in enemigos:
                enemigo.actualizar()
                nueva_bala = enemigo.disparar()
                if nueva_bala:
                    balas_enemigas.append(nueva_bala)

            # Colisiones: balas jugador vs enemigos
            for bala in balas_jugador[:]:
                for enemigo in enemigos[:]:
                    if bala.colisiona_con(enemigo):
                        enemigos.remove(enemigo)
                        if bala in balas_jugador:
                            balas_jugador.remove(bala)
                        puntuacion += 1
                        if puntuacion > highscore:
                            highscore = puntuacion
                            guardar_highscore(highscore)
                        break

            # Colisiones: balas enemigas vs jugador
            for bala in balas_enemigas[:]:
                if (jugador.x < bala.x < jugador.x + jugador.ancho and
                    jugador.y < bala.y < jugador.y + jugador.alto):
                    balas_enemigas.remove(bala)
                    game_over = True

            # Colisiones: enemigos vs jugador
            for enemigo in enemigos[:]:
                if enemigo.colisiona_con_jugador(jugador):
                    game_over = True

            # Ganar
            if not enemigos:
                ganaste = True

        # Dibujar
        jugador.dibujar(VENTANA)
        for bala in balas_jugador:
            bala.dibujar(VENTANA)
        for bala in balas_enemigas:
            bala.dibujar(VENTANA)
        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)

        # Mostrar puntuación
        fuente = pygame.font.Font(None, 36)
        texto_puntaje = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        texto_high = fuente.render(f"Récord: {highscore}", True, AMARILLO)
        VENTANA.blit(texto_puntaje, (10, 10))
        VENTANA.blit(texto_high, (10, 50))

        # Game Over o Victoria
        if game_over:
            mostrar_texto("¡GAME OVER!", 60, ROJO)
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)
        elif ganaste:
            mostrar_texto("¡GANASTE!", 60, BLANCO)
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()