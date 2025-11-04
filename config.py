import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#configuración para pygame
PYGAME_CONFIG = {
    'ANCHO': 800,
    'ALTO': 600,
    'FPS': 60,
    'CAPTION': "MARCIANITOS"
}

COLORES = {
    'NEGRO': (0, 0, 0),
    'BLANCO': (255, 255, 255),
    'VERDE': (0, 255, 0),
    'AZUL': (0, 150, 255),
    'ROJO': (255, 0, 0),
    'AMARILLO': (255, 255, 0),
    'MORADO': (180, 0, 255),
    'GRIS': (100, 100, 100)
}

#archivo de highsocre
ARCHIVOS = {
    'HIGHSCORE_FILE': "highscore.txt"
}

#configuración de imágenes
IMAGENES_CONFIG = {
    'NAVE_JUGADOR': {
        'path': os.path.join("IMAGENES", "E1.webp"),
        'scale': (60, 40)
    },
    'MARCIANITO_LVL1': {
        'path': os.path.join("IMAGENES", "E1.webp"),
        'scale': (40, 40)
    },
    'MARCIANITO_LVL2': {
        'path': os.path.join("IMAGENES", "E1.webp"),
        'scale': (40, 40)
    },
    'MARCIANITO_LVL3': {
        'path': os.path.join("IMAGENES", "O2.webp"),
        'scale': (40, 40)
    },
    'MARCIANITO_LVL4': {
        'path': os.path.join("IMAGENES", "O2.webp"),
        'scale': (40, 40)
    },
    'BOSS_ALIEN': {
        'path': os.path.join("IMAGENES", "finalboss.webp"),
        'scale': (200, 120)
    },
    'FONDO': {
        'path': os.path.join("IMAGENES", "fondo.webp"),
        'scale': (PYGAME_CONFIG['ANCHO'], PYGAME_CONFIG['ALTO'])
    },
    'POTENCIADOR': {
        'path': os.path.join("IMAGENES", "potenciador.webp"),
        'scale': (20, 20)
    },
    'EXPLOSION': {
        'path': os.path.join("IMAGENES", "explosion.webp"),
        'scale': (40, 40)
    }
}

#diccionario para almacenar las imágenes
IMAGENES = {}

def cargar_imagenes():
    """Carga y escala todas las imágenes"""
    try:
        for nombre, config in IMAGENES_CONFIG.items():
            imagen = pygame.image.load(os.path.join(BASE_DIR, config['path']))
            if config['path'].endswith('.webp'):
                imagen = imagen.convert_alpha()
            else:
                imagen = imagen.convert()
            
            IMAGENES[nombre] = pygame.transform.scale(imagen, config['scale'])
        
        return True
    except pygame.error as e:
        print(f"Error al cargar una imagen: {e}")
        print("Asegúrate de que las imágenes estén en la carpeta IMAGENES y sean válidas.")
        return False
