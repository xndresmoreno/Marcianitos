import pygame
import sys
import random
import os
from config import *

# Inicializar pygame
pygame.init()

# Configurar ventana
VENTANA = pygame.display.set_mode((PYGAME_CONFIG['ANCHO'], PYGAME_CONFIG['ALTO']))
pygame.display.set_caption(PYGAME_CONFIG['CAPTION'])
clock = pygame.time.Clock()

# Cargar imágenes
if not cargar_imagenes():
    sys.exit()

# El resto del código permanece igual, pero reemplaza las referencias a las variables antiguas
# Por ejemplo:
# ANTES: IMAGEN_NAVE_JUGADOR -> AHORA: IMAGENES['NAVE_JUGADOR']
# ANTES: ANCHO -> AHORA: PYGAME_CONFIG['ANCHO']
# ANTES: BLANCO -> AHORA: COLORES['BLANCO']

def cargar_highscore():
    if os.path.exists(ARCHIVOS['HIGHSCORE_FILE']):
        try:
            with open(ARCHIVOS['HIGHSCORE_FILE'], "r") as f:
                return int(f.read().strip())
        except ValueError:
            print(f"Advertencia: El archivo {ARCHIVOS['HIGHSCORE_FILE']} contiene un valor no válido. Reseteando a 0.")
            return 0
    return 0

def guardar_highscore(puntaje):
    try:
        with open(ARCHIVOS['HIGHSCORE_FILE'], "w") as f:
            f.write(str(puntaje))
    except IOError as e:
        print(f"Error al guardar highscore: {e}")

def mostrar_texto(texto, tamano, color, y_offset=0):
    fuente = pygame.font.Font(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(PYGAME_CONFIG['ANCHO'] // 2, PYGAME_CONFIG['ALTO'] // 2 + y_offset))
    VENTANA.blit(superficie, rect)

class Actor:
    def __init__(self, x, y, color=None): 
        self.x = x
        self.y = y
        self.color = color 
        self.imagen = None 

    def actualizar(self):
        pass

    def dibujar(self, superficie):
        pass

class DEMO(Actor):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocidad = 0
        self.direccion = 1
        self.ancho = 0
        self.alto = 0
        
    def actualizar(self):
        """Método base para movimiento horizontal con rebote en los bordes"""
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= PYGAME_CONFIG['ANCHO']:
            self.direccion *= -1
            
    def dibujar(self, superficie):
        """Método base para dibujar la imagen del objeto"""
        if self.imagen:
            superficie.blit(self.imagen, (self.x, self.y))

class DemoNave(DEMO):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imagen = IMAGENES['NAVE_JUGADOR']
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.velocidad = 3

    def disparar(self):
        return BalaJugador(self.x + self.ancho // 2, self.y)

class DemoEnemigo(DEMO):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imagen = IMAGENES['MARCIANITO_LVL1']
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.velocidad = 2

class NaveJugador(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, COLORES['VERDE'])
        self.imagen = IMAGENES['NAVE_JUGADOR']
        self.ancho = self.imagen.get_width() 
        self.alto = self.imagen.get_height() 
        self.velocidad = 7
        self.tiempo_recarga = 500  
        self.ultimo_disparo = 0
        self.vidas = 3
        
        self.potenciador_activo = None 
        self.potenciador_tiempo_fin = 0 
        self.duracion_potenciador = 7000 

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.x < PYGAME_CONFIG['ANCHO'] - self.ancho:
            self.x += self.velocidad
        
        if self.x < 0:
            self.x = 0
        if self.x > PYGAME_CONFIG['ANCHO'] - self.ancho:
            self.x = PYGAME_CONFIG['ANCHO'] - self.ancho

    def puede_disparar(self):
        return pygame.time.get_ticks() - self.ultimo_disparo >= self.tiempo_recarga

    def disparar(self):
        self.ultimo_disparo = pygame.time.get_ticks()
        
        if self.potenciador_activo == 'disparo_triple':
            x_izquierda = self.x + 10
            x_centro = self.x + self.ancho // 2
            x_derecha = self.x + self.ancho - 10
            return [
                BalaJugador(x_izquierda, self.y),
                BalaJugador(x_centro, self.y),
                BalaJugador(x_derecha, self.y)
            ]
        else:
            return [BalaJugador(self.x + self.ancho // 2, self.y)]

    def activar_potenciador(self, tipo):
        self.potenciador_activo = tipo
        self.potenciador_tiempo_fin = pygame.time.get_ticks() + self.duracion_potenciador

    def actualizar_potenciador(self):
        if self.potenciador_activo:
            if pygame.time.get_ticks() > self.potenciador_tiempo_fin:
                self.potenciador_activo = None 

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, self.y)) 
        fuente = pygame.font.Font(None, 32)
        texto = fuente.render(f"Vidas: {self.vidas}", True, COLORES['AMARILLO'])
        superficie.blit(texto, (PYGAME_CONFIG['ANCHO'] - 150, 10))

class Bala(Actor):
    def __init__(self, x, y, color, velocidad):
        super().__init__(x, y, color)
        self.velocidad = velocidad
        self.radio = 4 

    def actualizar(self):
        self.y += self.velocidad

    def fuera(self):
        return self.y < 0 or self.y > PYGAME_CONFIG['ALTO']

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)

class BalaJugador(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, COLORES['BLANCO'], -8)

    def colisiona(self, enemigo):
        if enemigo.imagen:
            enemigo_rect = enemigo.imagen.get_rect(topleft=(enemigo.x, enemigo.y))
            bala_rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
            return enemigo_rect.colliderect(bala_rect)
        else: 
            return (enemigo.x < self.x < enemigo.x + enemigo.ancho and
                    enemigo.y < self.y < enemigo.y + enemigo.alto)

class BalaEnemigo(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, COLORES['AMARILLO'], 5)

class Potenciador(Actor):
    def __init__(self, x, y, tipo):
        super().__init__(x, y) 
        self.tipo = tipo
        self.imagen = IMAGENES['POTENCIADOR']
        self.ancho = self.imagen.get_width() 
        self.alto = self.imagen.get_height() 
        self.velocidad = 3

    def actualizar(self):
        self.y += self.velocidad

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, self.y))

    def fuera(self):
        return self.y > PYGAME_CONFIG['ALTO']

    def colisiona_con_jugador(self, jugador):
        jugador_rect = jugador.imagen.get_rect(topleft=(jugador.x, jugador.y))
        potenciador_rect = self.imagen.get_rect(topleft=(self.x, self.y))
        return jugador_rect.colliderect(potenciador_rect)

class Explosion(Actor):
    def __init__(self, x, y, tamano_escala=1.0):
        super().__init__(x, y)
        self.imagen_original = IMAGENES['EXPLOSION']
        self.imagen = pygame.transform.scale(self.imagen_original, 
                                            (int(self.imagen_original.get_width() * tamano_escala), 
                                             int(self.imagen_original.get_height() * tamano_escala)))
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.x -= self.ancho // 2 
        self.y -= self.alto // 2
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 300 

    def actualizar(self):
        return pygame.time.get_ticks() - self.tiempo_inicio > self.duracion

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, self.y))

class Enemigo(Actor):
    def __init__(self, x, y, nivel):
        super().__init__(x, y) 
        
        if nivel == 1:
            self.imagen = IMAGENES['MARCIANITO_LVL1']
            self.vida = 1
        elif nivel == 2:
            self.imagen = IMAGENES['MARCIANITO_LVL2']
            self.vida = 1
        elif nivel == 3:
            self.imagen = IMAGENES['MARCIANITO_LVL3']
            self.vida = 2
        elif nivel == 4:
            self.imagen = IMAGENES['MARCIANITO_LVL4']
            self.vida = 2
        else: 
            self.imagen = IMAGENES['MARCIANITO_LVL4']
            self.vida = 3

        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.velocidad = 2 + nivel * 0.3
        self.direccion = 1  
        
        prob_calculada = 0.0015 + (nivel * 0.0008)
        self.prob_disparo = min(prob_calculada, 0.02) 

    def actualizar(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= PYGAME_CONFIG['ANCHO']:
            self.direccion *= -1
            self.y += 20  

    def disparar(self):
        if random.random() < self.prob_disparo:
            return [BalaEnemigo(self.x + self.ancho // 2, self.y + self.alto)] 
        return None 

    def colisiona_con_jugador(self, jugador):
        enemigo_rect = self.imagen.get_rect(topleft=(self.x, self.y))
        jugador_rect = jugador.imagen.get_rect(topleft=(jugador.x, jugador.y))
        return enemigo_rect.colliderect(jugador_rect)

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, self.y))

class Boss(Actor):
    def __init__(self, nivel):
        super().__init__(PYGAME_CONFIG['ANCHO'] // 2 - 100, 80, COLORES['MORADO'])
        self.imagen = IMAGENES['BOSS_ALIEN']
        self.ancho = self.imagen.get_width() 
        self.alto = self.imagen.get_height() 
        self.vida_max = 30 + nivel * 10
        self.vida = self.vida_max
        self.velocidad = 3
        self.direccion = 1
        
        self.prob_disparo = 0.06 
        self.potenciador_soltado_75 = False 
        self.potenciador_soltado_50 = False
        self.potenciador_soltado_25 = False

    def actualizar(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= PYGAME_CONFIG['ANCHO']:
            self.direccion *= -1

    def disparar(self):
        if random.random() < self.prob_disparo:
            x_izquierda = self.x + self.ancho // 4
            x_derecha = self.x + (self.ancho // 4) * 3
            return [
                BalaEnemigo(x_izquierda, self.y + self.alto),
                BalaEnemigo(x_derecha, self.y + self.alto)
            ]
        return None 

    def colisiona_con_jugador(self, jugador):
        boss_rect = self.imagen.get_rect(topleft=(self.x, self.y))
        jugador_rect = jugador.imagen.get_rect(topleft=(jugador.x, jugador.y))
        return boss_rect.colliderect(jugador_rect)

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, self.y)) 
        vida_ratio = self.vida / self.vida_max
        pygame.draw.rect(superficie, COLORES['ROJO'], (PYGAME_CONFIG['ANCHO'] // 2 - 200, 20, 400, 20)) 
        pygame.draw.rect(superficie, COLORES['VERDE'], (PYGAME_CONFIG['ANCHO'] // 2 - 200, 20, 400 * vida_ratio, 20))

def menu_principal():
    demo_nave = DemoNave(PYGAME_CONFIG['ANCHO'] // 2 - 30, PYGAME_CONFIG['ALTO'] - 100)
    
    def crear_enemigos_demo():
        return [DemoEnemigo(150 + c * 80, 100) for c in range(6)]
        
    demo_enemigos = crear_enemigos_demo()
    demo_balas = []
    demo_explosiones = []

    while True:
        clock.tick(PYGAME_CONFIG['FPS'])

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 'QUIT' 
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    return 'PLAY'  
                elif e.key == pygame.K_2:
                    return 'QUIT'  
        
        demo_nave.actualizar()
        
        if random.random() < 0.02: 
            demo_balas.append(demo_nave.disparar())
            
        for b in demo_balas: b.actualizar()
        demo_balas[:] = [b for b in demo_balas if not b.fuera()]
        
        for e in demo_enemigos: e.actualizar()
        
        demo_explosiones[:] = [exp for exp in demo_explosiones if not exp.actualizar()]
        
        for b in demo_balas[:]:
            for e in demo_enemigos[:]:
                if b.colisiona(e):
                    if b in demo_balas:
                        demo_balas.remove(b)
                    if e in demo_enemigos:
                        demo_enemigos.remove(e)
                    demo_explosiones.append(Explosion(e.x + e.ancho // 2, e.y + e.alto // 2))
                    break 
        
        if not demo_enemigos:
            demo_enemigos = crear_enemigos_demo()
            
        VENTANA.blit(IMAGENES['FONDO'], (0, 0))
        
        demo_nave.dibujar(VENTANA)
        for e in demo_enemigos: e.dibujar(VENTANA)
        for b in demo_balas: b.dibujar(VENTANA)
        for exp in demo_explosiones: exp.dibujar(VENTANA)

        mostrar_texto("MARCIANITOS", 72, COLORES['BLANCO'], -100)
        mostrar_texto("1. JUGAR", 48, COLORES['BLANCO'], -20)
        mostrar_texto("2. SALIR", 48, COLORES['BLANCO'], 40)
        
        pygame.display.flip() 

def game_loop():
    jugador = NaveJugador(PYGAME_CONFIG['ANCHO'] // 2 - 30, PYGAME_CONFIG['ALTO'] - 50)
    nivel = 1
    puntaje = 0
    highscore = cargar_highscore()
    game_over = False
    ganaste = False

    def generar_enemigos(nivel_actual):
        if nivel_actual % 5 == 0:
            return [Boss(nivel_actual)], True
        
        enemigos = [Enemigo(50 + c * 70, 80 + f * 50, nivel_actual) for f in range(3) for c in range(10)]
        return enemigos, False

    enemigos, es_boss = generar_enemigos(nivel)
    balas_jugador = []
    balas_enemigas = []
    potenciadores = [] 
    prob_potenciador = 0.1 
    explosiones = [] 

    while True: 
        clock.tick(PYGAME_CONFIG['FPS'])

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'QUIT' 
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not game_over and not ganaste:
                    if jugador.puede_disparar():
                        balas_jugador.extend(jugador.disparar())
                
                if (game_over or ganaste) and evento.key == pygame.K_r:
                    return 'RESTART'  
                if (game_over or ganaste) and evento.key == pygame.K_m:
                    return 'MENU'  
        
        if game_over or ganaste:
            pass
        else:
            teclas = pygame.key.get_pressed()
            jugador.mover(teclas)
            
            jugador.actualizar_potenciador() 

            for b in balas_jugador: b.actualizar()
            for b in balas_enemigas: b.actualizar()
            balas_jugador[:] = [b for b in balas_jugador if not b.fuera()]
            balas_enemigas[:] = [b for b in balas_enemigas if not b.fuera()]
            
            for p in potenciadores: p.actualizar()
            potenciadores[:] = [p for p in potenciadores if not p.fuera()]

            explosiones[:] = [exp for exp in explosiones if not exp.actualizar()]

            for e in enemigos:
                e.actualizar()
                nueva_bala = e.disparar()
                if nueva_bala:
                    balas_enemigas.extend(nueva_bala)

            for b in balas_jugador[:]:
                for e in enemigos[:]:
                    colision_detectada = False
                    if isinstance(e, Boss):
                        if e.x < b.x < e.x + e.ancho and e.y < b.y < e.y + e.alto:
                            e.vida -= 1
                            colision_detectada = True
                            
                            if e.vida <= e.vida_max * 0.75 and not e.potenciador_soltado_75:
                                potenciadores.append(Potenciador(e.x + e.ancho // 2, e.y + e.alto, 'disparo_triple'))
                                e.potenciador_soltado_75 = True
                            
                            if e.vida <= e.vida_max * 0.50 and not e.potenciador_soltado_50:
                                potenciadores.append(Potenciador(e.x + e.ancho // 2, e.y + e.alto, 'disparo_triple'))
                                e.potenciador_soltado_50 = True
                                
                            if e.vida <= e.vida_max * 0.25 and not e.potenciador_soltado_25:
                                potenciadores.append(Potenciador(e.x + e.ancho // 2, e.y + e.alto, 'disparo_triple'))
                                e.potenciador_soltado_25 = True
                            
                            if e.vida <= 0:
                                if e in enemigos: 
                                    enemigos.remove(e)
                                explosiones.append(Explosion(e.x + e.ancho // 2, e.y + e.alto // 2, tamano_escala=2.0)) 
                                ganaste = True  
                    else:
                        if b.colisiona(e):
                            e.vida -= 1
                            colision_detectada = True
                            if e.vida <= 0:
                                if e in enemigos: 
                                    enemigos.remove(e)
                                puntaje += 10
                                if puntaje > highscore:
                                    highscore = puntaje
                                    guardar_highscore(highscore)
                                
                                explosiones.append(Explosion(e.x + e.ancho // 2, e.y + e.alto // 2)) 

                                if random.random() < prob_potenciador:
                                    potenciadores.append(Potenciador(e.x + e.ancho // 2, e.y + e.alto // 2, 'disparo_triple'))
                    
                    if colision_detectada:
                        if b in balas_jugador:
                            balas_jugador.remove(b)
                        break  
            
            for b in balas_enemigas[:]:
                if (jugador.x < b.x < jugador.x + jugador.ancho and
                        jugador.y < b.y < jugador.y + jugador.alto):
                    
                    if b in balas_enemigas:
                        balas_enemigas.remove(b)
                    
                    jugador.vidas -= 1
                    if jugador.vidas <= 0:
                        game_over = True
                        break 
            
            for p in potenciadores[:]:
                if p.colisiona_con_jugador(jugador):
                    jugador.activar_potenciador(p.tipo)
                    potenciadores.remove(p)

            if not game_over:
                for e in enemigos:
                    if e.colisiona_con_jugador(jugador):
                        jugador.vidas = 0
                        game_over = True
                        break
                    if e.y + e.alto > jugador.y:
                        jugador.vidas = 0 
                        game_over = True
                        break

            if not enemigos and not game_over and not ganaste: 
                nivel += 1
                enemigos, es_boss = generar_enemigos(nivel)
                balas_jugador.clear()
                balas_enemigas.clear()
                jugador.x = PYGAME_CONFIG['ANCHO'] // 2 - jugador.ancho // 2
                
                VENTANA.fill(COLORES['NEGRO'])
                mostrar_texto(f"NIVEL {nivel}", 60, COLORES['BLANCO'])
                pygame.display.flip()
                pygame.time.delay(1500)

        VENTANA.blit(IMAGENES['FONDO'], (0, 0))

        jugador.dibujar(VENTANA)
        for e in enemigos: e.dibujar(VENTANA)
        for b in balas_jugador: b.dibujar(VENTANA)
        for b in balas_enemigas: b.dibujar(VENTANA)
        for p in potenciadores: p.dibujar(VENTANA) 
        for exp in explosiones: exp.dibujar(VENTANA) 

        fuente = pygame.font.Font(None, 36)
        VENTANA.blit(fuente.render(f"Puntos: {puntaje}", True, COLORES['BLANCO']), (10, 10))
        VENTANA.blit(fuente.render(f"Récord: {highscore}", True, COLORES['AMARILLO']), (10, 50))
        VENTANA.blit(fuente.render(f"Nivel: {nivel}", True, COLORES['AZUL']), (10, 90))
        
        if jugador.potenciador_activo:
            tiempo_restante = (jugador.potenciador_tiempo_fin - pygame.time.get_ticks()) // 1000 + 1
            texto_pot = fuente.render(f"TRIPLE: {tiempo_restante}s", True, COLORES['AMARILLO'])
            VENTANA.blit(texto_pot, (10, 130))

        if game_over:
            mostrar_texto("¡GAME OVER!", 60, COLORES['ROJO'])
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, COLORES['BLANCO'], 60)
        elif ganaste and es_boss:
            mostrar_texto("¡HAS VENCIDO AL JEFE!", 60, COLORES['BLANCO'])
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, COLORES['BLANCO'], 60)
        elif ganaste and not es_boss: 
            mostrar_texto("¡HAS GANADO!", 60, COLORES['BLANCO'])
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, COLORES['BLANCO'], 60)
            

        pygame.display.flip()
    
if __name__ == "__main__":
    estado_actual = 'MENU' 
    while True:
        if estado_actual == 'MENU':
            estado_actual = menu_principal()
        elif estado_actual == 'PLAY':
            estado_actual = game_loop()
        elif estado_actual == 'RESTART':
            estado_actual = game_loop() 
        elif estado_actual == 'QUIT':
            break 
    
    pygame.quit()
    sys.exit()
