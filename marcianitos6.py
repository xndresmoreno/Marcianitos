import pygame
import sys
import random
import os

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders")

NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
AZUL = (0, 150, 255)

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
    def __init__(self, x, y):
        super().__init__(x, y, ROJO)
        self.ancho = 40
        self.alto = 20
        self.velocidad = 3
        self.direccion = 1
        self.prob_disparo = 0.001

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


def mostrar_texto(texto, tamano, color, y_offset=0):
    fuente = pygame.font.Font(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(ANCHO // 2, ALTO // 2 + y_offset))
    VENTANA.blit(superficie, rect)


def crear_demo():
    jugador = NaveJugador(ANCHO // 2 - 30, ALTO - 50)
    enemigos = [Enemigo(100 + c * 80, 80 + f * 50) for f in range(3) for c in range(8)]
    balas_jugador, balas_enemigas = [], []
    return {"jugador": jugador, "enemigos": enemigos, "bj": balas_jugador, "be": balas_enemigas}

def actualizar_demo(demo):
    jugador = demo["jugador"]
    enemigos = demo["enemigos"]
    bj = demo["bj"]
    be = demo["be"]

    if enemigos:
        objetivo_x = sum(e.x for e in enemigos) / len(enemigos)
        if jugador.x + jugador.ancho // 2 < objetivo_x - 10:
            jugador.x += jugador.velocidad
        elif jugador.x + jugador.ancho // 2 > objetivo_x + 10:
            jugador.x -= jugador.velocidad

    if jugador.puede_disparar() and random.random() < 0.02:
        bj.append(jugador.disparar())

    for b in bj: b.actualizar()
    for b in be: b.actualizar()
    bj[:] = [b for b in bj if not b.fuera()]
    be[:] = [b for b in be if not b.fuera()]

    for e in enemigos:
        e.actualizar()
        nueva = e.disparar()
        if nueva: be.append(nueva)

    for b in bj[:]:
        for e in enemigos[:]:
            if b.colisiona(e):
                enemigos.remove(e)
                if b in bj: bj.remove(b)
                break

def menu_principal():
    demo = crear_demo()
    opcion = None

    while opcion is None:
        clock.tick(FPS)
        actualizar_demo(demo)

        VENTANA.fill(NEGRO)
        demo["jugador"].dibujar(VENTANA)
        for b in demo["bj"]: b.dibujar(VENTANA)
        for b in demo["be"]: b.dibujar(VENTANA)
        for e in demo["enemigos"]: e.dibujar(VENTANA)

        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        VENTANA.blit(overlay, (0, 0))

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
                    opcion = "jugar"
                elif e.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

    return opcion


def main():
    modo = menu_principal()
    if modo != "jugar": return

    while True:
        jugador = NaveJugador(ANCHO // 2 - 30, ALTO - 50)
        enemigos = [Enemigo(100 + c * 80, 80 + f * 50) for f in range(3) for c in range(8)]
        bj, be = [], []
        puntaje, highscore = 0, cargar_highscore()
        game_over, ganaste = False, False

        while True:
            clock.tick(FPS)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_SPACE and jugador.puede_disparar():
                        bj.append(jugador.disparar())
                    if (game_over or ganaste) and ev.key == pygame.K_r:
                        break  #reinicia sin menú
                    if (game_over or ganaste) and ev.key == pygame.K_m:
                        return main()

            teclas = pygame.key.get_pressed()
            jugador.mover(teclas)

            if not (game_over or ganaste):
                for b in bj: b.actualizar()
                for b in be: b.actualizar()
                bj[:] = [b for b in bj if not b.fuera()]
                be[:] = [b for b in be if not b.fuera()]

                for e in enemigos:
                    e.actualizar()
                    nueva = e.disparar()
                    if nueva: be.append(nueva)

                for b in bj[:]:
                    for e in enemigos[:]:
                        if b.colisiona(e):
                            enemigos.remove(e)
                            if b in bj: bj.remove(b)
                            puntaje += 1
                            if puntaje > highscore:
                                highscore = puntaje
                                guardar_highscore(highscore)
                            break

                for b in be[:]:
                    if jugador.x < b.x < jugador.x + jugador.ancho and jugador.y < b.y < jugador.y + jugador.alto:
                        be.remove(b)
                        game_over = True

                for e in enemigos:
                    if e.colisiona_con_jugador(jugador):
                        game_over = True

                if not enemigos:
                    ganaste = True

            VENTANA.fill(NEGRO)
            jugador.dibujar(VENTANA)
            for e in enemigos: e.dibujar(VENTANA)
            for b in bj: b.dibujar(VENTANA)
            for b in be: b.dibujar(VENTANA)

            fuente = pygame.font.Font(None, 36)
            VENTANA.blit(fuente.render(f"Puntos: {puntaje}", True, BLANCO), (10, 10))
            VENTANA.blit(fuente.render(f"Récord: {highscore}", True, AMARILLO), (10, 50))

            if game_over:
                mostrar_texto("¡GAME OVER!", 60, ROJO)
                mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)
            elif ganaste:
                mostrar_texto("¡GANASTE!", 60, BLANCO)
                mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)

            pygame.display.flip()

            if (game_over or ganaste) and any(e.type == pygame.KEYDOWN and e.key == pygame.K_r for e in pygame.event.get()):
                break  #reinicia juego

if __name__ == "__main__":
    main()