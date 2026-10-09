
import pygame
import numpy as np
from PIL import Image
import os
import sys
from pathlib import Path

# Directorio base del script (parte1/)
BASE_DIR = Path(__file__).resolve().parent

# Configuracion de posiciones y rotaciones de cada figura
# Se midieron los angulos visualmente sobre la plantilla y se probaron
# hasta que cada imagen quedara alineada dentro del cuadro negro.
#
# En PIL: rotate(+N) = sentido antihorario (CCW), rotate(-N) = horario (CW)
#
# f1 - Lena     (x=[10,142],  y=[20,151]):  -11 grados (inclina derecha)
# f2 - Gato     (x=[204,332], y=[22,151]):   +9 grados (inclina izquierda)
# f3 - Flor     (x=[380,537], y=[13,171]):  -39 grados (gran inclinacion derecha)
# f4 - Mariposa (x=[601,746], y=[14,159]):  +22 grados (inclinacion izquierda)

FIGURAS_CONFIG = [
    # (x_inicio, x_fin en figuras.png, centro_x, centro_y, angulo, nombre)
    (3,   220, 75.8,  85.3, -11, "Lena"),
    (242, 483, 268.1, 86.7,  +9, "Gato"),
    (503, 722, 459.1, 92.2, -39, "Flor"),
    (733, 979, 673.2, 86.4, +22, "Mariposa"),
]

TAM_CUADRO = 113  # lado del cuadro negro en la plantilla (en pixeles)

PLANTILLA_PATH = str(BASE_DIR / "imagenproyecto" / "plantilla.png")
FIGURAS_PATH   = str(BASE_DIR / "imagenproyecto" / "figuras.png")
OUTPUT_PATH    = str(BASE_DIR / "imagenproyecto" / "resultado_etapa2.png")


# FUNCIONES DE PROCESAMIENTO DE IMAGENES (PIL)

def extraer_figura(figuras_img, x_start, x_end):
    # Recortar la figura desde la imagen con todas las figuras
    return figuras_img.crop((x_start, 0, x_end, figuras_img.height))

def redimensionar_y_rotar(imagen, side, angulo):
    # Redimensionar al tamanio del cuadro en la plantilla
    img_resized = imagen.resize((side, side), Image.LANCZOS).convert('RGBA')

    if angulo == 0:
        return img_resized

    # Rotar con expand=True para no recortar las esquinas de la imagen
    img_rotated = img_resized.rotate(angulo, resample=Image.BICUBIC, expand=True)
    return img_rotated

def componer_resultado_pil():
    # Cargar imagenes base
    plantilla = Image.open(PLANTILLA_PATH).convert('RGBA')
    figuras   = Image.open(FIGURAS_PATH).convert('RGBA')

    resultado = plantilla.copy()

    print("  Procesando figuras:")
    for x_start, x_end, cx, cy, angulo, nombre in FIGURAS_CONFIG:
        print(f"    {nombre}: recorte [{x_start}:{x_end}], "
              f"centro [{cx:.1f}, {cy:.1f}], "
              f"rotacion {angulo} grados")

        #Extraer figura
        figura = extraer_figura(figuras, x_start, x_end)

        #Redimensionar y rotar completa (sin recortar esquinas)
        figura_rot = redimensionar_y_rotar(figura, TAM_CUADRO, angulo)

        #Pegar centrada en el cuadro correspondiente usando su mascara alfa
        rw, rh = figura_rot.size
        pos_x = int(round(cx - rw / 2.0))
        pos_y = int(round(cy - rh / 2.0))
        resultado.paste(figura_rot, (pos_x, pos_y), mask=figura_rot)

    return resultado


# VISUALIZACION CON PYGAME

def mostrar_con_pygame(resultado_pil):

    pygame.init()

    # Convertir PIL a Pygame surface
    resultado_rgb = resultado_pil.convert('RGB')
    res_w, res_h = resultado_rgb.size

    PADDING = 20
    WIN_W = res_w + PADDING * 2
    WIN_H = res_h + PADDING * 2

    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Proyecto #1 - Etapa 2: Composicion de Imagenes")

    BG_COLOR = (255, 255, 255)

    res_bytes = resultado_rgb.tobytes()
    res_surface = pygame.image.fromstring(res_bytes, (res_w, res_h), 'RGB')

    clock = pygame.time.Clock()
    running = True

    print("  Ventana abierta. Presiona ESC o cierra la ventana para terminar.")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BG_COLOR)

        # Centrar la imagen en la ventana
        img_x = (WIN_W - res_w) // 2
        img_y = (WIN_H - res_h) // 2
        screen.blit(res_surface, (img_x, img_y))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# MAIN

def main():

    # Verificar archivos
    for f in [PLANTILLA_PATH, FIGURAS_PATH]:
        if not os.path.exists(f):
            print(f"ERROR: No se encontro '{f}'")
            sys.exit(1)

    resultado = componer_resultado_pil()
    resultado.save(OUTPUT_PATH)
    mostrar_con_pygame(resultado)

if __name__ == "__main__":
    main()
