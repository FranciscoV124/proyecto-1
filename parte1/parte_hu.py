import cv2
import numpy as np


# Cargar imagen
imagen = cv2.imread("/imagenesdeproyecto1part1/vocales.png")


def detectar_imagen(imagen):

    if imagen is None:
        print("Error al cargar la imagen")
        return False

    print("Imagen cargada correctamente")
    return True


def calcular_log_hu(valor):

    if valor == 0:
        return 0

    return -np.sign(valor) * np.log10(abs(valor))


if detectar_imagen(imagen):

    # 1. Convertir imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # 2. Binarizar
    _, binaria = cv2.threshold(
        gris,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # 3. Buscar componentes conectados
    cantidad, etiquetas, datos, centroides = \
        cv2.connectedComponentsWithStats(
            binaria,
            connectivity=8
        )

    componentes = []

    # Empezamos en 1 porque 0 corresponde al fondo
    for i in range(1, cantidad):

        x = datos[i, cv2.CC_STAT_LEFT]
        y = datos[i, cv2.CC_STAT_TOP]
        ancho = datos[i, cv2.CC_STAT_WIDTH]
        alto = datos[i, cv2.CC_STAT_HEIGHT]
        area = datos[i, cv2.CC_STAT_AREA]

        componentes.append(
            (x, y, ancho, alto, area, i)
        )

    # 4. Ordenar las vocales de izquierda a derecha
    componentes.sort(key=lambda componente: componente[0])

    vocales = ["A", "E", "I", "O", "U"]

    resultados = []

    # 5. Calcular momentos de Hu de cada vocal
    for vocal, componente in zip(vocales, componentes):

        x, y, ancho, alto, area, etiqueta = componente

        # Crear una máscara vacía
        mascara = np.zeros_like(binaria)

        # Dejar solamente la vocal actual
        mascara[etiquetas == etiqueta] = 255

        # Calcular momentos normales
        momentos = cv2.moments(
            mascara,
            binaryImage=True
        )

        # Calcular los 7 momentos de Hu
        hu = cv2.HuMoments(momentos)

        hu_log = []

        for i in range(7):

            valor = hu[i][0]

            valor_log = calcular_log_hu(valor)

            hu_log.append(valor_log)

        resultados.append((vocal, hu_log))


    # 6. Mostrar tabla resumen

    print()
    print("TABLA RESUMEN - MOMENTOS INVARIANTES DE HU")
    print()

    print(
        f"{'Vocal':<8}"
        f"{'Log(H1)':>12}"
        f"{'Log(H2)':>12}"
        f"{'Log(H3)':>12}"
        f"{'Log(H4)':>12}"
        f"{'Log(H5)':>12}"
        f"{'Log(H6)':>12}"
        f"{'Log(H7)':>12}"
    )

    print("-" * 92)

    for vocal, hu in resultados:

        print(
            f"{vocal:<8}"
            f"{hu[0]:>12.4f}"
            f"{hu[1]:>12.4f}"
            f"{hu[2]:>12.4f}"
            f"{hu[3]:>12.4f}"
            f"{hu[4]:>12.4f}"
            f"{hu[5]:>12.4f}"
            f"{hu[6]:>12.4f}"
        )


    # Mostrar imágenes para comprobar
    cv2.imshow("Imagen original", imagen)
    cv2.imshow("Imagen binaria", binaria)

    cv2.waitKey(0)
    cv2.destroyAllWindows()