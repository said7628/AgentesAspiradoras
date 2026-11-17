
# Descripcion: Implementa el entorno y las estadisticas
#              del sistema multiagente de limpieza.
# Autores:
#     Said Valseca Figueroa - Matricula: A01801372
#     Lorena Antonio Monraga- Matricula: ____________
# Fecha de creacion: 16/11/2026


from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid

from agents import CeldaLimpieza, RobotLimpieza


class ModeloLimpieza(Model):
    """Simula una habitacion con robots reactivos."""

    # Descripcion: Construye e inicializa la simulacion.
    # Parametros:
    #     ancho: Numero de columnas.
    #     alto: Numero de filas.
    #     numeroAgentes: Cantidad de robots.
    #     porcentajeSuciedad: Porcentaje inicial sucio.
    #     tiempoMaximo: Limite de pasos de tiempo.
    #     semilla: Semilla para reproducir los resultados.
    # Retorno: Ninguno.
    def __init__(
        self,
        ancho=10,
        alto=10,
        numeroAgentes=5,
        porcentajeSuciedad=30,
        tiempoMaximo=1000,
        semilla=42,
    ):
        super().__init__(rng=semilla)

        if ancho < 1 or alto < 1:
            raise ValueError(
                "Las dimensiones deben ser positivas."
            )

        if numeroAgentes < 1:
            raise ValueError(
                "Debe existir al menos un robot."
            )

        if not 0 <= porcentajeSuciedad <= 100:
            raise ValueError(
                "El porcentaje debe estar entre 0 y 100."
            )

        if tiempoMaximo < 1:
            raise ValueError(
                "El tiempo maximo debe ser positivo."
            )

        self.ancho = ancho
        self.alto = alto
        self.numeroAgentes = numeroAgentes
        self.porcentajeSuciedad = porcentajeSuciedad
        self.tiempoMaximo = tiempoMaximo
        self.semilla = semilla

        self.totalCeldas = ancho * alto
        self.pasosEjecutados = 0
        self.movimientosTotales = 0
        self.tiempoLimpieza = None

        self.celdasSucias = set()
        self.celdas = {}
        self.robots = []

        self.grid = OrthogonalMooreGrid(
            (ancho, alto),
            capacity=None,
            random=self.random,
            torus=False,
        )

        self.inicializarSuciedad()
        self.inicializarCeldas()
        self.inicializarRobots()

        # Mesa requiere el atributo llamado "datacollector"
        # para generar las graficas de la interfaz web.
        self.datacollector = DataCollector(
            model_reporters={
                "Pasos": "pasosEjecutados",
                "Limpieza (%)": (
                    lambda modelo:
                    modelo.calcularPorcentajeLimpieza()
                ),
                "Movimientos": "movimientosTotales",
                "Celdas sucias": (
                    lambda modelo: len(modelo.celdasSucias)
                ),
            }
        )

        self.datacollector.collect(self)

        self.running = len(self.celdasSucias) > 0

        if not self.running:
            self.tiempoLimpieza = 0

    # Descripcion: Distribuye aleatoriamente la suciedad
    #              sin repetir posiciones.
    # Parametros: Ninguno.
    # Retorno: Ninguno.
    def inicializarSuciedad(self):
        posiciones = [
            (x, y)
            for x in range(self.ancho)
            for y in range(self.alto)
        ]

        cantidadSucias = round(
            self.totalCeldas * self.porcentajeSuciedad / 100.0
        )

        posicionesSucias = self.random.sample(
            posiciones,
            cantidadSucias,
        )

        self.celdasSucias = set(posicionesSucias)

    # Descripcion: Crea las celdas visuales del entorno.
    # Parametros: Ninguno.
    # Retorno: Ninguno.
    def inicializarCeldas(self):
        for celda in self.grid.all_cells:
            posicion = celda.coordinate

            agenteCelda = CeldaLimpieza(
                self,
                celda,
                estaSucia=posicion in self.celdasSucias,
            )

            self.celdas[posicion] = agenteCelda

    # Descripcion: Crea los robots en la posicion [1,1].
    # Parametros: Ninguno.
    # Retorno: Ninguno.
    def inicializarRobots(self):
        posicionInicial = (0, 0)

        celdaInicial = self.grid[posicionInicial]

        for _ in range(self.numeroAgentes):
            robot = RobotLimpieza(
                self,
                celdaInicial,
            )

            self.robots.append(robot)

    # Descripcion: Verifica que una posicion pertenezca
    #              a la habitacion.
    # Parametros:
    #     posicion: Tupla con coordenadas x, y.
    # Retorno: True si pertenece al entorno.
    def esPosicionValida(self, posicion):
        x, y = posicion

        return (
            0 <= x < self.ancho
            and 0 <= y < self.alto
        )

    # Descripcion: Consulta si existe suciedad.
    # Parametros:
    #     posicion: Coordenadas de la celda.
    # Retorno: True si la celda esta sucia.
    def estaCeldaSucia(self, posicion):
        return posicion in self.celdasSucias

    # Descripcion: Elimina la suciedad de una celda.
    # Parametros:
    #     posicion: Coordenadas de la celda.
    # Retorno: Ninguno.
    def limpiarCelda(self, posicion):
        if posicion in self.celdasSucias:
            self.celdasSucias.remove(posicion)

            self.celdas[posicion].estaSucia = False

    # Descripcion: Calcula la proporcion de celdas limpias.
    # Parametros: Ninguno.
    # Retorno: Porcentaje de limpieza entre 0 y 100.
    def calcularPorcentajeLimpieza(self):
        cantidadLimpias = (
            self.totalCeldas - len(self.celdasSucias)
        )

        return cantidadLimpias / self.totalCeldas * 100.0

    # Descripcion: Ejecuta un paso para todos los robots.
    # Parametros: Ninguno.
    # Retorno: Ninguno.
    def step(self):
        if self.running:
            ordenRobots = self.robots.copy()

            self.random.shuffle(ordenRobots)

            for robot in ordenRobots:
                robot.step()

            self.pasosEjecutados += 1

            if len(self.celdasSucias) == 0:
                self.tiempoLimpieza = self.pasosEjecutados
                self.running = False

            if self.pasosEjecutados >= self.tiempoMaximo:
                self.running = False

            self.datacollector.collect(self)

    # Descripcion: Ejecuta la simulacion hasta terminar.
    # Parametros: Ninguno.
    # Retorno: Diccionario con las estadisticas finales.
    def ejecutarSimulacion(self):
        while self.running:
            self.step()

        return self.obtenerEstadisticas()

    # Descripcion: Reune las metricas finales del modelo.
    # Parametros: Ninguno.
    # Retorno: Diccionario de resultados.
    def obtenerEstadisticas(self):
        return {
            "ancho": self.ancho,
            "alto": self.alto,
            "numeroAgentes": self.numeroAgentes,
            "porcentajeSuciedad": self.porcentajeSuciedad,
            "tiempoMaximo": self.tiempoMaximo,
            "semilla": self.semilla,
            "pasosEjecutados": self.pasosEjecutados,
            "tiempoLimpieza": self.tiempoLimpieza,
            "limpiezaCompleta": (
                len(self.celdasSucias) == 0
            ),
            "porcentajeLimpieza": (
                self.calcularPorcentajeLimpieza()
            ),
            "movimientosTotales": self.movimientosTotales,
            "celdasSuciasRestantes": len(
                self.celdasSucias
            ),
            "intentosFallidos": sum(
                robot.intentosFallidos
                for robot in self.robots
            ),
        }
