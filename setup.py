
# Descripcion: Prepara el entorno virtual del proyecto
#              y configura los recursos web de Solara.
# Autores:
#     Said Valseca - Matricula: ____________
#     Lorena Antonio - Matricula: ____________
# Fecha de creacion/modificacion: 16/11/2026

import subprocess
import sys
import venv
from pathlib import Path


CARPETA_PROYECTO = Path(__file__).resolve().parent
CARPETA_ENTORNO = CARPETA_PROYECTO / ".venv"


# Descripcion: Crea el entorno, instala los paquetes
#              y registra el tipo MIME de JavaScript.
# Parametros: Ninguno.
# Retorno: Ninguno.
def main():
    if sys.version_info < (3, 12):
        raise RuntimeError(
            "Se requiere Python 3.12 o superior."
        )

    if not CARPETA_ENTORNO.exists():
        venv.create(
            CARPETA_ENTORNO,
            with_pip=True,
        )

    if sys.platform == "win32":
        ejecutable = (
            CARPETA_ENTORNO / "Scripts" / "python.exe"
        )
    else:
        ejecutable = (
            CARPETA_ENTORNO / "bin" / "python"
        )

    subprocess.run(
        [
            str(ejecutable),
            "-m",
            "pip",
            "install",
            "-r",
            str(CARPETA_PROYECTO / "requirements.txt"),
        ],
        check=True,
    )

    # Se registra .mjs como JavaScript para evitar
    # conflictos con los tipos MIME de Windows.
    resultado = subprocess.check_output(
        [
            str(ejecutable),
            "-c",
            "import sysconfig; "
            "print(sysconfig.get_path('purelib'))",
        ],
        text=True,
    ).strip()

    archivoConfiguracion = (
        Path(resultado) / "sitecustomize.py"
    )

    archivoConfiguracion.write_text(
        "import mimetypes\n"
        "mimetypes.init()\n"
        "mimetypes.add_type("
        "'application/javascript', '.mjs', strict=True)\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            str(ejecutable),
            "-c",
            "import mimetypes; "
            "assert mimetypes.guess_type('test.mjs')[0] "
            "== 'application/javascript'",
        ],
        check=True,
    )

    print("Entorno configurado correctamente.")


if __name__ == "__main__":
    main()
