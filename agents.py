
# Descripcion: Define las celdas y los agentes reactivos
#              de una simulacion de robots de limpieza.
# Autores:
#     Said Valseca - Matricula: ____________
#     Lorena Antonio - Matricula: ____________
# Fecha de creacion: 16/11/2026

from mesa.discrete_space import CellAgent, FixedAgent


DIRECCIONES = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


class CeldaLimpieza(FixedAgent):
    """Representa el estado de limpieza de una celda."""

    # Descripcion: Inicializa una celda con su estado.
    # Parametros:
    #     model: Modelo al que pertenece la celda.
    #     cell: Posicion de la celda en la cuadricula.
    #     estaSucia: Estado inicial de suciedad.
    # Retorno: Ninguno.
    def __init__(self, model, cell, estaSucia=False):
        super().__init__(model)

        self.cell = cell
        self.estaSucia = estaSucia


class RobotLimpieza(CellAgent):
    """Agente reactivo que limpia y se mueve al azar."""

    # Descripcion: Inicializa un robot en su posicion.
    # Parametros:
    #     model: Modelo al que pertenece el robot.
    #     cell: Celda inicial del robot.
    # Retorno: Ninguno.
    def __init__(self, model, cell):
        super().__init__(model)

        self.cell = cell
        self.movimientosRealizados = 0
        self.celdasLimpiadas = 0
        self.intentosFallidos = 0

    # Descripcion: Ejecuta una accion reactiva del robot.
    # Parametros: Ninguno.
    # Retorno: Ninguno.
    def step(self):
        posicionActual = self.cell.coordinate

        if self.model.estaCeldaSucia(posicionActual):
            self.model.limpiarCelda(posicionActual)
            self.celdasLimpiadas += 1
        else:
            self.moverAleatoriamente()

    # Descripcion: Elige una de las ocho direcciones y
    #              se mueve si la posicion es valida.
    # Parametros: Ninguno.
    # Retorno: Ninguno.
    def moverAleatoriamente(self):
        direccion = self.random.choice(DIRECCIONES)

        posicionActual = self.cell.coordinate

        nuevaX = posicionActual[0] + direccion[0]
        nuevaY = posicionActual[1] + direccion[1]

        nuevaPosicion = (nuevaX, nuevaY)

        if self.model.esPosicionValida(nuevaPosicion):
            nuevaCelda = self.model.grid[nuevaPosicion]

            self.move_to(nuevaCelda)

            self.movimientosRealizados += 1
            self.model.movimientosTotales += 1
        else:
            self.intentosFallidos += 1
