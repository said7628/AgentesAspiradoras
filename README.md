# Sistema Multiagente de Robots de Limpieza

**Materia:** TC2008B — Modelación de Sistemas Multiagentes

**Integrantes:**
- Said Valseca Figueroa — Matrícula: A01801372
- Lorena Antonio Monraga — Matrícula: A01801978

## Descripción

Simulación de robots de limpieza reactivos desarrollada en Python utilizando **Mesa**.

Los robots se desplazan aleatoriamente dentro de una habitación de M×N celdas y limpian las celdas sucias. El proyecto permite analizar cómo influye la cantidad de agentes en el tiempo de limpieza, el porcentaje de celdas limpias y los movimientos realizados.

## Requisitos

- Python 3.12
- Git (para clonar el repositorio)
- Conexión a Internet para instalar las dependencias

## Instalación

Clonar el repositorio y abrir una terminal en la carpeta del proyecto.

Ejecutar el instalador automático:

```powershell
py -3.12 setup.py
```

Este comando:

- Crea el entorno virtual `.venv`.
- Instala las dependencias de `requirements.txt`.
- Configura el tipo MIME de los archivos `.mjs` utilizados por Solara.
- Verifica la configuración del entorno.

**No es necesario activar manualmente el entorno virtual.**

## Ejecución

### 1. Simulación visual (`run_app.py`)

```powershell
.\.venv\Scripts\python.exe run_app.py
```

Abrir en el navegador:

http://localhost:8765

El archivo `run_app.py` inicia Solara y configura el tipo MIME de JavaScript para evitar problemas de visualización en Windows.

La interfaz permite:

- Configurar el tamaño de la habitación.
- Seleccionar la cantidad de robots.
- Modificar el porcentaje inicial de suciedad.
- Establecer el tiempo máximo y la semilla aleatoria.
- Iniciar, pausar, reiniciar y avanzar la simulación.
- Visualizar la habitación y las estadísticas de limpieza.

Para detener el servidor, presionar `Ctrl + C`.

### 2. Experimentos estadísticos (`experiments.py`)

```powershell
.\.venv\Scripts\python.exe experiments.py
```

Ejecuta **150 simulaciones**, correspondientes a 30 repeticiones con 1, 2, 3, 5 y 10 robots.

Genera resultados estadísticos y gráficas para comparar el tiempo, los movimientos y el porcentaje de limpieza.

### 3. Programa principal (`main.py`)

```powershell
.\.venv\Scripts\python.exe main.py
```

Ejecuta los experimentos utilizando la configuración principal del proyecto.

**Nota:** No es necesario ejecutar `main.py` y `experiments.py` por separado para obtener los mismos resultados.

## Resultados

Los archivos generados se almacenan en:

- `resultados/`: archivos CSV con los datos individuales y resúmenes estadísticos.
- `graficas/`: imágenes PNG con las comparaciones de tiempo, movimientos y porcentaje de limpieza.

## Tecnologías

- Python 3.12
- Mesa 3.5.1
- Solara
- Matplotlib
- NumPy
- Pandas
- SciPy
- NetworkX

## Notas

- `agents.py` y `model.py` contienen la lógica de los agentes y del entorno; no se ejecutan directamente.
- `app.py` define la interfaz visual, mientras que `run_app.py` se encarga de iniciarla correctamente.
- `setup.py` prepara automáticamente el entorno de ejecución.
- La carpeta `.venv` no debe subirse a GitHub.
- Si el navegador conserva una versión anterior de la interfaz, realizar una recarga forzada con `Ctrl + Shift + R`.
- La ejecución requiere que las políticas de seguridad del equipo permitan cargar las bibliotecas instaladas.

---

**Tecnológico de Monterrey — 2026**
