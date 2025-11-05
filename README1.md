# MARCIANITOS — Instrucciones de instalación y uso

Este README explica **cómo clonar, configurar y ejecutar** el juego `MARCIANITOS` en tu máquina usando **Visual Studio Code** y **Git**. Incluye pasos para crear un entorno virtual, instalar dependencias, solucionar problemas comunes y configurar VSCode para ejecutar/depurar.

---

## TL;DR — Inicio rápido

1. Clona el repo:
   ```bash
   git clone https://github.com/xndresmoreno/Marcianitos.git
   ```
2. Entra en la carpeta del proyecto:
   ```bash
   cd Marcianitos
   ```
3. Crea y activa un entorno virtual:
   - Windows (PowerShell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
   - Windows (cmd): `python -m venv .venv && .\.venv\Scripts\activate.bat`
   - macOS / Linux: `python3 -m venv .venv && source .venv/bin/activate`
4. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Crea el archivo de highscore si no existe:
   ```bash
   echo 0 > highscore.txt
   ```
   (o crea un archivo vacío llamado `highscore.txt` en la raíz)
6. Ejecuta el juego:
   ```bash
   python main.py
   ```

---

## Requisitos

- **Python 3.8+** (recomendado 3.10/3.11). Comprueba con `python --version` o `python3 --version`.
- **Git** para clonar el repositorio.
- **Visual Studio Code** con la extensión **Python** instalada (opcional pero recomendado).
- Dependencias de Python: `pygame` (el juego usa `pygame` para la ventana, imágenes y sonido).

> Nota: en Linux puede que necesites paquetes del sistema para que `pygame` funcione correctamente (por ejemplo `libsdl2` y dependencias de audio/imagen). Si `pygame` falla al instalar o al ejecutar, mira la sección "Problemas comunes".

---

## Clonar el repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/xndresmoreno/Marcianitos.git
cd Marcianitos
```

---

## Entorno virtual (recomendado)

Crear un venv evita conflictos entre proyectos.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Dependencias

El archivo [`requirements.txt`](requirements.txt) incluye:

```
pygame>=2.6.0
```

Si instalas nuevas librerías, actualiza el archivo ejecutando:

```bash
pip freeze > requirements.txt
```

---

## Archivos y estructura importante

Asegúrate de que la estructura del proyecto tenga al menos estas entradas:

```
Marcianitos/
├── main.py
├── config.py
├── IMAGENES/
│   ├── E1.webp
│   ├── O2.webp
│   ├── finalboss.webp
│   ├── fondo.webp
│   ├── potenciador.webp
│   └── explosion.webp
├── highscore.txt
├── requirements.txt
└── README.md
```

---

## Ejecutar desde VSCode

1. Abre la carpeta del proyecto en VSCode: `File → Open Folder...` y selecciona `Marcianitos`.
2. Instala la extensión **Python**.
3. Selecciona el intérprete (el venv): `Ctrl+Shift+P` → `Python: Select Interpreter` → elige `.venv`.
4. Abre `main.py` y pulsa `F5` para ejecutar o usa `Run Python File`.

Si prefieres crear una configuración de depuración, usa este `launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Ejecutar main.py",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal"
    }
  ]
}
```

---

## Problemas comunes

### Error al cargar imágenes
- Verifica que los archivos existan en `IMAGENES/`.
- Asegúrate de que los nombres coincidan con los de `config.py`.

### Error `ModuleNotFoundError: No module named 'pygame'`
- Revisa que tu entorno virtual esté activo.
- Reinstala con `pip install pygame`.

### En Linux pygame no abre la ventana
Instala dependencias SDL:
```bash
sudo apt install libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0
```

---

## Buenas prácticas

- Usa `.gitignore` para excluir `.venv/`, `__pycache__/`, y `highscore.txt`.
- Genera ejecutables con `pyinstaller` si quieres compartir el juego sin requerir Python.

---

## Ejemplo de `.gitignore`

```
.venv/
__pycache__/
*.py[cod]
.vscode/
highscore.txt
```

---

Repositorio oficial: [https://github.com/xndresmoreno/Marcianitos](https://github.com/xndresmoreno/Marcianitos)

