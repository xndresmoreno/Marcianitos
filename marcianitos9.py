import pygame
import sys
import random
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pygame.init()


ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("MARCIANITOS")


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

try:
    
    IMAGEN_NAVE_JUGADOR = pygame.image.load(os.path.join(BASE_DIR, "IMAGENES", "A1.webp")).convert_alpha()
    IMAGEN_MARCIANITO_VERDE = pygame.image.load(os.path.join(BASE_DIR, "IMAGENES", "E1.webp")).convert_alpha()
    IMAGEN_MARCIANITO_AZUL = pygame.image.load(os.path.join(BASE_DIR, "IMAGENES", "O2.webp")).convert_alpha()
    IMAGEN_MARCIANITO_ROJO = pygame.image.load(os.path.join(BASE_DIR, "IMAGENES", "E1.webp")).convert_alpha()
    IMAGEN_BOSS_ALIEN = pygame.image.load(os.path.join(BASE_DIR, "IMAGENES", "finalboss.webp")).convert_alpha()

    
    IMAGEN_FONDO = pygame.image.load(os.path.join(BASE_DIR, "IMAGENES", "fondo.webp")).convert()
    
    
    IMAGEN_POTENCIADOR = pygame.image.load(os.path.join(BASE_DIR, "IMAGENES", "potenciador.webp")).convert_alpha()
    
    
    IMAGEN_EXPLOSION = pygame.image.load(os.path.join(BASE_DIR, "IMAGENES", "explosion.webp")).convert_alpha()


    
    IMAGEN_NAVE_JUGADOR = pygame.transform.scale(IMAGEN_NAVE_JUGADOR, (60, 40)) #un poco más alto
    IMAGEN_MARCIANITO_VERDE = pygame.transform.scale(IMAGEN_MARCIANITO_VERDE, (40, 40))
    IMAGEN_MARCIANITO_AZUL = pygame.transform.scale(IMAGEN_MARCIANITO_AZUL, (40, 40))
    IMAGEN_MARCIANITO_ROJO = pygame.transform.scale(IMAGEN_MARCIANITO_ROJO, (40, 40))
    IMAGEN_BOSS_ALIEN = pygame.transform.scale(IMAGEN_BOSS_ALIEN, (200, 120)) # mas grande para el boss

    
    IMAGEN_FONDO = pygame.transform.scale(IMAGEN_FONDO, (ANCHO, ALTO))
    
    
    IMAGEN_POTENCIADOR = pygame.transform.scale(IMAGEN_POTENCIADOR, (20, 20))

    
    IMAGEN_EXPLOSION = pygame.transform.scale(IMAGEN_EXPLOSION, (40, 40))


except pygame.error as e:
    print(f"Error al cargar una imagen: {e}")
    print("Asegúrate de que las imágenes 'nave_jugador.png', 'marcianito_verde.png', etc.,")
    print("estén en la misma carpeta que el script y sean archivos válidos.")
    sys.exit() 



def cargar_highscore():
    """Carga la puntuación más alta desde un archivo."""
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except ValueError:
            print(f"Advertencia: El archivo {HIGHSCORE_FILE} contiene un valor no válido. Reseteando a 0.")
            return 0
    return 0

def guardar_highscore(puntaje):
    """Guarda la puntuación más alta en un archivo."""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(puntaje))
    except IOError as e:
        print(f"Error al guardar highscore: {e}")

def mostrar_texto(texto, tamano, color, y_offset=0):
    """Muestra texto centrado en la pantalla."""
    fuente = pygame.font.Font(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(ANCHO // 2, ALTO // 2 + y_offset))
    VENTANA.blit(superficie, rect)


class Actor:
    """Clase base para todos los objetos del juego."""
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color #puede ser None si usamos imagen
        self.imagen = None #nueva propiedad para la imagen

    def actualizar(self):
        """Método para actualizar la lógica del actor (sobrescribir en subclases)."""
        pass

    def dibujar(self, superficie):
        """Método para dibujar el actor (sobrescribir en subclases)."""
        pass

class NaveJugador(Actor):
    """Representa la nave del jugador."""
    def __init__(self, x, y):
        super().__init__(x, y, VERDE)
        self.imagen = IMAGEN_NAVE_JUGADOR #asignar la imagen aquí
        self.ancho = self.imagen.get_width() #tomar ancho de la imagen
        self.alto = self.imagen.get_height() #tomar alto de la imagen
        self.velocidad = 7
        self.tiempo_recarga = 500  
        self.ultimo_disparo = 0
        self.vidas = 3
        
        
        self.potenciador_activo = None #tipo de potenciador (ej: 'disparo_triple')
        self.potenciador_tiempo_fin = 0 #cuando caduca el potenciador
        self.duracion_potenciador = 7000 
        

    def mover(self, teclas):
        """Mueve la nave basado en las teclas presionadas."""
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.x < ANCHO - self.ancho:
            self.x += self.velocidad
        
    
        if self.x < 0:
            self.x = 0
        if self.x > ANCHO - self.ancho:
            self.x = ANCHO - self.ancho

    def puede_disparar(self):
        """Comprueba si el tiempo de recarga ha pasado."""
        return pygame.time.get_ticks() - self.ultimo_disparo >= self.tiempo_recarga

    
    def disparar(self):
        """Crea una o más balas y reinicia el temporizador de recarga."""
        self.ultimo_disparo = pygame.time.get_ticks()
        
        
        if self.potenciador_activo == 'disparo_triple':
            # Disparo triple
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
        """Activa un potenciador y reinicia su temporizador."""
        self.potenciador_activo = tipo
        self.potenciador_tiempo_fin = pygame.time.get_ticks() + self.duracion_potenciador

    def actualizar_potenciador(self):
        """Comprueba si el potenciador ha caducado."""
        if self.potenciador_activo:
            if pygame.time.get_ticks() > self.potenciador_tiempo_fin:
                self.potenciador_activo = None 
    

    def dibujar(self, superficie):
        """Dibuja la nave (ahora la imagen)."""
        superficie.blit(self.imagen, (self.x, self.y)) 
        
        fuente = pygame.font.Font(None, 32)
        texto = fuente.render(f"Vidas: {self.vidas}", True, AMARILLO)
        superficie.blit(texto, (ANCHO - 150, 10))

class Bala(Actor):
    """Clase base para las balas."""
    def __init__(self, x, y, color, velocidad):
        super().__init__(x, y, color)
        self.velocidad = velocidad
        self.radio = 4 

    def actualizar(self):
        """Mueve la bala verticalmente."""
        self.y += self.velocidad

    def fuera(self):
        """Comprueba si la bala está fuera de la pantalla."""
        return self.y < 0 or self.y > ALTO

    def dibujar(self, superficie):
        """Dibuja la bala (un círculo)."""
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)

class BalaJugador(Bala):
    """Bala disparada por el jugador."""
    def __init__(self, x, y):
        super().__init__(x, y, BLANCO, -8)

    def colisiona(self, enemigo):
        
        if enemigo.imagen:
            enemigo_rect = enemigo.imagen.get_rect(topleft=(enemigo.x, enemigo.y))
            bala_rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
            return enemigo_rect.colliderect(bala_rect)
        else: 
            return (enemigo.x < self.x < enemigo.x + enemigo.ancho and
                    enemigo.y < self.y < enemigo.y + enemigo.alto)

class BalaEnemigo(Bala):
    """Bala disparada por un enemigo."""
    def __init__(self, x, y):
        super().__init__(x, y, AMARILLO, 5)


class Potenciador(Actor):
    """Representa un item de potenciador que cae."""
    def __init__(self, x, y, tipo):
        super().__init__(x, y) 
        self.tipo = tipo
        self.imagen = IMAGEN_POTENCIADOR 
        self.ancho = self.imagen.get_width() 
        self.alto = self.imagen.get_height() 
        self.velocidad = 3

    def actualizar(self):
        """Mueve el potenciador hacia abajo."""
        self.y += self.velocidad

    def dibujar(self, superficie):
        """Dibuja el potenciador (la imagen)."""
        superficie.blit(self.imagen, (self.x, self.y))

    def fuera(self):
        """Comprueba si está fuera de la pantalla por abajo."""
        return self.y > ALTO

    def colisiona_con_jugador(self, jugador):
        """Comprueba colisión con el jugador."""
        jugador_rect = jugador.imagen.get_rect(topleft=(jugador.x, jugador.y))
        potenciador_rect = self.imagen.get_rect(topleft=(self.x, self.y))
        return jugador_rect.colliderect(potenciador_rect)



class Explosion(Actor):
    """Representa una explosión animada."""
    def __init__(self, x, y, tamano_escala=1.0):
        super().__init__(x, y)
        self.imagen_original = IMAGEN_EXPLOSION
        self.imagen = pygame.transform.scale(self.imagen_original, 
                                            (int(self.imagen_original.get_width() * tamano_escala), 
                                             int(self.imagen_original.get_height() * tamano_escala)))
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.x -= self.ancho // 2 #centrar la explosión donde estaba el enemigo
        self.y -= self.alto // 2
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 300 #duración de la explosión en milisegundos (0.3 segundos)

    def actualizar(self):
        """Comprueba si la explosión ha terminado."""
        return pygame.time.get_ticks() - self.tiempo_inicio > self.duracion

    def dibujar(self, superficie):
        """Dibuja la imagen de la explosión."""
        superficie.blit(self.imagen, (self.x, self.y))

class Enemigo(Actor):
    """Representa un enemigo estándar."""
    def __init__(self, x, y, nivel):
        super().__init__(x, y) #color ya no se pasa directamente
        
        #asigna imagen y vida según el nivel
        if nivel < 3:
            self.imagen = IMAGEN_MARCIANITO_VERDE
            self.vida = 1
        elif nivel < 6:
            self.imagen = IMAGEN_MARCIANITO_AZUL
            self.vida = 2
        else:
            self.imagen = IMAGEN_MARCIANITO_ROJO
            self.vida = 3

        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.velocidad = 2 + nivel * 0.3
        self.direccion = 1  # 1 = derecha, -1 = izquierda
        
        
        prob_calculada = 0.0015 + (nivel * 0.0008)
        self.prob_disparo = min(prob_calculada, 0.02) #límite del 2% por frame (¡muy difícil!)
        

    def actualizar(self):
        """Mueve el enemigo lateralmente y lo baja si toca un borde."""
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= ANCHO:
            self.direccion *= -1
            self.y += 20  #mover hacia abajo

    def disparar(self):
        """Decide aleatoriamente si disparar."""
        if random.random() < self.prob_disparo:
            return [BalaEnemigo(self.x + self.ancho // 2, self.y + self.alto)] #devuelve lista
        return None #devuelve None si no dispara

    def colisiona_con_jugador(self, jugador):
        """Comprueba colisión de rectángulo (enemigo/imagen) a rectángulo (jugador/imagen)."""
        enemigo_rect = self.imagen.get_rect(topleft=(self.x, self.y))
        jugador_rect = jugador.imagen.get_rect(topleft=(jugador.x, jugador.y))
        return enemigo_rect.colliderect(jugador_rect)

    def dibujar(self, superficie):
        """Dibuja el enemigo (su imagen)."""
        superficie.blit(self.imagen, (self.x, self.y))

class Boss(Actor):
    """Representa un enemigo Jefe de nivel."""
    def __init__(self, nivel):
        super().__init__(ANCHO // 2 - 100, 80, MORADO)
        self.imagen = IMAGEN_BOSS_ALIEN #la imagen del boss
        self.ancho = self.imagen.get_width() #ancho de la imagen
        self.alto = self.imagen.get_height() #alto de la imagen
        self.vida_max = 30 + nivel * 10
        self.vida = self.vida_max
        self.velocidad = 3
        self.direccion = 1
        
        
        self.prob_disparo = 0.06 
        
        self.potenciador_soltado_75 = False 
        self.potenciador_soltado_50 = False
        self.potenciador_soltado_25 = False
        

    def actualizar(self):
        """Mueve al jefe lateralmente."""
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= ANCHO:
            self.direccion *= -1

    
    def disparar(self):
        """Decide aleatoriamente si disparar (con más frecuencia que un enemigo normal)."""
        if random.random() < self.prob_disparo:
            x_izquierda = self.x + self.ancho // 4
            x_derecha = self.x + (self.ancho // 4) * 3
            return [
                BalaEnemigo(x_izquierda, self.y + self.alto),
                BalaEnemigo(x_derecha, self.y + self.alto)
            ]
        return None
    

    def colisiona_con_jugador(self, jugador):
        """Comprueba colisión de rectángulo (jefe/imagen) a rectángulo (jugador/imagen)."""
        boss_rect = self.imagen.get_rect(topleft=(self.x, self.y))
        jugador_rect = jugador.imagen.get_rect(topleft=(jugador.x, jugador.y))
        return boss_rect.colliderect(jugador_rect)

    def dibujar(self, superficie):
        """Dibuja al jefe y su barra de vida."""
        superficie.blit(self.imagen, (self.x, self.y)) #la imagen del boss
        #barra de vida del boss
        vida_ratio = self.vida / self.vida_max
        #fondo rojo de la barra de vida
        pygame.draw.rect(superficie, ROJO, (ANCHO // 2 - 200, 20, 400, 20)) 
        #relleno verde de la vida actual
        pygame.draw.rect(superficie, VERDE, (ANCHO // 2 - 200, 20, 400 * vida_ratio, 20))

# MENU PRINCIPAL

def menu_principal():
    """Muestra el menú principal y espera la selección del jugador."""
    while True:
        
        VENTANA.blit(IMAGEN_FONDO, (0, 0))
        
        mostrar_texto("MARCIANITOS", 72, BLANCO, -100)
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
    """Función principal que contiene el bucle del juego."""
    menu_principal()  

    jugador = NaveJugador(ANCHO // 2 - 30, ALTO - 50)
    nivel = 1
    puntaje = 0
    highscore = cargar_highscore()
    game_over = False
    ganaste = False

    def generar_enemigos(nivel_actual):
        """Genera una oleada de enemigos o un jefe."""
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
    

    ejecutando = True
    while ejecutando:
        clock.tick(FPS)

        #eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not game_over and not ganaste:
                    if jugador.puede_disparar():
                        
                        balas_jugador.extend(jugador.disparar())
                
                
                if (game_over or ganaste) and evento.key == pygame.K_r:
                    main()  #reinicia el juego llamando a main() de nuevo
                    return  #sale de esta instancia de main()
                if (game_over or ganaste) and evento.key == pygame.K_m:
                    main()  #main() llama a menu_principal() primero
                    return  #sale de esta instancia de main()
        
        if game_over or ganaste:
            # si el juego terminó, solo dibujamos la pantalla de fin
            pass
        else:
            
            teclas = pygame.key.get_pressed()
            jugador.mover(teclas)
            
            
            jugador.actualizar_potenciador() #Comprueba si el potenciador se acabó
            

            #actualizar balas
            for b in balas_jugador: b.actualizar()
            for b in balas_enemigas: b.actualizar()
            #eliminar balas que salen de la pantalla
            balas_jugador[:] = [b for b in balas_jugador if not b.fuera()]
            balas_enemigas[:] = [b for b in balas_enemigas if not b.fuera()]
            
            
            for p in potenciadores: p.actualizar()
            
            potenciadores[:] = [p for p in potenciadores if not p.fuera()]

            explosiones[:] = [exp for exp in explosiones if not exp.actualizar()]
            

            #enemigos y hacer que disparen
            for e in enemigos:
                e.actualizar()
                nueva_bala = e.disparar()
                if nueva_bala:
                    #ahora usamos .extend() para que funcione con el Boss (que dispara listas)
                    #y con los enemigos (que también devuelven listas)
                    balas_enemigas.extend(nueva_bala)

            #colisiones balas jugador vs enemigos
            for b in balas_jugador[:]:
                for e in enemigos[:]:
                    colision_detectada = False
                    if isinstance(e, Boss):
                        #colisión con Boss
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
                                if e in enemigos: #asegurarse de que todavía está en la lista
                                    enemigos.remove(e)
                                explosiones.append(Explosion(e.x + e.ancho // 2, e.y + e.alto // 2, tamano_escala=2.0)) # Explosión grande para el jefe
                                ganaste = True  
                    else:
                        #colisión con Enemigo normal
                        if b.colisiona(e):
                            e.vida -= 1
                            colision_detectada = True
                            if e.vida <= 0:
                                if e in enemigos: #asegurarse de que todavía está en la lista
                                    enemigos.remove(e)
                                puntaje += 10
                                if puntaje > highscore:
                                    highscore = puntaje
                                    guardar_highscore(highscore)
                                
                                
                                explosiones.append(Explosion(e.x + e.ancho // 2, e.y + e.alto // 2)) #añadir explosión
                                
                                #probabilidad de soltar un potenciador
                                if random.random() < prob_potenciador:
                                    potenciadores.append(Potenciador(e.x + e.ancho // 2, e.y + e.alto // 2, 'disparo_triple'))
                    
                    if colision_detectada:
                        if b in balas_jugador:
                            balas_jugador.remove(b)
                        break  #la bala solo puede golpear a un enemigo
            
            #colisiones balas enemigas vs jugador
            for b in balas_enemigas[:]:
                if (jugador.x < b.x < jugador.x + jugador.ancho and
                        jugador.y < b.y < jugador.y + jugador.alto):
                    
                    if b in balas_enemigas:
                        balas_enemigas.remove(b)
                    
                    jugador.vidas -= 1
                    if jugador.vidas <= 0:
                        game_over = True
                        break #salir del bucle si el jugador muere
            
            #colisiones potenciadores vs jugador
            for p in potenciadores[:]:
                if p.colisiona_con_jugador(jugador):
                    jugador.activar_potenciador(p.tipo)
                    potenciadores.remove(p) 

            #colisiones enemigos vs jugador (contacto físico)
            if not game_over:
                for e in enemigos:
                    if e.colisiona_con_jugador(jugador):
                        jugador.vidas = 0
                        game_over = True
                        break
                    #game over si los enemigos llegan al fondo
                    if e.y + e.alto > jugador.y:
                        jugador.vidas = 0 #asegúrate de que muestre 0 vidas
                        game_over = True
                        break

            if not enemigos and not game_over and not ganaste: #asegurarse de que no esté en estado de "ganaste" por boss
                nivel += 1
                enemigos, es_boss = generar_enemigos(nivel)
                balas_jugador.clear()
                balas_enemigas.clear()
                jugador.x = ANCHO // 2 - jugador.ancho // 2
                
                VENTANA.fill(NEGRO)
                mostrar_texto(f"NIVEL {nivel}", 60, BLANCO)
                pygame.display.flip()
                pygame.time.delay(1500)

        VENTANA.blit(IMAGEN_FONDO, (0, 0)) #ahora dibujamos la imagen de fondo

        jugador.dibujar(VENTANA)
        for e in enemigos: e.dibujar(VENTANA)
        for b in balas_jugador: b.dibujar(VENTANA)
        for b in balas_enemigas: b.dibujar(VENTANA)
        
        for p in potenciadores: p.dibujar(VENTANA) #dibujar los potenciadores



        for exp in explosiones: exp.dibujar(VENTANA) #dibujar las explosiones



        fuente = pygame.font.Font(None, 36)
        VENTANA.blit(fuente.render(f"Puntos: {puntaje}", True, BLANCO), (10, 10))
        VENTANA.blit(fuente.render(f"Récord: {highscore}", True, AMARILLO), (10, 50))
        VENTANA.blit(fuente.render(f"Nivel: {nivel}", True, AZUL), (10, 90))
        

        #mostrar tiempo restante del potenciador
        if jugador.potenciador_activo:
            tiempo_restante = (jugador.potenciador_tiempo_fin - pygame.time.get_ticks()) // 1000 + 1
            texto_pot = fuente.render(f"TRIPLE: {tiempo_restante}s", True, AMARILLO)
            VENTANA.blit(texto_pot, (10, 130))

        if game_over:
            mostrar_texto("¡GAME OVER!", 60, ROJO)
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)
        elif ganaste and es_boss:
            mostrar_texto("¡HAS VENCIDO AL JEFE!", 60, BLANCO)
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)
        elif ganaste and not es_boss: #este caso probablemente no se dará con la lógica actual si solo ganamos con el boss
            mostrar_texto("¡HAS GANADO!", 60, BLANCO)
            mostrar_texto("Presiona R para reiniciar o M para menú", 36, BLANCO, 60)
            

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()