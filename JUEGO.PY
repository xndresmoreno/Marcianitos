import pygame #libreria para crear juegos en 2D
import random #para generar situaciones aleatorias 

pygame.init() #inicializa los modulos del Pygame
pygame.mixer.init() #para inicializar el sonido que en el futuro añadiremos

#fondo = pygame.image.
#laser_sonido= 
#explosion_sonido=
#golpe_sonido=

#BUCLE QUE EJECUTA LA EXPLOSION ANIMADA
explosion_list = []
for i in range (1,13):
    explosion = pygame.image.load
    explosion_list.append(explosion)

#TAMAÑO DE LA VENTANA DEL JUEGO 
width = fondo.get_width() #devuelve el ancho 
height = fondo.get_height() #devuelve el alto
window = pygame.display.set_mode((width, height)) #crea la ventana del juego


#CARGAMOS AL JUGADOR Y LO COLOCAMOS CENTROADO HORIZONTALMENTE CERCA DE LA PARTE INFERIOR DE LA PANTALLA
class Jugador (pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image = pygame.image.load().convert_alpha()
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.centery = height - 50 
        self.velocidad_x = 0 
        self.vida = 100

        #METODO PARA ACTUALIZAR EL JUGADOR, MOVERLO Y LIMITARLO EN LOS BORDES 



        #METODO PARA DISPARAR 
        
#REPRESENTA A LOS ENEMIGOS, SE COLOCAN EN UNA POSICION ALEATORIA, DESDE ARRIBA, CON UAN VELOCIDAD ALEATORAIA 
class Enemigos (pygame.sprite.Sprite):
    def __init__ (self, x, y):
        super().__init__()
        self.image = pygame.image.load
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, width-50)
        self.rect.y = 10
        self.velocidad_y = random.randrange(-5, 20)

        #METODO PARA ACTUALIZAR EL ENEMIGO 
        
        #METODO PARA DISPARAR ENEMIGOS

#REPRESENTA LAS BALAS QUE DISPARA EL JUGADOR, SE MUEVEN HACIA ARRIBA 
class Balas(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.image.load().convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.y = y 
        self.velocidad = -18

        #metodo actualizar 

#REPRESENTA LAS BALAS QUE DISPARAN LOS ENEMIGOS, SE MUEVEN HACIA ABAJO 
class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load().convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = random.randrange(10, width)
        self.velocidad_y = 4

        #metodo actualizar 

#SE USA PARA ANIMAR UNA EXPLOSION EN LA POSICION DONDE UN ENEMIGO MUERE O UNA BALA IMPACTA 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = explosion_list[0]
        img_scala = pygame.transform.scale(self.image, (20,20))
        self.rect = img_scala.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_explo = 30
        self.frames = 0 

        #METODO PARA ACTUALIZAR

#CREAMOS UNOS GRUPOS QUE PERMIEN MANEJAR Y DIBUJAR VARIOS OBJETOS A LA VEZ 
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()


#CREA A EL JUGADOR Y LO AÑADE A LOS GRUPOS 
player = Jugador()
grupo_jugador.add(player)
grupo_balas_jugador.add(player)

#CREA A LOS ENEMIGOS 
for x in range (10):
    enemigo = Enemigos(10,10)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)

#FUNCION DE EJECUCION 

