# Actividad: Agentes Aspiradoras
# Fecha: 16/11/2026
# Autores:
#     A01801372 Said Valseca Figueroa
#     A01801978 Lorena Antonio Monraga
# Descripcion: Implementa la interfaz web del sistema
#              multiagente de robots de limpieza
#              utilizando Mesa, Solara y Matplotlib.

import solara

from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle
from mesa.visualization.utils import update_counter

from agents import CeldaLimpieza, RobotLimpieza
from model import ModeloLimpieza


# Descripcion: Define colores, tamanos y simbolos de cada agente.
# Parametros:
#     agente: Robot o celda representada en la habitacion.
# Retorno: Estilo grafico del agente.
def representarAgente(agente):
    dimension = max(agente.model.ancho, agente.model.alto)
    escala = min(1.0, 10.0 / dimension) ** 2

    if isinstance(agente, RobotLimpieza):
        return AgentPortrayalStyle(
            color="#6D4AFF",
            marker="o",
            size=180 * escala,
            zorder=3,
        )

    if isinstance(agente, CeldaLimpieza):
        colorCelda = "#FF8A8E" if agente.estaSucia else "#A8E2CF"
        return AgentPortrayalStyle(
            color=colorCelda,
            marker="s",
            size=300 * escala,
            zorder=1,
        )

    return AgentPortrayalStyle(color="#94A3B8", marker="s", size=20)


# Descripcion: Mejora el fondo y el tamano del tablero de la habitacion.
# Parametros:
#     ejes: Ejes de la figura Matplotlib del tablero.
# Retorno: Ninguno.
def configurarGrafica(ejes):
    ejes.figure.set_size_inches(7, 7)
    ejes.figure.patch.set_facecolor("#FFFFFF")
    ejes.set_facecolor("#F7F9FF")
    ejes.set_aspect("equal", adjustable="box")
    ejes.set_xticks([])
    ejes.set_yticks([])
    ejes.set_title("Habitacion de limpieza", color="#252444", fontsize=15, pad=15)
    for borde in ejes.spines.values():
        borde.set_color("#DDE3F0")


# Descripcion: Aplica un estilo uniforme a las graficas de resultados.
# Parametros:
#     ejes: Ejes del grafico.
#     titulo: Encabezado del grafico.
#     color: Color de la curva.
# Retorno: Ninguno.
def configurarCurva(ejes, titulo, color):
    ejes.figure.set_size_inches(5, 3.4)
    ejes.figure.patch.set_facecolor("#FFFFFF")
    ejes.set_facecolor("#FFFFFF")
    ejes.set_title(titulo, color="#252444", fontsize=11, pad=10)
    ejes.set_xlabel("Pasos", color="#667085", fontsize=9)
    ejes.grid(alpha=0.25, color="#CBD5E1", linestyle="--")
    ejes.tick_params(colors="#667085", labelsize=8)

    for linea in ejes.get_lines():
        linea.set_color(color)
        linea.set_linewidth(2.5)

    for borde in ejes.spines.values():
        borde.set_color("#E4E7F0")

    ejes.figure.tight_layout(pad=1.5)


# Descripcion: Personaliza la grafica del porcentaje de limpieza.
# Parametros:
#     ejes: Ejes del grafico de limpieza.
# Retorno: Ninguno.
def configurarLimpieza(ejes):
    configurarCurva(ejes, "Progreso de limpieza", "#6D4AFF")
    ejes.set_ylabel("Limpieza (%)", color="#667085", fontsize=9)
    ejes.set_ylim(0, 105)


# Descripcion: Personaliza la grafica de movimientos acumulados.
# Parametros:
#     ejes: Ejes del grafico de movimientos.
# Retorno: Ninguno.
def configurarMovimientos(ejes):
    configurarCurva(ejes, "Movimientos realizados", "#12A98C")
    ejes.set_ylabel("Movimientos", color="#667085", fontsize=9)


# Descripcion: Presenta un indicador numerico dentro de una tarjeta.
# Parametros:
#     titulo: Nombre del indicador.
#     valor: Valor actual del indicador.
#     color: Color visual del valor.
# Retorno: Componente visual de Solara.
@solara.component
def mostrarIndicador(titulo, valor, color):
    with solara.Card(classes=["tarjeta-indicador"], margin=0, elevation=0):
        solara.Text(
            titulo,
            style={"color": "#667085", "fontSize": "12px", "fontWeight": "600"},
        )
        solara.Text(
            str(valor),
            style={"color": color, "fontSize": "23px", "fontWeight": "800"},
        )


# Descripcion: Agrupa estadisticas, leyenda y graficas en un panel.
# Parametros:
#     modelo: Instancia actual de ModeloLimpieza.
# Retorno: Componente visual que se actualiza en cada paso.
@solara.component
def mostrarPanel(modelo):
    update_counter.get()

    porcentajeLimpieza = modelo.calcularPorcentajeLimpieza()
    cantidadSucias = len(modelo.celdasSucias)

    if cantidadSucias == 0:
        estado = "Limpieza completada"
    elif modelo.pasosEjecutados >= modelo.tiempoMaximo:
        estado = "Tiempo maximo alcanzado"
    elif modelo.pasosEjecutados == 0:
        estado = "Lista para iniciar"
    else:
        estado = "En proceso"

    solara.Style(
        """
        .v-application .v-main__wrap { background: #F5F7FC !important; }
        .v-app-bar { background: linear-gradient(100deg, #5441B8, #926BE7) !important; }
        .react-grid-item { background: #FFFFFF; border: 1px solid #E6EAF3;
          border-radius: 18px; padding: 12px; box-shadow: 0 6px 24px rgba(37,36,68,.06); }
        .tarjeta-indicador { background: #F7F8FD !important; border: 1px solid #E9EAF5;
          border-radius: 14px !important; padding: 4px; box-shadow: none !important; }
        .panel-datos .v-card__title { color: #252444; font-weight: 700; }
        """
    )

    with solara.Column(gap="12px", classes=["panel-datos"]):
        with solara.Card("Resumen en tiempo real", margin=0, elevation=0):
            solara.Text(
                estado,
                style={"color": "#5945CA", "fontSize": "14px", "fontWeight": "700"},
            )
            solara.ProgressLinear(value=float(porcentajeLimpieza), color="purple")
            solara.Text(
                f"{porcentajeLimpieza:.2f}% de la habitacion limpia",
                style={"color": "#667085", "fontSize": "12px"},
            )

            with solara.Columns([1, 1, 1], wrap=True):
                mostrarIndicador("Robots", modelo.numeroAgentes, "#5945CA")
                mostrarIndicador(
                    "Pasos", f"{modelo.pasosEjecutados} / {modelo.tiempoMaximo}", "#252444"
                )
                mostrarIndicador("Movimientos", modelo.movimientosTotales, "#12A98C")
                mostrarIndicador(
                    "Habitacion", f"{modelo.ancho} x {modelo.alto}", "#252444"
                )
                mostrarIndicador("Celdas sucias", cantidadSucias, "#E56A78")
                mostrarIndicador(
                    "Tiempo de limpieza",
                    f"{modelo.tiempoLimpieza} pasos"
                    if modelo.tiempoLimpieza is not None else "--",
                    "#5945CA",
                )

        with solara.Card("Evolucion de la simulacion", margin=0, elevation=0):
            with solara.Columns([1, 1], wrap=True):
                graficaLimpieza[0](modelo)
                graficaMovimientos[0](modelo)

        with solara.Card("Leyenda", margin=0, elevation=0):
            with solara.Row(gap="18px", style={"flexWrap": "wrap"}):
                solara.Text("🟣 Robot", style={"fontSize": "13px"})
                solara.Text("🟥 Celda sucia", style={"fontSize": "13px"})
                solara.Text("🟩 Celda limpia", style={"fontSize": "13px"})
            solara.Text(
                f"Suciedad inicial: {modelo.porcentajeSuciedad}%",
                style={"color": "#667085", "fontSize": "12px"},
            )


# Parametros configurables del modelo. Se conservan sus nombres originales.
PARAMETROS_MODELO = {
    "ancho": Slider("Ancho (columnas)", value=10, min=1, max=30, step=1),
    "alto": Slider("Alto (filas)", value=10, min=1, max=30, step=1),
    "numeroAgentes": Slider("Numero de robots", value=5, min=1, max=30, step=1),
    "porcentajeSuciedad": Slider(
        "Celdas inicialmente sucias (%)", value=30, min=0, max=100, step=5
    ),
    "tiempoMaximo": Slider("Tiempo maximo (pasos)", value=1000, min=1, max=5000, step=1),
    "semilla": Slider("Semilla aleatoria", value=42, min=0, max=10000, step=1),
}


# Instancia principal del modelo.
modeloInicial = ModeloLimpieza()


# Renderizador de la habitacion. Conserva el backend Matplotlib.
renderizador = (
    SpaceRenderer(model=modeloInicial, backend="matplotlib")
    .setup_agents(representarAgente)
    .render()
)
renderizador.post_process = configurarGrafica


# Graficas conectadas a las variables recopiladas por el modelo.
graficaLimpieza = make_plot_component(
    "Limpieza (%)", post_process=configurarLimpieza, backend="matplotlib"
)
graficaMovimientos = make_plot_component(
    "Movimientos", post_process=configurarMovimientos, backend="matplotlib"
)


# Aplicacion que importa run_app.py. Mantiene controles y reinicio de Mesa.
page = SolaraViz(
    model=modeloInicial,
    renderer=renderizador,
    components=[(mostrarPanel, 0)],
    model_params=PARAMETROS_MODELO,
    name="Robots de Limpieza | TC2008B SMA",
    play_interval=150,
)

