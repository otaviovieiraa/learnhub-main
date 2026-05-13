# Quick Reference - LearnHub Docker

## 🚀 Início Rápido

```bash
# Desenvolvimento
cp .env.example .env
docker-compose up -d
docker-compose exec web python manage.py migrate
open http://localhost:3000

# Produção
cp .env.example .env
# Editar .env com valores reais
docker build -t learnhub:latest .
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Variáveis de Ambiente

```env
# Obrigatórias em Produção
SECRET_KEY=<gerar novo>
DATABASE_PASSWORD=<senha forte>
ALLOWED_HOSTS=seu-dominio.com

# Padrão
DEBUG=False
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=learnhub_db
DATABASE_USER=postgres
DATABASE_HOST=postgres
DATABASE_PORT=5432
```

## 🐳 Arquivos Docker

| Arquivo | Uso | Características |
|---------|-----|-----------------|
| `Dockerfile` | Produção | Multi-stage, Alpine, non-root |
| `Dockerfile.dev` | Dev | Sem otimizações, hot reload |
| `docker-compose.yml` | Dev | Volumes, auto-reload |
| `docker-compose.prod.yml` | Prod | Sem bind mounts, healthchecks |
| `docker-compose.nginx.yml` | Prod+Nginx | Reverse proxy, SSL ready |

## 🛠️ Comandos Mais Usados

```bash
# Desenvolvimento
make dev                  # Inicia
make dev-stop            # Para
make dev-logs            # Logs
make migrate             # Migrações
make createsuperuser     # Criar admin

# Produção
make prod                # Inicia
docker build -t learnhub:latest .
docker-compose -f docker-compose.prod.yml up -d

# Utilidades
make healthcheck         # Verificar saúde
make shell              # Django shell
make clean              # Limpar tudo
```

## 🔐 Segurança

✅ Sem credenciais hardcoded
✅ Sem root no container
✅ Imagem Alpine (50MB)
✅ Healthchecks automáticos
✅ Variáveis de ambiente apenas

## 📊 Status

```bash
# Ver containers
docker-compose ps

# Ver logs
docker-compose logs -f web

# Acessar BD
docker-compose exec postgres psql -U postgres -d learnhub_db

# Health check
curl http://localhost:3000/health/
```

## 🐛 Problemas Comuns

| Problema | Solução |
|----------|---------|
| Porta em uso | `make clean`, mudar porta em .env |
| BD não conecta | `docker-compose ps`, verificar healthcheck |
| Container falha | `docker-compose logs web` |
| Migração falha | `docker-compose exec web python manage.py migrate --fake-initial` |

## 📚 Documentação Completa

- [DOCKER.md](DOCKER.md) - Setup e deployment
- [SECURITY.md](SECURITY.md) - Segurança e secrets
- [Makefile](Makefile) - Todos os comandos
