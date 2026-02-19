GEMINI.md
Dev environment tips
Usa siempre un entorno virtual:
python -m venv venv
Windows:
  venv\Scripts\activate
macOS / Linux:
  source venv/bin/activate
Instala dependencias
pip install -r requirements.txt  pip install -r requirements-dev.txt

Para desarrollo rápido usa pip install -e . (si tienes setup.py o pyproject.toml).
Evita instalar paquetes globales. Siempre trabaja dentro del venv.

Corre todos los tests con:
pytest -v
O con covertura:
pytest --cov=src --cov-report=term-missingopen htmlcov/index.html
Desde la raíz del proyecto también puedes usar:
python -m pytest
Para ejecutar test especificos:
pytest -k "nombre_del_test"
O con patron
pytest -k "scraping or pdf"
Después de mover archivos o cambiar imports, siempre corre:Bash
ruff check .          # linting rápidoruff format .         # formateo (Black compatible)mypy src              # Verificación de tipos estáticos

Todos los tests deben pasar y el linting debe estar limpio antes de hacer commit.
Agrega o actualiza tests por cada cambio que hagas (aunque nadie te lo pida).

PR instructions
Título del PR: Descripción corta y clara
Ejemplos:

Añadir extracción de tablas de PDF
Mejorar logging y manejo de errores en scraper

Antes de hacer commit siempre ejecuta:Bash
ruff check --fix .  ruff format .  pytest  


El CI de GitHub Actions (.github/workflows/ci.yml) debe pasar en verde.


Incluye en la descripción del PR:


Qué se cambió


Por qué


Cómo probarlo


Integracion continua (CI/CD)
Ejemplo basico .github/workflows/ci.yml:
name: CI
on: [push, pull_request]
jobs:  test:    runs-on: ubuntu-latest
    steps:      - uses: actions/checkout@v4      - uses: actions/setup-python@v5        with:          python-version: "3.11"      - run: pip install -r requirements-dev.txt      - run: ruff check .      - run: ruff format --check .      - run: pytest --cov=src