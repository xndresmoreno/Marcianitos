import pygame
import sys
import random
import os
import threading

pygame.init()

#configuración base
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders Avanzado")

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

    def disparar(self):
        self.ultimo_disparo = pygame.time.get_ticks()
        return BalaJugador(self.x + self.ancho // 2, self.y)

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))
        fuente = pygame.font.Font(None, 32)
        texto = fuente.render(f"Vidas: {self.vidas}", True, AMARILLO)
        superficie.blit(texto, (ANCHO - 150, 10))

class Bala:
    def __init__(self, x, y, color, velocidad):
        self.x = x
        self.y = y
        self.color = color
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

class Enemigo:
    def __init__(self, x, y, nivel):
        if nivel < 3:
            color = VERDE
            self.vida = 1
        elif nivel < 6:
            color = AZUL
            self.vida = 2
        else:
            color = ROJO
            self.vida = 3
        self.x, self.y = x, y
        self.color = color
        self.ancho, self.alto = 40, 20
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

class Boss:
    def __init__(self, nivel):
        self.x, self.y = ANCHO // 2 - 100, 80
        self.color = MORADO
        self.ancho, self.alto = 200, 60
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
        #barra de vida
        vida_ratio = self.vida / self.vida_max
        pygame.draw.rect(superficie, ROJO, (200, 20, 400, 20))
        pygame.draw.rect(superficie, VERDE, (200, 20, 400 * vida_ratio, 20))


def demo_background(stop_event):
    jugador = NaveJugador(ANCHO // 2, ALTO - 50)
    enemigos = [Enemigo(100 + c * 80, 80 + f * 50, 1) for f in range(3) for c in range(8)]
    balas_jugador = []
    balas_enemigas = []

    while not stop_event.is_set():
        clock.tick(FPS)
        VENTANA.fill(NEGRO)

        if enemigos:
            objetivo_x = sum(e.x for e in enemigos) / len(enemigos)
            if jugador.x + jugador.ancho // 2 < objetivo_x:
                jugador.x += jugador.velocidad / 2
            elif jugador.x + jugador.ancho // 2 > objetivo_x:
                jugador.x -= jugador.velocidad / 2

        if jugador.puede_disparar() and random.random() < 0.02:
            balas_jugador.append(jugador.disparar())

        for b in balas_jugador: b.actualizar()
        for b in balas_enemigas: b.actualizar()
        balas_jugador = [b for b in balas_jugador if not b.fuera()]
        balas_enemigas = [b for b in balas_enemigas if not b.fuera()]

        for e in enemigos:
            e.actualizar()
            nueva = e.disparar()
            if nueva: balas_enemigas.append(nueva)

        for b in balas_jugador[:]:
            for e in enemigos[:]:
                if b.colisiona(e):
                    enemigos.remove(e)
                    balas_jugador.remove(b)
                    break

        jugador.dibujar(VENTANA)
        for e in enemigos: e.dibujar(VENTANA)
        for b in balas_jugador: b.dibujar(VENTANA)
        for b in balas_enemigas: b.dibujar(VENTANA)

        pygame.display.flip()

 
def menu_principal():
    stop_demo = threading.Event()
    hilo_demo = threading.Thread(target=demo_background, args=(stop_demo,))
    hilo_demo.daemon = True
    hilo_demo.start()

    opcion = None
    while opcion is None:
        mostrar_texto("SPACE INVADERS", 72, BLANCO, -100)
        mostrar_texto("1. JUGAR", 48, BLANCO, -20)
        mostrar_texto("2. SALIR", 48, BLANCO, 40)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                stop_demo.set()
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    opcion = "jugar"
                elif e.key == pygame.K_2:
                    stop_demo.set()
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)

    stop_demo.set()
    pygame.time.wait(200)
    return opcion

def main():
    menu_principal()

    def reiniciar_juego():
        return NaveJugador(ANCHO // 2 - 30, ALTO - 50), 1, 0, cargar_highscore()

    jugador, nivel, puntaje, highscore = reiniciar_juego()
    game_over, ganaste = False, False

    def generar_enemigos(nivel):
        if nivel % 5 == 0:
            return [Boss(nivel)], True
        enemigos = [Enemigo(100 + c * 80, 80 + f * 50, nivel) for f in range(3) for c in range(8)]
        return enemigos, False

    enemigos, es_boss = generar_enemigos(nivel)
    bj, be = [], []

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and jugador.puede_disparar():
                    bj.append(jugador.disparar())
                if (game_over or ganaste) and e.key == pygame.K_r:
                    return main()  #reinicia desde nivel 1
                if (game_over or ganaste) and e.key == pygame.K_m:
                    return main()

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        if not game_over and not ganaste:
            for b in bj: b.actualizar()
            for b in be: b.actualizar()
            bj = [b for b in bj if not b.fuera()]
            be = [b for b in be if not b.fuera()]

            for enemigo in enemigos:
                enemigo.actualizar()
                nueva = enemigo.disparar()
                if nueva: be.append(nueva)

            for b in bj[:]:
                for enemigo in enemigos[:]:
                    if isinstance(enemigo, Boss):
                        if enemigo.x < b.x < enemigo.x + enemigo.ancho and enemigo.y < b.y < enemigo.y + enemigo.alto:
                            enemigo.vida -= 1
                            bj.remove(b)
                            if enemigo.vida <= 0:
                                enemigos.remove(enemigo)
                                ganaste = True
                            break
                    elif b.colisiona(enemigo):
                        enemigo.vida -= 1
                        if enemigo.vida <= 0:
                            enemigos.remove(enemigo)
                            puntaje += 1
                            if puntaje > highscore:
                                highscore = puntaje
                                guardar_highscore(highscore)
                        bj.remove(b)
                        break

            for b in be[:]:
                if jugador.x < b.x < jugador.x + jugador.ancho and jugador.y < b.y < jugador.y + jugador.alto:
                    be.remove(b)
                    jugador.vidas -= 1
                    if jugador.vidas <= 0:
                        game_over = True

            for enemigo in enemigos:
                if hasattr(enemigo, 'colisiona_con_jugador') and enemigo.colisiona_con_jugador(jugador):
                    jugador.vidas = 0
                    game_over = True

            if not enemigos and not es_boss:
                nivel += 1
                enemigos, es_boss = generar_enemigos(nivel)
                bj.clear(); be.clear()
                jugador.x = ANCHO // 2 - jugador.ancho // 2
                mostrar_texto(f"NIVEL {nivel}", 60, BLANCO)
                pygame.display.flip()
                pygame.time.delay(1500)

        VENTANA.fill(NEGRO)
        jugador.dibujar(VENTANA)
        for e in enemigos: e.dibujar(VENTANA)
        for b in bj: b.dibujar(VENTANA)
        for b in be: b.dibujar(VENTANA)

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