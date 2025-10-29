import pygame
import sys
import random
import os

pygame.init()

#configuración base
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("MARCIANITOS")

#colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (0, 150, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
MORADO = (180, 0, 255)
GRIS = (100, 100, 100)

FPS = 60
clock = pygame.time.Clock()

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

def mostrar_texto(texto, tamano, color, y_offset=0):
    fuente = pygame.font.Font(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(ANCHO // 2, ALTO // 2 + y_offset))
    VENTANA.blit(superficie, rect)

class Actor:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def actualizar(self):
        pass

    def dibujar(self, superficie):
        pass

class NaveJugador(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, VERDE)
        self.ancho = 60
        self.alto = 20
        self.velocidad = 7
        self.tiempo_recarga = 500
        self.ultimo_disparo = 0
        self.vidas = 3

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.x < ANCHO - self.ancho:
            self.x += self.velocidad

    def puede_disparar(self):
        return pygame.time.get_ticks() - self.ultimo_disparo >= self.tiempo_recarga

    def disparar(self, x_offset=0):
        self.ultimo_disparo = pygame.time.get_ticks()
        return BalaJugador(self.x + self.ancho // 2 + x_offset, self.y)

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))
        #mostrar vidas
        fuente = pygame.font.Font(None, 32)
        texto = fuente.render(f"Vidas: {self.vidas}", True, AMARILLO)
        superficie.blit(texto, (ANCHO - 150, 10))

class Bala(Actor):
    def __init__(self, x, y, color, velocidad):
        super().__init__(x, y, color)
        self.velocidad = velocidad
        self.radio = 4

    def actualizar(self):
        self.y += self.velocidad

    def fuera(self):
        return self.y < 0 or self.y > ALTO

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)

class BalaJugador(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, BLANCO, -8)

    def colisiona(self, enemigo):
        return enemigo.x < self.x < enemigo.x + enemigo.ancho and enemigo.y < self.y < enemigo.y + enemigo.alto

class BalaEnemigo(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, AMARILLO, 5)

class Enemigo(Actor):
    def __init__(self, x, y, nivel):
        #cambia el color y comportamiento según el nivel
        if nivel < 3:
            color = VERDE
            self.vida = 1
        elif nivel < 6:
            color = AZUL
            self.vida = 2
        else:
            color = ROJO
            self.vida = 3

        super().__init__(x, y, color)
        self.ancho = 40
        self.alto = 20
        self.velocidad = 2 + nivel * 0.3
        self.direccion = 1
        self.prob_disparo = 0.001 + nivel * 0.0005

    def actualizar(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= ANCHO:
            self.direccion *= -1
            self.y += 20

    def disparar(self):
        if random.random() < self.prob_disparo:
            return BalaEnemigo(self.x + self.ancho // 2, self.y + self.alto)
        return None

    def colisiona_con_jugador(self, jugador):
        return (
            jugador.x < self.x + self.ancho
            and jugador.x + jugador.ancho > self.x
            and jugador.y < self.y + self.alto
            and jugador.y + jugador.alto > self.y
        )

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))

class Boss(Actor):
    def __init__(self, nivel):
        super().__init__(ANCHO // 2 - 100, 80, MORADO)
        self.ancho = 200
        self.alto = 60
        self.vida_max = 30 + nivel * 10
        self.vida = self.vida_max
        self.velocidad = 3
        self.direccion = 1
        self.prob_disparo = 0.02

    def actualizar(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= ANCHO:
            self.direccion *= -1

    def disparar(self):
        if random.random() < self.prob_disparo:
            return BalaEnemigo(self.x + self.ancho // 2, self.y + self.alto)
        return None

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))
        #barra de vida del boss
        vida_ratio = self.vida / self.vida_max
        pygame.draw.rect(superficie, ROJO, (200, 20, 400, 20))
        pygame.draw.rect(superficie, VERDE, (200, 20, 400 * vida_ratio, 20))


def menu_principal():
    while True:
        VENTANA.fill(NEGRO)
        mostrar_texto("SPACE INVADERS", 72, BLANCO, -100)
        mostrar_texto("1. JUGAR", 48, BLANCO, -20)
        mostrar_texto("2. SALIR", 48, BLANCO, 40)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    return
                elif e.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()


def main():
    menu_principal()

    jugador = NaveJugador(ANCHO // 2 - 30, ALTO - 50)
    nivel = 1
    puntaje = 0
    highscore = cargar_highscore()
    game_over = False
    ganaste = False

    def generar_enemigos(nivel):
        if nivel % 5 == 0:
            return [Boss(nivel)], True
        enemigos = [Enemigo(100 + c * 80, 80 + f * 50, nivel) for f in range(3) for c in range(8)]
        return enemigos, False

    enemigos, es_boss = generar_enemigos(nivel)
    balas_jugador = []
    balas_enemigas = []

    while True:
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and jugador.puede_disparar():
                    balas_jugador.append(jugador.disparar())
                if (game_over or ganaste) and evento.key == pygame.K_r:
                    return main()
                if (game_over or ganaste) and evento.key == pygame.K_m:
                    return main()

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        if not game_over and not ganaste:
            #actualizar balas
            for b in balas_jugador: b.actualizar()
            for b in balas_enemigas: b.actualizar()
            balas_jugador[:] = [b for b in balas_jugador if not b.fuera()]
            balas_enemigas[:] = [b for b in balas_enemigas if not b.fuera()]

            #actualizar enemigos
            for e in enemigos:
                e.actualizar()
                nueva = e.disparar()
                if nueva: balas_enemigas.append(nueva)

            for b in balas_jugador[:]:
                for e in enemigos[:]:
                    if isinstance(e, Boss):
                        if e.x < b.x < e.x + e.ancho and e.y < b.y < e.y + e.alto:
                            e.vida -= 1
                            if b in balas_jugador: balas_jugador.remove(b)
                            if e.vida <= 0:
                                enemigos.remove(e)
                                ganaste = True
                            break
                    else:
                        if b.colisiona(e):
                            e.vida -= 1
                            if e.vida <= 0:
                                enemigos.remove(e)
                                puntaje += 1
                                if puntaje > highscore:
                                    highscore = puntaje
                                    guardar_highscore(highscore)
                            if b in balas_jugador: balas_jugador.remove(b)
                            break

            #colisiones balas enemigas vs jugador
            for b in balas_enemigas[:]:
                if jugador.x < b.x < jugador.x + jugador.ancho and jugador.y < b.y < jugador.y + jugador.alto:
                    balas_enemigas.remove(b)
                    jugador.vidas -= 1
                    if jugador.vidas <= 0:
                        game_over = True

            #colisiones con enemigos vs jugador
            for e in enemigos:
                if hasattr(e, 'colisiona_con_jugador') and e.colisiona_con_jugador(jugador):
                    jugador.vidas = 0
                    game_over = True


            if not enemigos and not es_boss:
                nivel += 1
                enemigos, es_boss = generar_enemigos(nivel)
                balas_jugador.clear()
                balas_enemigas.clear()
                jugador.x = ANCHO // 2 - jugador.ancho // 2
                mostrar_texto(f"NIVEL {nivel}", 60, BLANCO)
                pygame.display.flip()
                pygame.time.delay(1500)

        VENTANA.fill(NEGRO)
        jugador.dibujar(VENTANA)
        for e in enemigos: e.dibujar(VENTANA)
        for b in balas_jugador: b.dibujar(VENTANA)
        for b in balas_enemigas: b.dibujar(VENTANA)

        fuente = pygame.font.Font(None, 36)
        VENTANA.blit(fuente.render(f"Puntos: {puntaje}", True, BLANCO), (10, 10))
        VENTANA.blit(fuente.render(f"Récord: {highscore}", True, AMARILLO), (10, 50))
        VENTANA.blit(fuente.render(f"Nivel: {nivel}", True, AZUL), (10, 90))

        if game_over:
            mostrar_texto("¡GAME OVER!", 60, ROJO)
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)
        elif ganaste and es_boss:
            mostrar_texto("¡HAS VENCIDO AL JEFE FINAL!", 60, BLANCO)
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)

        pygame.display.flip()

if __name__ == "__main__":
    main()