# Autores:
#     Said Valseca - Matricula: ____________
#     Lorena Antonio - Matricula: ____________
# Fecha de creacion/modificacion: 16/11/2026

import solara
from mesa.visualization import Slider, SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

from agents import CeldaLimpieza, RobotLimpieza
from model import ModeloLimpieza


# Descripcion: Define un estilo distinto para cada tipo de agente,
#              permitiendo identificar la suciedad y los robots.
# Parametros:
#     agente: CeldaLimpieza o RobotLimpieza a representar.
# Retorno: AgentPortrayalStyle con el estilo de visualizacion.
def representarAgente(agente):
    if isinstance(agente, RobotLimpieza):
        return AgentPortrayalStyle(
            color="#2458a0",
            marker="circle",
            size=160,
            zorder=3,
        )

    if isinstance(agente, CeldaLimpieza):
        colorCelda = "#e87878" if agente.estaSucia else "#a9dfc6"
        return AgentPortrayalStyle(
            color=colorCelda,
            marker="square",
            size=480,
            zorder=1,
        )

    return AgentPortrayalStyle(color="#888888", marker="circle", size=20)


# Descripcion: Muestra las estadisticas actuales de la simulacion
#              para facilitar la interpretacion de las graficas.
# Parametros:
#     modelo: Instancia activa de ModeloLimpieza.
# Retorno: Componente Markdown de Solara con los indicadores.
def mostrarEstado(modelo):
    estado = "En ejecucion" if modelo.running else "Finalizada"
    porcentajeLimpieza = modelo.calcularPorcentajeLimpieza()

    return solara.Markdown(
        f"**Estado:** {estado} | "
        f"**Pasos:** {modelo.pasosEjecutados}/{modelo.tiempoMaximo} | "
        f"**Limpieza:** {porcentajeLimpieza:.1f}% | "
        f"**Movimientos:** {modelo.movimientosTotales} | "
        f"**Celdas sucias:** {len(modelo.celdasSucias)}"
    )


# Los nombres de estos parametros coinciden con el constructor del
# modelo del equipo; Solara los utiliza al reiniciar la simulacion.
PARAMETROS_MODELO = {
    "ancho": Slider("Ancho (columnas)", value=10, min=1, max=30, step=1),
    "alto": Slider("Alto (filas)", value=10, min=1, max=30, step=1),
    "numeroAgentes": Slider(
        "Numero de robots", value=5, min=1, max=30, step=1
    ),
    "porcentajeSuciedad": Slider(
        "Celdas inicialmente sucias (%)", value=30, min=0, max=100, step=5
    ),
    "tiempoMaximo": Slider(
        "Tiempo maximo (pasos)", value=1000, min=1, max=2000, step=1
    ),
    "semilla": Slider("Semilla aleatoria", value=42, min=0, max=10000, step=1),
}

# La interfaz usa el mismo modelo y los mismos agentes del equipo.
modeloInicial = ModeloLimpieza()
renderizador = (
    SpaceRenderer(modeloInicial, backend="altair")
    .setup_agents(representarAgente)
    .render()
)

# SolaraViz proporciona Play/Pause, Step, Reset y los controles del modelo.
# Ejecutar desde la carpeta del proyecto: python -m solara run app.py
page = SolaraViz(
    model=modeloInicial,
    renderer=renderizador,
    components=[
        mostrarEstado,
        make_plot_component("Limpieza (%)", backend="altair"),
        make_plot_component("Movimientos", backend="altair"),
    ],
    model_params=PARAMETROS_MODELO,
    name="Robots de limpieza reactivos | TC2008B SMA",
    play_interval=150,
)
