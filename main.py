import pygame
import sys
import subprocess
from pathlib import Path

pygame.init()

ANCHO = 850
ALTO = 650

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Proyecto 1 - Vision por Computador")

BLANCO = (255, 255, 255)
FONDO = (20, 26, 42)
AZUL = (45, 105, 190)
AZUL_CLARO = (65, 135, 225)
ROJO = (190, 55, 65)

fuente = pygame.font.SysFont("Arial", 23)
fuente_titulo = pygame.font.SysFont("Arial", 32, bold=True)

reloj = pygame.time.Clock()

CARPETA_PROYECTO = Path(__file__).resolve().parent


def crear_boton(texto, x, y, ancho, alto, color=AZUL):

    rectangulo = pygame.Rect(x, y, ancho, alto)

    if rectangulo.collidepoint(pygame.mouse.get_pos()):
        if color == AZUL:
            color = AZUL_CLARO

    pygame.draw.rect(
        ventana,
        color,
        rectangulo,
        border_radius=12
    )

    superficie = fuente.render(texto, True, BLANCO)
    posicion = superficie.get_rect(center=rectangulo.center)

    ventana.blit(superficie, posicion)

    return rectangulo


def ejecutar_ejercicio(ruta):

    archivo = CARPETA_PROYECTO / ruta

    if not archivo.is_file():
        print(f"No se encontro el archivo: {archivo}")
        return

    try:
        print(f"Ejecutando: {archivo.name}")

        proceso = subprocess.Popen(
            [sys.executable, str(archivo)],
            cwd=str(CARPETA_PROYECTO)
        )

        print(f"Ejercicio iniciado. PID: {proceso.pid}")

    except Exception as error:
        print(f"Error al ejecutar {archivo.name}: {error}")


def buscar_ejercicio(carpeta, nombre):

    ruta = Path(carpeta) / nombre

    if (CARPETA_PROYECTO / ruta).is_file():
        return str(ruta)

    ruta_python = Path(carpeta) / f"{nombre}.py"

    if (CARPETA_PROYECTO / ruta_python).is_file():
        return str(ruta_python)

    return str(ruta_python)


def main():

    menu_actual = "principal"
    ejecutando = True

    while ejecutando:

        ventana.fill(FONDO)

        titulo = fuente_titulo.render(
            "PROYECTO 1 - VISION POR COMPUTADOR",
            True,
            BLANCO
        )

        ventana.blit(
            titulo,
            titulo.get_rect(center=(ANCHO // 2, 55))
        )

        botones = []

        if menu_actual == "principal":

            botones.append((
                crear_boton(
                    "PARTE 1 - COMPAÑERO",
                    225, 180, 400, 65
                ),
                "parte1"
            ))

            botones.append((
                crear_boton(
                    "PARTE 2 - MIS 7 EJERCICIOS",
                    225, 280, 400, 65
                ),
                "parte2"
            ))

            botones.append((
                crear_boton(
                    "SALIR",
                    225, 400, 400, 65, ROJO
                ),
                "salir"
            ))

        elif menu_actual == "parte1":

            botones.append((
                crear_boton(
                    "Momentos de Hu",
                    225, 150, 400, 60
                ),
                buscar_ejercicio("parte1", "parte_hu")
            ))

            botones.append((
                crear_boton(
                    "Composicion de imagenes",
                    225, 235, 400, 60
                ),
                buscar_ejercicio("parte1", "parte_composicion")
            ))

            botones.append((
                crear_boton(
                    "VOLVER",
                    225, 400, 400, 60, ROJO
                ),
                "principal"
            ))

        elif menu_actual == "parte2":

            nombres = [
                "Ejercicio_1",
                "ejercicio2",
                "ejercicio3",
                "ejercicio4",
                "ejercicio5",
                "ejercicio6",
                "ejercicio7"
            ]

            for i, nombre in enumerate(nombres):

                y = 110 + i * 65

                botones.append((
                    crear_boton(
                        f"Ejercicio {i + 1}",
                        225, y, 400, 50
                    ),
                    buscar_ejercicio("proyecto_2", nombre)
                ))

            botones.append((
                crear_boton(
                    "VOLVER",
                    225, 580, 400, 50, ROJO
                ),
                "principal"
            ))

        pygame.display.flip()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:

                    for rectangulo, accion in botones:

                        if rectangulo.collidepoint(evento.pos):

                            if accion == "salir":
                                ejecutando = False

                            elif accion in ["principal", "parte1", "parte2"]:
                                menu_actual = accion

                            else:
                                ejecutar_ejercicio(accion)

                            break

        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
