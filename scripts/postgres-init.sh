#!/bin/bash

# Script para criar banco de dados e usuário PostgreSQL
# Executado após o PostgreSQL iniciar

set -e

# Variáveis padrão se não forem definidas
DB_NAME="${DATABASE_NAME:-learnhub_db}"
DB_USER="${DATABASE_USER:-learnhub_user}"
DB_PASSWORD="${DATABASE_PASSWORD:-postgres_secure_password_here}"

echo "Aguardando PostgreSQL ficar pronto..."
until PGPASSWORD="$DB_PASSWORD" psql -h "$POSTGRES_HOST" -U "$DB_USER" -d postgres -c "SELECT 1" 2>/dev/null; do
  echo "PostgreSQL ainda não está pronto, aguardando..."
  sleep 2
done

echo "PostgreSQL está pronto!"

# Verificar se banco existe, senão criar
echo "Verificando/criando banco de dados: $DB_NAME"
PGPASSWORD="$DB_PASSWORD" psql -h "$POSTGRES_HOST" -U "$DB_USER" -d postgres << EOF
SELECT 'Database $DB_NAME already exists' as status
WHERE EXISTS (SELECT 1 FROM pg_database WHERE datname = '$DB_NAME');

-- Criar banco se não existir
CREATE DATABASE "$DB_NAME" OWNER "$DB_USER";

-- Garantir permissões
GRANT ALL PRIVILEGES ON DATABASE "$DB_NAME" TO "$DB_USER";
EOF

echo "Setup do banco de dados concluído!"
