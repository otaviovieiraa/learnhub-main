#!/bin/bash

# Script de entrypoint para container Django em produção
# Garante que o banco de dados existe antes de rodar migrações

set -e

# Variáveis padrão
DB_NAME="${DATABASE_NAME:-learnhub_db}"
DB_USER="${DATABASE_USER:-learnhub_user}"
DB_PASSWORD="${DATABASE_PASSWORD:-postgres_secure_password_here}"
DB_HOST="${DATABASE_HOST:-postgres}"
DB_PORT="${DATABASE_PORT:-5432}"

echo "=== Iniciando LearnHub ==="
echo "Banco de dados: $DB_HOST:$DB_PORT/$DB_NAME"

# Aguardar PostgreSQL ficar pronto
echo "Aguardando PostgreSQL ficar acessível..."
for i in {1..30}; do
    if psql \
        -h "$DB_HOST" \
        -U "$DB_USER" \
        -d "postgres" \
        -c "SELECT 1" \
        >/dev/null 2>&1; then
        echo "✓ PostgreSQL está pronto!"
        break
    fi
    
    if [ $i -eq 30 ]; then
        echo "✗ PostgreSQL não respondeu após 30 tentativas"
        exit 1
    fi
    
    echo "  Tentativa $i/30 - aguardando..."
    sleep 1
done

# Criar banco de dados se não existir
echo "Verificando banco de dados: $DB_NAME"
DB_EXISTS=$(psql \
    -h "$DB_HOST" \
    -U "$DB_USER" \
    -d "postgres" \
    -t -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" \
    2>/dev/null || echo "")

if [ -z "$DB_EXISTS" ]; then
    echo "✓ Criando banco de dados: $DB_NAME"
    psql \
        -h "$DB_HOST" \
        -U "$DB_USER" \
        -d "postgres" \
        -c "CREATE DATABASE \"$DB_NAME\" OWNER \"$DB_USER\";"
else
    echo "✓ Banco de dados já existe"
fi

# Executar migrações Django
echo "Executando migrações Django..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "=== Setup concluído! Iniciando aplicação ==="

# Executar comando passado (geralmente gunicorn ou runserver)
exec "$@"
