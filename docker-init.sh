#!/bin/bash

# ============================================================================
# LearnHub Docker - Initialization Script
# ============================================================================
# This script helps you set up Docker for the LearnHub project
# Usage: ./docker-init.sh [dev|prod]
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker não está instalado. Instale em: https://docker.com/install"
        exit 1
    fi
    print_success "Docker encontrado: $(docker --version)"
}

check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose não está instalado"
        exit 1
    fi
    print_success "Docker Compose encontrado: $(docker-compose --version)"
}

# Setup environment file
setup_env() {
    if [ -f ".env" ]; then
        print_info ".env já existe. Pulando..."
    else
        print_info "Criando .env a partir de .env.example..."
        cp .env.example .env
        print_success ".env criado"
        print_info "⚠️  Edite .env e configure suas variáveis!"
    fi
}

# Setup for development
setup_dev() {
    print_info "Configurando ambiente de DESENVOLVIMENTO..."
    
    setup_env
    
    print_info "Construindo imagem..."
    docker-compose build
    
    print_info "Iniciando containers..."
    docker-compose up -d
    
    print_success "Aguardando PostgreSQL..."
    sleep 3
    
    print_info "Executando migrações..."
    docker-compose exec -T web python manage.py migrate || true
    
    print_success "✨ Ambiente de desenvolvimento pronto!"
    print_info "Acesse em: http://localhost:3000"
    print_info "Para ver logs: docker-compose logs -f web"
}

# Setup for production
setup_prod() {
    print_info "Configurando ambiente de PRODUÇÃO..."
    
    if [ -f ".env" ]; then
        print_info ".env encontrado"
    else
        print_error ".env não encontrado. Crie a partir de .env.example"
        exit 1
    fi
    
    # Verify security settings
    if grep -q 'SECRET_KEY=your-super-secret-key' .env; then
        print_error "SECRET_KEY ainda não foi alterado!"
        exit 1
    fi
    
    if grep -q 'DATABASE_PASSWORD=postgres_secure_password_here' .env; then
        print_error "DATABASE_PASSWORD ainda não foi alterado!"
        exit 1
    fi
    
    if grep -q 'DEBUG=True' .env; then
        print_error "DEBUG ainda está True!"
        exit 1
    fi
    
    print_success "Variáveis de segurança validadas"
    
    print_info "Fazendo build da imagem..."
    docker build -t learnhub:latest .
    
    print_info "Iniciando containers de produção..."
    docker-compose -f docker-compose.prod.yml up -d
    
    print_success "✨ Ambiente de produção pronto!"
    print_info "Acesse em: http://localhost:3000"
}

# Main menu
if [ "$1" == "dev" ]; then
    check_docker
    check_docker_compose
    setup_dev
elif [ "$1" == "prod" ]; then
    check_docker
    check_docker_compose
    setup_prod
else
    echo "Uso: $0 [dev|prod]"
    echo ""
    echo "dev:  Configura ambiente de desenvolvimento com hot reload"
    echo "prod: Configura ambiente de produção com imagem otimizada"
    exit 1
fi
