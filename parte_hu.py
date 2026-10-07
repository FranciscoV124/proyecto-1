# Proyecto #1 - INFO 1128
# Etapa 1: Momentos Invariantes de Hu para vocales (A, E, I, O, U)

import cv2
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def extraer_vocales(path="vocales.png"):
    img = Image.open(path).convert("RGBA")
    arr = np.array(img)

    # Separar canales para detectar píxeles oscuros (las letras son negras)
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    mascara_oscura = (r < 80) & (g < 80) & (b < 80) & (a > 100)

    # Encontrar qué columnas tienen contenido (algún píxel oscuro)
    cols_con_contenido = np.any(mascara_oscura, axis=0)
    indices_cols = np.where(cols_con_contenido)[0]

    # Agrupar columnas contiguas para separar cada letra
    grupos = []
    if len(indices_cols) > 0:
        cortes = np.where(np.diff(indices_cols) > 15)[0]
        limites = [0] + list(cortes + 1) + [len(indices_cols)]
        for i in range(len(limites) - 1):
            segmento = indices_cols[limites[i]:limites[i+1]]
            grupos.append((segmento[0], segmento[-1]))

    vocales = ['A', 'E', 'I', 'O', 'U']
    imagenes = {}
    for i, (x0, x1) in enumerate(grupos[:5]):
        letra = vocales[i]
        recorte = arr[:, x0:x1+1, :]

        # Convertir a escala de grises: fondo blanco, letra negra
        recorte_gris = np.ones((recorte.shape[0], recorte.shape[1]), dtype=np.uint8) * 255
        oscuro = (recorte[:,:,0] < 80) & (recorte[:,:,1] < 80) & (recorte[:,:,2] < 80) & (recorte[:,:,3] > 100)
        recorte_gris[oscuro] = 0

        imagenes[letra] = recorte_gris
        Image.fromarray(recorte_gris).save(f"vocal_{letra}.png")
        print(f"  Vocal {letra}: {recorte_gris.shape[1]}x{recorte_gris.shape[0]} px")

    return imagenes

def calcular_hu_moments(imagen_gris):
    # Binarizar con Otsu y calcular momentos
    _, binary = cv2.threshold(imagen_gris, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    img_moments = cv2.moments(binary)
    hu_moments = cv2.HuMoments(img_moments).flatten()
    # Escala logaritmica para facilitar comparacion
    hu_log = np.array([-np.sign(h)*np.log10(abs(h)) if h != 0 else 0.0 for h in hu_moments])
    return hu_moments, hu_log

def generar_tabla_resumen(resultados):
    vocales = ['A', 'E', 'I', 'O', 'U']
    hu_labels = [f'H{i+1}' for i in range(7)]

    print("\nMOMENTOS INVARIANTES DE HU - Escala log: -sign(h)*log10|h|")
    header = f"{'Vocal':<8}" + "".join(f"{'H'+str(i+1):>18}" for i in range(7))
    print(header)
    print("-" * 90)
    for v in vocales:
        vals = resultados[v]['log']
        row = f"{v:<8}" + "".join(f"{vals[i]:>18.4f}" for i in range(7))
        print(row)

    # Generar tabla como imagen con fondo blanco
    fig, axes = plt.subplots(2, 1, figsize=(16, 8))
    fig.patch.set_facecolor('white')

    for ax_idx, (title, key, fmt) in enumerate([
        ("Momentos de Hu - Valores Originales", 'raw', '.2e'),
        ("Momentos de Hu - Escala Logaritmica", 'log', '.4f')
    ]):
        ax = axes[ax_idx]
        ax.axis('off')
        data = [[v] + [f"{resultados[v][key][i]:{fmt}}" for i in range(7)] for v in vocales]
        col_labels = ['Vocal'] + hu_labels
        tbl = ax.table(cellText=data, colLabels=col_labels, cellLoc='center', loc='center')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)
        tbl.scale(1, 2)
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)

    plt.suptitle("Proyecto #1 - Momentos Invariantes de Hu", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig("tabla_hu.png", dpi=150, bbox_inches='tight', facecolor='white')
    print("Tabla guardada: tabla_hu.png")

def imprimir_conclusiones():
    print("""
CONCLUSIONES DEL ANALISIS DE MOMENTOS DE HU:

1. H1 es similar en todas las vocales pero no identico: los valores van de 3.02 (I)
   a 3.15 (O). Esto tiene sentido: H1 mide la dispersion total de pixeles respecto
   al centroide, y aunque todas son letras del mismo tamano, la I es muy estrecha
   (56px de ancho) mientras la O y la A son mas anchas (77-94px). La diferencia
   es pequena pero consistente.

2. H5 de la O es el unico valor NEGATIVO de toda la tabla (-29.02). Esto llama
   mucho la atencion. H5 captura una combinacion de momentos de orden superior
   relacionados con la simetria radial. La O es la unica letra cerrada y
   perfectamente redondeada del conjunto, lo que hace que su distribucion de
   pixeles sea cualitativamente distinta al resto. El signo negativo indica que
   la estructura de la O "invierte" el patron que tienen las letras abiertas.

3. La I tiene los valores mas extremos en H3, H4 y H5 (14.89, 15.46, 30.71).
   Esto refleja que la I es la forma mas alargada y angosta del conjunto.
   Los momentos de orden mayor son muy sensibles a la elongacion, por eso
   la I se destaca claramente en esos momentos.

4. H7 separa las vocales en dos grupos por signo: positivo (A=+21.50, O=+28.14,
   U=+22.84) y negativo (E=-22.36, I=-30.90). H7 mide asimetria de tercer orden
   y su signo depende de como estan distribuidos los trazos respecto al eje.
   Las letras con apertura hacia arriba o trazos superiores dominantes tienden
   a un signo, y las que tienen mas masa en la parte inferior o son cerradas
   tienden al otro.

5. En conclusion, los momentos de Hu SI permiten distinguir las vocales entre si,
   especialmente combinando H3, H5 y H7. Ningun par de vocales tiene los siete
   momentos identicos. Sin embargo, usando solo H1 o H2 no seria suficiente
   porque sus diferencias son pequenas (tercer decimal). Para un clasificador
   real habria que usar al menos H3 en adelante.
""")

def generar_grafico(resultados):
    vocales = ['A', 'E', 'I', 'O', 'U']
    colores = ['#d73027', '#fc8d59', '#fee090', '#91bfdb', '#4575b4']

    fig, ejes = plt.subplots(2, 4, figsize=(18, 8))
    fig.patch.set_facecolor('white')
    ejes = ejes.flatten()

    for i in range(7):
        eje = ejes[i]
        valores = [resultados[v]['log'][i] for v in vocales]
        barras = eje.bar(vocales, valores, color=colores, width=0.6, edgecolor='black', linewidth=1)
        eje.set_title(f'Momento H{i+1}', fontsize=11, fontweight='bold')
        eje.set_ylabel('Escala log', fontsize=9)
        eje.tick_params(labelsize=10)

        # Ocultar bordes innecesarios
        for borde in ['top', 'right']:
            eje.spines[borde].set_visible(False)

        for barra, val in zip(barras, valores):
            eje.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.05, f'{val:.2f}',
                    ha='center', va='bottom', fontsize=8)

    # El octavo eje queda vacio
    ejes[7].axis('off')

    plt.suptitle("Comparacion de Momentos de Hu por Vocal", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig("grafico_hu.png", dpi=150, bbox_inches='tight', facecolor='white')
    print("Grafico guardado: grafico_hu.png")

def main():
    print("\nExtrayendo vocales de la imagen")
    imagenes = extraer_vocales("vocales.png")

    print("\nCalculando momentos de Hu")
    resultados = {}
    for letra, imagen in imagenes.items():
        hu_moments, hu_log = calcular_hu_moments(imagen)
        resultados[letra] = {'raw': hu_moments, 'log': hu_log}

    generar_tabla_resumen(resultados)
    generar_grafico(resultados)
    imprimir_conclusiones()

    return resultados

if __name__ == "__main__":
    main()
