# Sistema Multiagente de Robots de Limpieza

**Materia:** TC2008B — Modelación de Sistemas Multiagentes

**Integrantes:**
- Said Valseca Figueroa — Matrícula: A01801372
- Lorena Antonio Monraga— Matrícula: A01801978

## Descripción

Simulación de robots de limpieza reactivos desarrollada en Python utilizando **Mesa**.

Los robots se desplazan aleatoriamente dentro de una habitación y limpian las celdas sucias. El proyecto permite analizar cómo influye la cantidad de robots en el tiempo de limpieza y los movimientos realizados.

## Requisitos

- Python 3.12
- Git (para clonar el repositorio)

## Instalación

Desde la carpeta del proyecto, crear el entorno virtual:

```powershell
py -3.12 -m venv .venv
```

Instalar las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecución

**1. Simulación visual (app.py)**

```powershell
.\.venv\Scripts\python.exe -m solara run app.py
```

Abrir en el navegador: http://localhost:8765

Para detener el servidor, presionar `Ctrl + C`.

**2. Experimentos estadísticos (experiments.py)**

```powershell
.\.venv\Scripts\python.exe experiments.py
```

Ejecuta 150 simulaciones y genera estadísticas y gráficas comparativas.

**3. Programa principal (main.py)**

```powershell
.\.venv\Scripts\python.exe main.py
```

Ejecuta los experimentos utilizando la configuración principal.

## Resultados

Los archivos generados se guardan en:

- `resultados/`: archivos CSV con los datos de las simulaciones.
- `graficas/`: imágenes PNG con las comparaciones de tiempo, movimientos y limpieza.

## Tecnologías

- Python
- Mesa
- Solara
- Matplotlib
- NetworkX

---

Tecnológico de Monterrey — 2026
