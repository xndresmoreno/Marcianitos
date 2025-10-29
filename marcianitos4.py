import pygame
import sys
import random

#Inicializar pygame
pygame.init()

#Configuración de pantalla
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders con Balas Heredadas")

#Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

#FPS
FPS = 60
clock = pygame.time.Clock()



#Clase base Actor

class Actor:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def actualizar(self):
        pass

    def dibujar(self, superficie):
        pass



#Clase de la Nave del Jugador

class NaveJugador(Actor):
    def __init__(self, x, y, ancho=60, alto=20, color=VERDE, velocidad=7, tiempo_recarga=500):
        super().__init__(x, y, color)
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
        self.tiempo_recarga = tiempo_recarga  # milisegundos
        self.ultimo_disparo = 0  # tiempo del último disparo

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.x < ANCHO - self.ancho:
            self.x += self.velocidad

    def puede_disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        return tiempo_actual - self.ultimo_disparo >= self.tiempo_recarga

    def disparar(self):
        self.ultimo_disparo = pygame.time.get_ticks()
        bala_x = self.x + self.ancho // 2
        bala_y = self.y
        return BalaJugador(bala_x, bala_y)

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))



#Clase base Bala

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



#Bala del jugador (rápida, hacia arriba)

class BalaJugador(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, BLANCO, radio=4, velocidad=-8)

    def colisiona_con(self, enemigo):
        return (enemigo.x < self.x < enemigo.x + enemigo.ancho and
                enemigo.y < self.y < enemigo.y + enemigo.alto)



#Bala del enemigo (más lenta, hacia abajo)

class BalaEnemigo(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, AMARILLO, radio=4, velocidad=5)



#Clase Enemigo

class Enemigo(Actor):
    def __init__(self, x, y, ancho=40, alto=20, color=ROJO, velocidad=3, prob_disparo=0.001):
        super().__init__(x, y, color)
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
        self.direccion = 1
        self.prob_disparo = prob_disparo  # probabilidad por frame de disparar

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

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))



#Bucle principal

def main():
    jugador = NaveJugador(ANCHO // 2 - 30, ALTO - 50)
    balas_jugador = []
    balas_enemigas = []
    enemigos = []

    #Crear enemigos
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

        #EVENTOS 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and jugador.puede_disparar():
                    balas_jugador.append(jugador.disparar())

        #MOVIMIENTO JUGADOR
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        #ACTUALIZAR BALAS
        for bala in balas_jugador:
            bala.actualizar()
        for bala in balas_enemigas:
            bala.actualizar()

        balas_jugador = [b for b in balas_jugador if not b.fuera_de_pantalla()]
        balas_enemigas = [b for b in balas_enemigas if not b.fuera_de_pantalla()]

        #ACTUALIZAR ENEMIGOS
        for enemigo in enemigos:
            enemigo.actualizar()
            nueva_bala = enemigo.disparar()
            if nueva_bala:
                balas_enemigas.append(nueva_bala)

        #COLISIONES: BALAS JUGADOR vs ENEMIGOS
        for bala in balas_jugador[:]:
            for enemigo in enemigos[:]:
                if bala.colisiona_con(enemigo):
                    enemigos.remove(enemigo)
                    balas_jugador.remove(bala)
                    break

        #COLISIONES: BALAS ENEMIGAS vs JUGADOR
        for bala in balas_enemigas[:]:
            if (jugador.x < bala.x < jugador.x + jugador.ancho and
                    jugador.y < bala.y < jugador.y + jugador.alto):
                balas_enemigas.remove(bala)
                fuente = pygame.font.Font(None, 60)
                texto = fuente.render("¡GAME OVER!", True, ROJO)
                VENTANA.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 30))
                pygame.display.flip()
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

        #DIBUJAR TODO 
        jugador.dibujar(VENTANA)
        for bala in balas_jugador:
            bala.dibujar(VENTANA)
        for bala in balas_enemigas:
            bala.dibujar(VENTANA)
        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)

        #GANAR
        if not enemigos:
            fuente = pygame.font.Font(None, 60)
            texto = fuente.render("¡GANASTE!", True, BLANCO)
            VENTANA.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
