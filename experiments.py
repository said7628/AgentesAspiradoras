# Actividad: Agentes Aspiradoras
# Fecha: 16/11/2026
# Autores:
#     A01801372 Said Valseca Figueroa
#     A01801978 Lorena Antonio Monraga
# Descripcion: Ejecuta experimentos estadisticos
#              del sistema multiagente de limpieza.
#              Compara la eficiencia de distintas
#              cantidades de robots reactivos.


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
TIEMPO_MAXIMO = 1000
SEMILLA_BASE = 2026

CARPETA_RESULTADOS = Path("resultados")
CARPETA_GRAFICAS = Path("graficas")


# Descripcion: Ejecuta una simulacion individual
#              con los parametros proporcionados.
# Parametros:
#     ancho: Numero de columnas.
#     alto: Numero de filas.
#     numeroAgentes: Cantidad de robots.
#     porcentajeSuciedad: Porcentaje inicial sucio.
#     tiempoMaximo: Limite de pasos.
#     semilla: Semilla aleatoria de la simulacion.
# Retorno: Diccionario de estadisticas finales.
def ejecutarExperimento(
    ancho,
    alto,
    numeroAgentes,
    porcentajeSuciedad,
    tiempoMaximo,
    semilla,
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


# Descripcion: Calcula la desviacion estandar
#              muestral de una serie de valores.
# Parametros:
#     valores: Secuencia de valores numericos.
# Retorno: Desviacion estandar o cero cuando
#          existen menos de dos observaciones.
def calcularDesviacion(valores):
    desviacion = 0.0

    if len(valores) > 1:
        desviacion = stdev(valores)

    return desviacion


# Descripcion: Guarda registros estadisticos en CSV
#              para facilitar su revision posterior.
# Parametros:
#     archivo: Ruta de salida del archivo CSV.
#     filas: Lista de diccionarios con los registros.
# Retorno: Ninguno.
def guardarCsv(archivo, filas):
    archivo.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if len(filas) > 0:
        with archivo.open(
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as salida:
            escritor = csv.DictWriter(
                salida,
                fieldnames=list(filas[0].keys()),
            )

            escritor.writeheader()
            escritor.writerows(filas)


# Descripcion: Resume los indicadores de un grupo
#              de simulaciones con igual numero
#              de robots.
# Parametros:
#     corridasGrupo: Resultados individuales.
#     numeroAgentes: Cantidad de robots del grupo.
# Retorno: Diccionario con estadisticas agregadas.
def resumirGrupo(corridasGrupo, numeroAgentes):
    exitos = [
        corrida
        for corrida in corridasGrupo
        if corrida["limpiezaCompleta"]
    ]

    pasos = [
        corrida["pasosEjecutados"]
        for corrida in corridasGrupo
    ]

    movimientos = [
        corrida["movimientosTotales"]
        for corrida in corridasGrupo
    ]

    porcentajes = [
        corrida["porcentajeLimpieza"]
        for corrida in corridasGrupo
    ]

    tiemposExitosos = [
        corrida["tiempoLimpieza"]
        for corrida in exitos
    ]

    repeticiones = len(corridasGrupo)

    tiempoExitosoPromedio = None
    desviacionTiempoExitoso = None

    if len(tiemposExitosos) > 0:
        tiempoExitosoPromedio = round(
            mean(tiemposExitosos),
            2,
        )

        desviacionTiempoExitoso = round(
            calcularDesviacion(tiemposExitosos),
            2,
        )

    resumen = {
        "numeroAgentes": numeroAgentes,
        "repeticiones": repeticiones,
        "pasosPromedio": round(mean(pasos), 2),
        "desviacionPasos": round(
            calcularDesviacion(pasos),
            2,
        ),
        "movimientosPromedio": round(
            mean(movimientos),
            2,
        ),
        "desviacionMovimientos": round(
            calcularDesviacion(movimientos),
            2,
        ),
        "limpiezaPromedio": round(
            mean(porcentajes),
            2,
        ),
        "desviacionLimpieza": round(
            calcularDesviacion(porcentajes),
            2,
        ),
        "limpiezasCompletas": len(exitos),
        "porcentajeExito": round(
            100.0 * len(exitos) / repeticiones,
            2,
        ),
        "tiempoExitosoPromedio": tiempoExitosoPromedio,
        "desviacionTiempoExitoso": desviacionTiempoExitoso,
    }

    return resumen


# Descripcion: Ejecuta todas las configuraciones
#              experimentales y recopila sus datos.
# Parametros:
#     cantidadesAgentes: Cantidades de robots a comparar.
#     repeticiones: Simulaciones por configuracion.
#     ancho: Numero de columnas.
#     alto: Numero de filas.
#     porcentajeSuciedad: Porcentaje inicial sucio.
#     tiempoMaximo: Limite de pasos por simulacion.
#     semillaBase: Semilla inicial de los experimentos.
#     carpetaResultados: Carpeta de archivos CSV.
# Retorno: Lista de resumenes estadisticos.
def ejecutarExperimentos(
    cantidadesAgentes=CANTIDADES_AGENTES,
    repeticiones=REPETICIONES,
    ancho=10,
    alto=10,
    porcentajeSuciedad=30,
    tiempoMaximo=TIEMPO_MAXIMO,
    semillaBase=SEMILLA_BASE,
    carpetaResultados=CARPETA_RESULTADOS,
):
    if repeticiones < 1:
        raise ValueError(
            "Debe realizarse al menos una repeticion."
        )

    if (
        len(cantidadesAgentes) == 0
        or any(
            cantidad < 1
            for cantidad in cantidadesAgentes
        )
    ):
        raise ValueError(
            "Las cantidades de agentes deben ser positivas."
        )

    corridasRegistradas = []
    resumenes = []

    for numeroAgentes in cantidadesAgentes:
        corridasGrupo = []

        for numeroRepeticion in range(repeticiones):
            # La misma semilla por repeticion permite
            # comparar grupos con suciedad inicial igual.
            semilla = semillaBase + numeroRepeticion

            estadisticas = ejecutarExperimento(
                ancho=ancho,
                alto=alto,
                numeroAgentes=numeroAgentes,
                porcentajeSuciedad=porcentajeSuciedad,
                tiempoMaximo=tiempoMaximo,
                semilla=semilla,
            )

            registro = {
                "repeticion": numeroRepeticion + 1,
                **estadisticas,
            }

            corridasRegistradas.append(registro)
            corridasGrupo.append(registro)

        resumen = resumirGrupo(
            corridasGrupo,
            numeroAgentes,
        )

        resumenes.append(resumen)

    guardarCsv(
        Path(carpetaResultados) / "corridas.csv",
        corridasRegistradas,
    )

    guardarCsv(
        Path(carpetaResultados) / "resumenes.csv",
        resumenes,
    )

    return resumenes


# Descripcion: Imprime una tabla comparativa de
#              las configuraciones experimentales.
# Parametros:
#     resumenes: Lista de resultados agregados.
# Retorno: Ninguno.
def mostrarResultados(resumenes):
    print()
    print("RESULTADOS DE ROBOTS DE LIMPIEZA")
    print("-" * 86)

    print(
        f"{'Robots':>7} | "
        f"{'Pasos':>10} | "
        f"{'Movimientos':>12} | "
        f"{'Limpieza %':>10} | "
        f"{'Exito %':>9} | "
        f"{'Tiempo exito':>12}"
    )

    print("-" * 86)

    for resumen in resumenes:
        tiempoExito = resumen["tiempoExitosoPromedio"]

        tiempoTexto = "N/D"

        if tiempoExito is not None:
            tiempoTexto = f"{tiempoExito:.2f}"

        print(
            f"{resumen['numeroAgentes']:>7} | "
            f"{resumen['pasosPromedio']:>10.2f} | "
            f"{resumen['movimientosPromedio']:>12.2f} | "
            f"{resumen['limpiezaPromedio']:>10.2f} | "
            f"{resumen['porcentajeExito']:>9.2f} | "
            f"{tiempoTexto:>12}"
        )

    print("-" * 86)

    print(
        "Pasos promedio: incluye simulaciones "
        "que alcanzaron el limite."
    )

    print(
        "Tiempo exito: promedio de las simulaciones "
        "que limpiaron toda la habitacion."
    )


# Descripcion: Genera una grafica de lineas con
#              resultados por cantidad de robots.
# Parametros:
#     resumenes: Resultados agregados.
#     campo: Indicador del eje vertical.
#     titulo: Titulo de la grafica.
#     etiquetaY: Etiqueta del eje vertical.
#     archivo: Ruta de salida de la imagen.
# Retorno: Ninguno.
def guardarGrafica(
    resumenes,
    campo,
    titulo,
    etiquetaY,
    archivo,
):
    numerosRobots = [
        fila["numeroAgentes"]
        for fila in resumenes
    ]

    valores = [
        fila[campo]
        for fila in resumenes
    ]

    figura, ejes = plt.subplots(
        figsize=(8, 4.5)
    )

    ejes.plot(
        numerosRobots,
        valores,
        marker="o",
        linewidth=2,
    )

    ejes.set_xticks(numerosRobots)
    ejes.set_xlabel("Cantidad de robots")
    ejes.set_ylabel(etiquetaY)
    ejes.set_title(titulo)

    ejes.grid(
        axis="y",
        alpha=0.25,
    )

    if campo == "limpiezaPromedio":
        ejes.set_ylim(0, 105)

    figura.tight_layout()

    figura.savefig(
        archivo,
        dpi=170,
    )

    plt.close(figura)


# Descripcion: Genera las graficas comparativas
#              de tiempo, movimientos y limpieza.
# Parametros:
#     resumenes: Resultados de los experimentos.
# Retorno: Ninguno.
def generarGraficas(resumenes):
    CARPETA_GRAFICAS.mkdir(
        parents=True,
        exist_ok=True,
    )

    configuraciones = (
        (
            "pasosPromedio",
            "Cantidad de robots vs. pasos utilizados",
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
            "Cantidad de robots vs. limpieza final",
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


# Descripcion: Permite ejecutar experimentos desde
#              la terminal mediante argumentos.
# Parametros: Ninguno; lee argumentos de consola.
# Retorno: Ninguno.
def main():
    analizador = argparse.ArgumentParser(
        description=(
            "Experimentos del sistema multiagente "
            "de robots de limpieza."
        )
    )

    analizador.add_argument(
        "--repeticiones",
        type=int,
        default=REPETICIONES,
    )

    analizador.add_argument(
        "--ancho",
        type=int,
        default=10,
    )

    analizador.add_argument(
        "--alto",
        type=int,
        default=10,
    )

    analizador.add_argument(
        "--suciedad",
        type=int,
        default=30,
    )

    analizador.add_argument(
        "--tiempo",
        type=int,
        default=TIEMPO_MAXIMO,
    )

    analizador.add_argument(
        "--semilla",
        type=int,
        default=SEMILLA_BASE,
    )

    analizador.add_argument(
        "--agentes",
        nargs="+",
        type=int,
        default=list(CANTIDADES_AGENTES),
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

    print()
    print("Experimentos finalizados correctamente.")
    print("Resultados guardados en: resultados/")
    print("Graficas guardadas en: graficas/")


if __name__ == "__main__":
    main()