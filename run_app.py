
# Descripcion: Inicia la interfaz web de Mesa
#              configurando los recursos JavaScript.
# Autores:
#     Said Valseca Figueroa - A01801372
#     Lorena Antonio Monraga - A01801978
# Fecha de modificacion: 16/11/2026

import mimetypes
import os
import runpy
import sys
from pathlib import Path


# Descripcion: Configura el tipo MIME de JavaScript
#              e inicia el servidor web de Solara.
# Parametros: Ninguno.
# Retorno: Ninguno.
def main():
    mimetypes.init()

    mimetypes.add_type(
        "application/javascript",
        ".mjs",
        strict=True,
    )

    tipoMime = mimetypes.guess_type(
        "grid-layout-plus.mjs"
    )[0]

    if tipoMime != "application/javascript":
        raise RuntimeError(
            "No se pudo configurar el tipo MIME."
        )

    carpetaProyecto = Path(__file__).resolve().parent

    os.chdir(carpetaProyecto)

    # El modo produccion evita la recarga automatica
    # del servidor durante esta ejecucion.
    os.environ["SOLARA_MODE"] = "production"

    sys.argv = [
        "solara",
        "run",
        str(carpetaProyecto / "app.py"),
        "--production",
    ]

    print("Iniciando simulacion de robots de limpieza.")
    print("Tipo MIME .mjs:", tipoMime)

    runpy.run_module(
        "solara",
        run_name="__main__",
        alter_sys=True,
    )


if __name__ == "__main__":
    main()
