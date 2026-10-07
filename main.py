# Proyecto #1 - INFO 1128
# Script principal: ejecuta la etapa 1 y la etapa 2

import os, sys

def main():
    print("PROYECTO #1 - INFO 1128 - By Alberto Caro")
    print("Etapa 1: Momentos Invariantes de Hu para vocales")
    print("Etapa 2: Composición de imágenes con plantilla (Pygame + PIL)")
    
    import parte_hu
    resultados = parte_hu.main()
    import parte_composicion
    parte_composicion.main()
    
    print()
    print("Archivos generados:")
    print("tabla_hu.png - Tabla de momentos de Hu")
    print("grafico_hu.png - Gráfico comparativo")
    print("vocal_A/E/I/O/U.png - Vocales extraídas")
    print("resultado_etapa2.png - Composición final")

if __name__ == "__main__":
    main()
