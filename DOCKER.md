# Docker Setup - LearnHub Project

## 📋 Estrutura

```
.
├── Dockerfile              # Build multi-stage para produção
├── Dockerfile.dev          # Build para desenvolvimento
├── docker-compose.yml      # Orquestração de desenvolvimento
├── docker-compose.prod.yml # Orquestração de produção
├── .dockerignore           # Arquivos excluídos do build
├── .env.example            # Template de variáveis de ambiente
├── requirements.txt        # Dependências Python
├── scripts/
│   ├── entrypoint.sh       # Script de inicialização da aplicação
│   ├── healthcheck-django.sh
│   └── healthcheck-postgres.sh
└── core/
    ├── settings.py         # Atualizado com suporte a variáveis de ambiente
    └── wsgi.py
```

## 🚀 Quick Start - Desenvolvimento

### 1. Preparar ambiente
```bash
# Clonar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
nano .env
```

### 2. Iniciar containers
```bash
# Construir e iniciar
docker-compose up -d

# Verificar status
docker-compose ps
```

### 3. Executar migrações (primeira vez)
```bash
# Aplicar migrações
docker-compose exec web python manage.py migrate

# Criar superuser (opcional)
docker-compose exec web python manage.py createsuperuser
```

### 4. Acessar aplicação
- Frontend: http://localhost:3000
- PostgreSQL: localhost:5432

### 5. Parar containers
```bash
docker-compose down
```

---

## 🏭 Produção

### 1. Preparar ambiente
```bash
cp .env.example .env
# Editar .env com valores seguros e reais
```

### 2. Build da imagem
```bash
# Build com tag específica
docker build -t learnhub:v1.0.0 .
docker tag learnhub:v1.0.0 learnhub:latest

# Ou com registro (Docker Hub, ECR, etc)
docker tag learnhub:latest seu-usuario/learnhub:latest
docker push seu-usuario/learnhub:latest
```

### 3. Deploy
```bash
# Usando docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d

# Verificar status
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f web
```

### 4. Executar migrações em produção
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

---

## 🔒 Segurança

### ✅ Implementado

- [x] **Nenhuma credencial hardcoded** - todas as variáveis estão em `.env`
- [x] **Container não roda como root** - usa usuário `appuser` (UID 1000)
- [x] **Imagem Alpine** - 50MB vs 900MB (python:3.11 padrão)
- [x] **Multi-stage build** - apenas dependências de runtime na imagem final
- [x] **Non-root user** - aplicação roda com privilégios mínimos
- [x] **Security opt** - `no-new-privileges:true` em produção
- [x] **Healthcheck** - monitoramento automático dos serviços

### 📋 Checklist de segurança

Antes de fazer deploy em produção:

- [ ] Gerar novo `SECRET_KEY` seguro
- [ ] Definir `DEBUG=False`
- [ ] Configurar `ALLOWED_HOSTS` com seus domínios
- [ ] Usar senha forte para `DATABASE_PASSWORD`
- [ ] Configurar credenciais de superuser
- [ ] Revisar variáveis em `.env` antes de subir
- [ ] Usar secrets do Docker Swarm ou K8s em produção
- [ ] Configurar HTTPS/SSL com reverse proxy (nginx, traefik)

---

## 📊 Variáveis de Ambiente

| Variável | Descrição | Default |
|----------|-----------|---------|
| `DEBUG` | Modo debug Django | `False` (prod) |
| `SECRET_KEY` | Chave secreta Django | ⚠️ **MUDAR** |
| `ALLOWED_HOSTS` | Hosts permitidos | localhost,127.0.0.1 |
| `DATABASE_ENGINE` | Engine do banco | postgresql |
| `DATABASE_NAME` | Nome do banco | learnhub_db |
| `DATABASE_USER` | Usuário postgres | postgres |
| `DATABASE_PASSWORD` | Senha postgres | ⚠️ **MUDAR** |
| `DATABASE_HOST` | Host postgres | postgres |
| `DATABASE_PORT` | Porta postgres | 5432 |

---

## 🐛 Troubleshooting

### Container web não inicia
```bash
# Ver logs detalhados
docker-compose logs web

# Executar comando manualmente
docker-compose run --rm web python manage.py check
```

### PostgreSQL não conecta
```bash
# Verificar se container está saudável
docker-compose ps

# Testar conexão
docker-compose exec postgres psql -U postgres -d learnhub_db -c "SELECT 1"
```

### Porta já em uso
```bash
# Mudar porta no docker-compose.yml ou .env
# Ou matar processo que está usando
sudo lsof -i :3000
```

### Rebuild necessário
```bash
# Reconstruir imagem
docker-compose build --no-cache

# Reiniciar
docker-compose up -d
```

---

## 📈 Performance

### Development
- Hot reload via volume mounts
- Django development server
- Sem otimizações de produção

### Production
- Multi-stage build (imagem mínima)
- Gunicorn com 4 workers
- Static files coletados
- Sem bind mounts (apenas imagem)
- Health checks contínuos

---

## 🔄 CI/CD Integration

### GitHub Actions exemplo
```yaml
name: Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: docker/build-push-action@v2
        with:
          push: true
          tags: seu-usuario/learnhub:latest
          registry: docker.io
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

---

## 📞 Suporte

Para problemas:
1. Verificar logs: `docker-compose logs [serviço]`
2. Verificar health: `docker-compose ps`
3. Testar endpoints: `curl http://localhost:3000/health/`
