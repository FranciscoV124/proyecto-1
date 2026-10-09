from PIL import Image
import matplotlib.pyplot as plt
import cv2

imagen = cv2.imread("proyecto_2/imagenes/monito.jpg")


def detectar_imagen(imagen):

    if imagen is None:
        print("Error al cargar la imagen")
        return False

    print("Imagen cargada correctamente")
    return True

detectar_imagen(imagen)

def calcular_histograma(imagen):
    imagen = imagen.convert("L")

    histograma = imagen.histogram()

    plt.bar(range(256), histograma)

    plt.title("Histograma de la imagen")
    plt.xlabel("Intensidad de píxeles")
    plt.ylabel("Cantidad de píxeles")

    plt.show()


imagen = Image.open("proyecto_2/imagenes/monito.jpg")

calcular_histograma(imagen)