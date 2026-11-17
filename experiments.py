# Autores:
#     Said Valseca - Matricula: ____________
#     Lorena Antonio - Matricula: ____________
# Fecha de creacion/modificacion: 16/11/2026

import argparse
import csv
from pathlib import Path
from statistics import mean, stdev

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import ModeloLimpieza


CANTIDADES_AGENTES = (1, 2, 3, 5, 10)
REPETICIONES = 30
CARPETA_RESULTADOS = Path("resultados")
CARPETA_GRAFICAS = Path("graficas")


# Descripcion: Ejecuta un escenario y obtiene las mediciones finales.
# Parametros:
#     ancho: Numero de columnas de la habitacion.
#     alto: Numero de filas de la habitacion.
#     numeroAgentes: Numero de robots de limpieza.
#     porcentajeSuciedad: Porcentaje de celdas sucias al inicio.
#     tiempoMaximo: Numero maximo de pasos permitidos.
#     semilla: Valor utilizado para reproducir el escenario.
# Retorno: Diccionario de estadisticas de ModeloLimpieza.
def ejecutarExperimento(
    ancho, alto, numeroAgentes, porcentajeSuciedad, tiempoMaximo, semilla
):
    modelo = ModeloLimpieza(
        ancho=ancho,
        alto=alto,
        numeroAgentes=numeroAgentes,
        porcentajeSuciedad=porcentajeSuciedad,
        tiempoMaximo=tiempoMaximo,
        semilla=semilla,
    )
    return modelo.ejecutarSimulacion()


# Descripcion: Calcula la desviacion estandar muestral de una serie;
#              devuelve cero cuando existe una sola observacion.
# Parametros:
#     valores: Secuencia de valores numericos.
# Retorno: Desviacion estandar muestral como numero decimal.
def calcularDesviacion(valores):
    return stdev(valores) if len(valores) > 1 else 0.0


# Descripcion: Exporta registros tabulares para reproducir el analisis.
# Parametros:
#     archivo: Ruta del archivo CSV de salida.
#     filas: Lista de diccionarios con columnas consistentes.
# Retorno: Ninguno.
def guardarCsv(archivo, filas):
    archivo.parent.mkdir(parents=True, exist_ok=True)
    if filas:
        with archivo.open("w", newline="", encoding="utf-8-sig") as salida:
            escritor = csv.DictWriter(salida, fieldnames=list(filas[0].keys()))
            escritor.writeheader()
            escritor.writerows(filas)


# Descripcion: Repite escenarios con la misma suciedad inicial para
#              comparar las cantidades de agentes de forma equitativa.
# Parametros:
#     cantidadesAgentes: Secuencia de numeros de robots a evaluar.
#     repeticiones: Numero de simulaciones por configuracion.
#     ancho: Columnas de la habitacion.
#     alto: Filas de la habitacion.
#     porcentajeSuciedad: Porcentaje inicial de celdas sucias.
#     tiempoMaximo: Limite de pasos por simulacion.
#     semillaBase: Primera semilla aleatoria de cada grupo.
#     carpetaResultados: Carpeta en la que se guardan los CSV.
# Retorno: Lista de resumenes, uno por cantidad de agentes.
def ejecutarExperimentos(
    cantidadesAgentes=CANTIDADES_AGENTES,
    repeticiones=REPETICIONES,
    ancho=10,
    alto=10,
    porcentajeSuciedad=30,
    tiempoMaximo=500,
    semillaBase=2026,
    carpetaResultados=CARPETA_RESULTADOS,
):
    if repeticiones < 1:
        raise ValueError("Debe realizarse al menos una repeticion.")
    if not cantidadesAgentes or any(cantidad < 1 for cantidad in cantidadesAgentes):
        raise ValueError("Las cantidades de agentes deben ser positivas.")

    corridasRegistradas = []
    resumenes = []

    for numeroAgentes in cantidadesAgentes:
        corridasGrupo = []

        for numeroRepeticion in range(repeticiones):
            # Una semilla compartida por repeticion genera la misma
            # distribucion inicial de suciedad entre grupos de robots.
            semilla = semillaBase + numeroRepeticion
            estadisticas = ejecutarExperimento(
                ancho=ancho,
                alto=alto,
                numeroAgentes=numeroAgentes,
                porcentajeSuciedad=porcentajeSuciedad,
                tiempoMaximo=tiempoMaximo,
                semilla=semilla,
            )
            registro = {"repeticion": numeroRepeticion + 1, **estadisticas}
            corridasRegistradas.append(registro)
            corridasGrupo.append(registro)

        exitos = [corrida for corrida in corridasGrupo if corrida["limpiezaCompleta"]]
        pasos = [corrida["pasosEjecutados"] for corrida in corridasGrupo]
        movimientos = [corrida["movimientosTotales"] for corrida in corridasGrupo]
        porcentajes = [corrida["porcentajeLimpieza"] for corrida in corridasGrupo]
        tiemposExitosos = [corrida["tiempoLimpieza"] for corrida in exitos]

        resumenes.append(
            {
                "numeroAgentes": numeroAgentes,
                "repeticiones": repeticiones,
                "pasosPromedio": round(mean(pasos), 2),
                "desviacionPasos": round(calcularDesviacion(pasos), 2),
                "movimientosPromedio": round(mean(movimientos), 2),
                "desviacionMovimientos": round(calcularDesviacion(movimientos), 2),
                "limpiezaPromedio": round(mean(porcentajes), 2),
                "desviacionLimpieza": round(calcularDesviacion(porcentajes), 2),
                "limpiezasCompletas": len(exitos),
                "porcentajeExito": round(100.0 * len(exitos) / repeticiones, 2),
                # Solo las corridas exitosas tienen tiempo de limpieza.
                "tiempoExitosoPromedio": (
                    round(mean(tiemposExitosos), 2) if tiemposExitosos else None
                ),
                "desviacionTiempoExitoso": (
                    round(calcularDesviacion(tiemposExitosos), 2)
                    if tiemposExitosos
                    else None
                ),
            }
        )

    guardarCsv(Path(carpetaResultados) / "corridas.csv", corridasRegistradas)
    guardarCsv(Path(carpetaResultados) / "resumenes.csv", resumenes)
    return resumenes


# Descripcion: Imprime los indicadores de cada configuracion para
#              identificar diferencias en tiempo, movimiento y limpieza.
# Parametros:
#     resumenes: Lista de diccionarios de ejecutarExperimentos().
# Retorno: Ninguno.
def mostrarResultados(resumenes):
    print("\nResultados de robots de limpieza")
    print("Robots | Pasos prom. | Mov. prom. | Limpieza % | Exito % | Tiempo exito")
    print("-" * 75)
    for resumen in resumenes:
        tiempoExito = resumen["tiempoExitosoPromedio"]
        tiempoTexto = f"{tiempoExito:.2f}" if tiempoExito is not None else "N/D"
        print(
            f'{resumen["numeroAgentes"]:>6} | '
            f'{resumen["pasosPromedio"]:>11.2f} | '
            f'{resumen["movimientosPromedio"]:>10.2f} | '
            f'{resumen["limpiezaPromedio"]:>10.2f} | '
            f'{resumen["porcentajeExito"]:>7.2f} | '
            f'{tiempoTexto:>12}'
        )
    print("\nNota: el promedio de pasos incluye corridas limitadas por tiempo.")
    print("El tiempo de limpieza completa incluye solamente corridas exitosas.")


# Descripcion: Guarda una grafica comparativa con eje horizontal de robots.
# Parametros:
#     resumenes: Resumenes por cantidad de agentes.
#     campo: Indicador que se utiliza en el eje vertical.
#     titulo: Titulo explicativo de la grafica.
#     etiquetaY: Nombre de la variable del eje vertical.
#     archivo: Ruta de la imagen PNG de salida.
# Retorno: Ninguno.
def guardarGrafica(resumenes, campo, titulo, etiquetaY, archivo):
    numerosRobots = [fila["numeroAgentes"] for fila in resumenes]
    valores = [fila[campo] for fila in resumenes]
    figura, ejes = plt.subplots(figsize=(8, 4.5))
    ejes.plot(numerosRobots, valores, marker="o", linewidth=2)
    ejes.set_xticks(numerosRobots)
    ejes.set_xlabel("Cantidad de robots")
    ejes.set_ylabel(etiquetaY)
    ejes.set_title(titulo)
    ejes.grid(axis="y", alpha=0.25)
    if campo == "limpiezaPromedio":
        ejes.set_ylim(0, 105)
    figura.tight_layout()
    figura.savefig(archivo, dpi=170)
    plt.close(figura)


# Descripcion: Genera las tres graficas solicitadas en la actividad.
# Parametros:
#     resumenes: Lista de resumenes de ejecutarExperimentos().
# Retorno: Ninguno; las graficas se guardan como imagenes PNG.
def generarGraficas(resumenes):
    CARPETA_GRAFICAS.mkdir(parents=True, exist_ok=True)
    configuraciones = (
        (
            "pasosPromedio",
            "Cantidad de robots vs. tiempo de ejecucion",
            "Pasos promedio",
            "robots_vs_tiempo.png",
        ),
        (
            "movimientosPromedio",
            "Cantidad de robots vs. movimientos",
            "Movimientos promedio",
            "robots_vs_movimientos.png",
        ),
        (
            "limpiezaPromedio",
            "Cantidad de robots vs. porcentaje de limpieza",
            "Porcentaje de limpieza",
            "robots_vs_limpieza.png",
        ),
    )
    for campo, titulo, etiquetaY, nombreArchivo in configuraciones:
        guardarGrafica(
            resumenes,
            campo,
            titulo,
            etiquetaY,
            CARPETA_GRAFICAS / nombreArchivo,
        )


# Descripcion: Permite ejecutar las pruebas sin depender de main.py,
#              manteniendo tambien las funciones para su integracion.
# Parametros: Ninguno; utiliza argumentos de la terminal.
# Retorno: Ninguno.
def main():
    analizador = argparse.ArgumentParser(
        description="Experimentos de agentes aspiradores con Mesa."
    )
    analizador.add_argument("--repeticiones", type=int, default=REPETICIONES)
    analizador.add_argument("--ancho", type=int, default=10)
    analizador.add_argument("--alto", type=int, default=10)
    analizador.add_argument("--suciedad", type=int, default=30)
    analizador.add_argument("--tiempo", type=int, default=500)
    analizador.add_argument("--semilla", type=int, default=2026)
    analizador.add_argument(
        "--agentes", nargs="+", type=int, default=list(CANTIDADES_AGENTES)
    )
    argumentos = analizador.parse_args()
    resumenes = ejecutarExperimentos(
        cantidadesAgentes=argumentos.agentes,
        repeticiones=argumentos.repeticiones,
        ancho=argumentos.ancho,
        alto=argumentos.alto,
        porcentajeSuciedad=argumentos.suciedad,
        tiempoMaximo=argumentos.tiempo,
        semillaBase=argumentos.semilla,
    )
    mostrarResultados(resumenes)
    generarGraficas(resumenes)
    print("\nArchivos guardados en las carpetas resultados/ y graficas/.")


if __name__ == "__main__":
    main()
