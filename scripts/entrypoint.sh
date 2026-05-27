#!/bin/sh

set -e

# Variáveis padrão se não definidas
DB_NAME="${DATABASE_NAME:-learnhub_db}"
DB_USER="${DATABASE_USER:-learnhub_user}"
DB_PASSWORD="${DATABASE_PASSWORD:-postgres_secure_password_here}"
DB_HOST="${DATABASE_HOST:-postgres}"
DB_PORT="${DATABASE_PORT:-5432}"

echo "================================"
echo "Iniciando LearnHub em Produção"
echo "================================"
echo "Banco: $DB_HOST:$DB_PORT/$DB_NAME"

# Aguardar PostgreSQL ficar pronto
echo "Aguardando PostgreSQL ficar acessível..."
attempt=1
max_attempts=30

while [ $attempt -le $max_attempts ]; do
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "postgres" -c "SELECT 1" >/dev/null 2>&1; then
        echo "✓ PostgreSQL está pronto!"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        echo "✗ PostgreSQL não respondeu após $max_attempts tentativas"
        exit 1
    fi
    
    echo "  Tentativa $attempt/$max_attempts..."
    attempt=$((attempt + 1))
    sleep 1
done

# Criar banco de dados se não existir
echo "Verificando/criando banco de dados: $DB_NAME"
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "postgres" << EOF
SELECT 'Database exists' WHERE EXISTS (SELECT 1 FROM pg_database WHERE datname = '$DB_NAME');
EOF

DB_EXISTS=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "postgres" -t -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" 2>/dev/null || echo "")

if [ -z "$DB_EXISTS" ]; then
    echo "  Criando banco: $DB_NAME"
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "postgres" -c "CREATE DATABASE \"$DB_NAME\" OWNER \"$DB_USER\";"
    echo "✓ Banco criado com sucesso"
else
    echo "✓ Banco já existe"
fi

echo "Executando migrações Django..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "================================"
echo "✓ Setup concluído com sucesso!"
echo "Iniciando Gunicorn..."
echo "================================"

exec gunicorn \
    --bind 0.0.0.0:3000 \
    --workers 4 \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --access-logfile - \
    --error-logfile - \
    --timeout 120 \
    core.wsgi:application
