# Sistema Multiagente de Robots de Limpieza

**Materia:** TC2008B — Modelación de Sistemas Multiagentes

**Integrantes:**
- Said Valseca Figueroa — Matrícula: A01801372
- Lorena Antonio Monraga — Matrícula: A01801978

## Descripción

Simulación de robots de limpieza reactivos desarrollada en Python utilizando **Mesa**.

Los robots se desplazan aleatoriamente dentro de una habitación de M×N celdas y limpian las celdas sucias. El proyecto permite analizar cómo influye la cantidad de agentes en el tiempo de limpieza y los movimientos realizados.

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
- Configura automáticamente el tipo MIME de los archivos `.mjs` utilizados por Solara.
- Comprueba que la configuración se haya realizado correctamente.

No es necesario activar manualmente el entorno virtual.

## Ejecución

### 1. Simulación visual (`app.py`)

```powershell
.\.venv\Scripts\python.exe -m solara run app.py
```

Abrir en el navegador:

http://localhost:8765

La interfaz permite configurar el tamaño de la habitación, cantidad de robots, porcentaje de suciedad, tiempo máximo y semilla aleatoria.

Para detener el servidor, presionar `Ctrl + C`.

### 2. Experimentos estadísticos (`experiments.py`)

```powershell
.\.venv\Scripts\python.exe experiments.py
```

Ejecuta **150 simulaciones** (30 repeticiones con 1, 2, 3, 5 y 10 robots) y genera estadísticas y gráficas comparativas.

### 3. Programa principal (`main.py`)

```powershell
.\.venv\Scripts\python.exe main.py
```

Ejecuta los experimentos utilizando la configuración principal del proyecto.

No es necesario ejecutar `main.py` y `experiments.py` por separado para generar los mismos resultados.

## Resultados

Los archivos generados se guardan en:

- `resultados/`: archivos CSV con los datos individuales y los resúmenes estadísticos.
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

- Los archivos `agents.py` y `model.py` son utilizados internamente por la simulación y no necesitan ejecutarse directamente.
- La carpeta `.venv` se genera automáticamente y no debe subirse a GitHub.
- Si el navegador conserva una versión anterior de la interfaz, realizar una recarga forzada con `Ctrl + Shift + R`.
- La ejecución requiere que las políticas de seguridad del equipo permitan cargar las bibliotecas de Python.

---

**Tecnológico de Monterrey — 2026**
