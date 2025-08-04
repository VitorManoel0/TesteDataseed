from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dataseed.settings import Settings
from dataseed.models import table_registry
import os
from pathlib import Path

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Configurar a URL do banco de dados
database_url = Settings().DATABASE_URL

# Para o Alembic, converter aiosqlite para sqlite e garantir caminho absoluto
if database_url.startswith('sqlite+aiosqlite://'):
    # Remove o +aiosqlite para o Alembic usar o driver padrão do SQLite
    sqlite_path = database_url.replace('sqlite+aiosqlite:///', '')

    # Se o caminho for relativo, torná-lo absoluto baseado no diretório atual
    if not os.path.isabs(sqlite_path):
        # Obter o diretório do projeto (onde está o alembic.ini)
        project_root = Path(config.config_file_name).parent if config.config_file_name else Path.cwd()
        sqlite_path = project_root / sqlite_path
        sqlite_path = sqlite_path.resolve()

    # Criar o diretório se não existir
    sqlite_path = Path(sqlite_path)
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)

    alembic_url = f'sqlite:///{sqlite_path}'
    print(f"Using database at: {sqlite_path}")
else:
    alembic_url = database_url

config.set_main_option('sqlalchemy.url', alembic_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = table_registry.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Para SQLite, especificar algumas opções úteis
        render_as_batch=True,  # Necessário para ALTER TABLE no SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Configuração específica para SQLite
    configuration = config.get_section(config.config_ini_section, {})
    configuration['sqlalchemy.url'] = alembic_url

    print(f"Connecting to: {alembic_url}")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                # Para SQLite, especificar algumas opções úteis
                render_as_batch=True,  # Necessário para ALTER TABLE no SQLite
                compare_type=True,  # Comparar tipos de dados
                compare_server_default=True,  # Comparar valores padrão
            )

            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print(f"Database URL being used: {alembic_url}")
        raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()