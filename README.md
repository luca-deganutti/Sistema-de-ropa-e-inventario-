# Sistema Interno - Distribuidora de Ropa (Starter Template)

Base reusable para proyectos backend con FastAPI + PostgreSQL + SQLAlchemy + Alembic.

## Stack
- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic Settings
- Pytest

## Estructura
```text
app/
  api/v1/
  core/
  db/
  models/
  repositories/
  schemas/
  services/
tests/
alembic/
```

## Setup rápido
1. Crear y activar entorno virtual.
2. Instalar dependencias:
   - `pip install -r requirements-dev.txt`
3. Copiar variables de entorno:
   - `copy .env.example .env` (Windows)
4. Levantar API:
   - `uvicorn app.main:app --reload`
5. Correr tests:
   - `pytest -q`

## Migraciones (Alembic)
- Crear revisión:
  - `alembic revision --autogenerate -m "create initial tables"`
- Aplicar migraciones:
  - `alembic upgrade head`
- Revertir una migración:
  - `alembic downgrade -1`

## Calidad de código
- Formatear:
  - `black .`
- Lint:
  - `ruff check .`
- Tipos:
  - `mypy app`

## Notas
- `get_settings()` devuelve configuración tipada y cacheada.
- `get_db()` maneja el ciclo de vida de sesión de base de datos (abre/cierra).
- `alembic/env.py` usa `Base.metadata` para detectar modelos al autogenerar migraciones.
