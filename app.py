
# Descripcion: Implementa la interfaz web del sistema
#              multiagente de robots de limpieza
#              utilizando Mesa, Solara y Matplotlib.
# Autores:
#     Said Valseca - Matricula: ____________
#     Lorena Antonio - Matricula: ____________
# Fecha de creacion/modificacion: 16/11/2026

import solara

from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

from agents import CeldaLimpieza, RobotLimpieza
from model import ModeloLimpieza


# Descripcion: Define la apariencia visual de los
#              robots y las celdas de la habitacion.
# Parametros:
#     agente: Instancia del agente que se dibujara.
# Retorno: Estilo visual del agente.
def representarAgente(agente):
    if isinstance(agente, RobotLimpieza):
        apariencia = AgentPortrayalStyle(
            color="#2563EB",
            marker="o",
            size=110,
            zorder=3,
        )

    elif isinstance(agente, CeldaLimpieza):
        colorCelda = (
            "#DC6B50"
            if agente.estaSucia
            else "#B8E4C9"
        )

        apariencia = AgentPortrayalStyle(
            color=colorCelda,
            marker="s",
            size=210,
            zorder=1,
        )

    else:
        apariencia = AgentPortrayalStyle(
            color="#808080",
            marker="s",
            size=30,
        )

    return apariencia


# Descripcion: Configura los ejes de la habitacion.
# Parametros:
#     ejes: Ejes de Matplotlib.
# Retorno: Ninguno.
def configurarGrafica(ejes):
    ejes.set_aspect("equal")
    ejes.set_xticks([])
    ejes.set_yticks([])
    ejes.set_facecolor("#F8FAFC")


# Descripcion: Muestra los indicadores actuales
#              de la simulacion.
# Parametros:
#     modelo: Instancia activa de ModeloLimpieza.
# Retorno: Componente visual de Solara.
@solara.component
def mostrarEstado(modelo):
    porcentajeLimpieza = (
        modelo.calcularPorcentajeLimpieza()
    )

    cantidadSucias = len(modelo.celdasSucias)

    if modelo.running:
        estado = "En ejecucion"

    elif cantidadSucias == 0:
        estado = "Limpieza completada"

    else:
        estado = "Tiempo maximo alcanzado"

    solara.Markdown(
        "### Estadisticas de la simulacion"
    )

    solara.Markdown(
        f"**Estado:** {estado}"
    )

    solara.Markdown(
        f"**Robots:** {modelo.numeroAgentes}"
    )

    solara.Markdown(
        f"**Habitacion:** {modelo.ancho} x {modelo.alto}"
    )

    solara.Markdown(
        f"**Pasos ejecutados:** "
        f"{modelo.pasosEjecutados} / {modelo.tiempoMaximo}"
    )

    solara.Markdown(
        f"**Limpieza:** {porcentajeLimpieza:.2f}%"
    )

    solara.Markdown(
        f"**Movimientos totales:** "
        f"{modelo.movimientosTotales}"
    )

    solara.Markdown(
        f"**Celdas sucias restantes:** "
        f"{cantidadSucias}"
    )

    if modelo.tiempoLimpieza is not None:
        solara.Markdown(
            f"**Tiempo de limpieza completa:** "
            f"{modelo.tiempoLimpieza} pasos"
        )


# Descripcion: Explica los colores utilizados
#              para identificar los agentes.
# Parametros:
#     modelo: Instancia activa del modelo.
# Retorno: Componente visual de Solara.
@solara.component
def mostrarLeyenda(modelo):
    solara.Markdown("### Leyenda")

    solara.Markdown(
        "- 🔵 Robot de limpieza\n"
        "- 🟥 Celda sucia\n"
        "- 🟩 Celda limpia"
    )

    solara.Markdown(
        f"**Suciedad inicial:** "
        f"{modelo.porcentajeSuciedad}%"
    )


# Parametros configurables de la simulacion.
PARAMETROS_MODELO = {
    "ancho": Slider(
        "Ancho (columnas)",
        value=10,
        min=1,
        max=30,
        step=1,
    ),
    "alto": Slider(
        "Alto (filas)",
        value=10,
        min=1,
        max=30,
        step=1,
    ),
    "numeroAgentes": Slider(
        "Numero de robots",
        value=5,
        min=1,
        max=30,
        step=1,
    ),
    "porcentajeSuciedad": Slider(
        "Celdas inicialmente sucias (%)",
        value=30,
        min=0,
        max=100,
        step=5,
    ),
    "tiempoMaximo": Slider(
        "Tiempo maximo (pasos)",
        value=1000,
        min=1,
        max=5000,
        step=1,
    ),
    "semilla": Slider(
        "Semilla aleatoria",
        value=42,
        min=0,
        max=10000,
        step=1,
    ),
}


# Inicializacion del modelo compartido.
modeloInicial = ModeloLimpieza()


# Configuracion del renderizador Matplotlib.
renderizador = (
    SpaceRenderer(
        model=modeloInicial,
        backend="matplotlib",
    )
    .setup_agents(representarAgente)
    .render()
)

renderizador.post_process = configurarGrafica


# Graficas de las estadisticas de limpieza.
graficaLimpieza = make_plot_component(
    "Limpieza (%)",
    backend="matplotlib",
)

graficaMovimientos = make_plot_component(
    "Movimientos",
    backend="matplotlib",
)


# Configuracion de la interfaz web.
page = SolaraViz(
    model=modeloInicial,
    renderer=renderizador,
    components=[
        (mostrarEstado, 0),
        (mostrarLeyenda, 0),
        graficaLimpieza,
        graficaMovimientos,
    ],
    model_params=PARAMETROS_MODELO,
    name="Robots de Limpieza Reactivos | TC2008B SMA",
    play_interval=150,
)
