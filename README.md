## Database migration

#### It's necessary the environment variable: `DATABASE_URL`

New migration:

```
alembic revision -m 'create_tables' --rev-id='001' --autogenerate
```

Run migration to head revision:

```
alembic upgrade head
```

Run migration to previous revision:

```
alembic downgrade -1
```

## Instalação Local (Atualizada)
- Rodar o comando `virtualenv` para criar o virtual enviroment.
- Step 1: Update and Refresh Repository Lists
    - sudo apt update
    - sudo apt-get install python3-dev
- Executar o comando pip install -r requirements.txt

