# Actividad: Agentes Aspiradoras
# Fecha: 16/11/2026
# Autores:
#     A01801372 Said Valseca Figueroa
#     A01801978 Lorena Antonio Monraga
# Descripcion: Ejecuta los experimentos del sistema
#              multiagente de robots de limpieza.


from experiments import (
    ejecutarExperimentos,
    generarGraficas,
    mostrarResultados,
)


ANCHO_HABITACION = 10
ALTO_HABITACION = 10
PORCENTAJE_SUCIEDAD = 30
TIEMPO_MAXIMO = 1000


# Descripcion: Ejecuta el conjunto de experimentos,
#              muestra los resultados y genera graficas.
# Parametros: Ninguno.
# Retorno: Ninguno.
def main():
    print("=" * 60)
    print("SISTEMA MULTIAGENTE DE ROBOTS DE LIMPIEZA")
    print("=" * 60)

    print(
        f"Habitacion: "
        f"{ANCHO_HABITACION} x {ALTO_HABITACION}"
    )

    print(
        f"Suciedad inicial: {PORCENTAJE_SUCIEDAD}%"
    )

    print(f"Tiempo maximo: {TIEMPO_MAXIMO} pasos")

    print("Iniciando experimentos...")

    resultados = ejecutarExperimentos(
        ancho=ANCHO_HABITACION,
        alto=ALTO_HABITACION,
        porcentajeSuciedad=PORCENTAJE_SUCIEDAD,
        tiempoMaximo=TIEMPO_MAXIMO,
    )

    mostrarResultados(resultados)

    generarGraficas(resultados)

    print()
    print("Experimentos finalizados correctamente.")
    print("Las graficas se guardaron en: graficas/")


if __name__ == "__main__":
    main()
