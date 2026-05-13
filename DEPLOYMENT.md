# Production Deployment Guide - LearnHub

## 📋 Pre-deployment Checklist

- [ ] Todos os testes passando localmente
- [ ] `.env` configurado com valores de produção
- [ ] Backup do banco de dados realizado
- [ ] SSL/TLS certificate pronto (ou usar Let's Encrypt)
- [ ] Domain apontado para seu servidor
- [ ] Firewall configurado (apenas 80, 443 expostos)
- [ ] Sistema operacional atualizado
- [ ] Docker e Docker Compose instalados

## 🚀 Step-by-Step Deployment

### 1. Preparar Servidor

```bash
# Login no servidor
ssh user@seu-servidor.com

# Atualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalação
docker --version
docker-compose --version
```

### 2. Clonar Repositório

```bash
# Criar diretório de produção
sudo mkdir -p /app/learnhub
sudo chown $USER:$USER /app/learnhub

# Clonar repositório
cd /app/learnhub
git clone https://seu-repo.git .

# Ou usar git pull se já existe
```

### 3. Configurar Variáveis de Ambiente

```bash
# Copiar exemplo
cp .env.example .env

# Editar com valores de produção
nano .env
```

**Valores importantes a serem alterados em produção:**

```env
# Django
DEBUG=False
SECRET_KEY=<gerar novo com: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com

# Database
DATABASE_PASSWORD=<gerar senha forte: openssl rand -base64 32>

# Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=<gerar senha forte>
DJANGO_SUPERUSER_EMAIL=admin@seu-dominio.com
```

### 4. Build da Imagem

```bash
# Build com tag
docker build -t learnhub:v1.0.0 .
docker tag learnhub:v1.0.0 learnhub:latest

# Verificar imagem
docker images | grep learnhub

# Opcional: Push para registry (Docker Hub, ECR, etc)
docker tag learnhub:latest seu-usuario/learnhub:latest
docker push seu-usuario/learnhub:latest
```

### 5. Iniciar Serviços

```bash
# Iniciar com docker-compose (sem nginx)
docker-compose -f docker-compose.prod.yml up -d

# Ou com nginx (recomendado)
docker-compose -f docker-compose.nginx.yml up -d

# Verificar status
docker-compose -f docker-compose.prod.yml ps
```

### 6. Executar Migrações

```bash
# Primeira vez
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Coletar static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Criar superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 7. Configurar HTTPS com Let's Encrypt

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Gerar certificado (com nginx rodando)
sudo certbot certonly --standalone -d seu-dominio.com -d www.seu-dominio.com

# Certificado será em: /etc/letsencrypt/live/seu-dominio.com/

# Copiar para config docker
sudo cp -r /etc/letsencrypt/live/seu-dominio.com/ ./config/ssl/
sudo chown $USER:$USER ./config/ssl -R

# Desabilitar SSL do em desenvolvimento, editar ./config/nginx.conf
# Descomente as linhas SSL:
# ssl_certificate /etc/nginx/ssl/sua-dominio/fullchain.pem;
# ssl_certificate_key /etc/nginx/ssl/seu-dominio/privkey.pem;
# ssl on;
```

### 8. Renovação de Certificados

```bash
# Criar script de renovação
cat > /app/learnhub/renew-certs.sh << 'EOF'
#!/bin/bash
certbot renew --quiet
cp -r /etc/letsencrypt/live/seu-dominio.com/ ./config/ssl/
docker-compose -f docker-compose.nginx.yml restart nginx
EOF

chmod +x renew-certs.sh

# Adicionar ao crontab (renovar a cada dia)
(crontab -l 2>/dev/null; echo "0 2 * * * /app/learnhub/renew-certs.sh") | crontab -
```

## 🔄 Operações Comuns em Produção

### Visualizar Logs

```bash
# Último 50 linhas
docker-compose -f docker-compose.prod.yml logs -f web --tail 50

# Logs de database
docker-compose -f docker-compose.prod.yml logs -f postgres

# Logs de nginx
docker-compose -f docker-compose.nginx.yml logs -f nginx
```

### Backup do Banco de Dados

```bash
# Backup local
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U postgres learnhub_db > backup-$(date +%Y%m%d-%H%M%S).sql

# Backup comprimido (mais rápido)
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U postgres learnhub_db | gzip > backup-$(date +%Y%m%d).sql.gz

# Restaurar backup
gunzip < backup-20240101.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U postgres learnhub_db
```

### Atualizar Aplicação

```bash
# Puxar últimas mudanças
git pull origin main

# Rebuild imagem
docker build -t learnhub:v1.1.0 .

# Atualizar .env se necessário
nano .env

# Stop containers
docker-compose -f docker-compose.prod.yml down

# Tag nova versão
docker tag learnhub:v1.1.0 learnhub:latest

# Iniciar novamente
docker-compose -f docker-compose.prod.yml up -d

# Aplicar migrações se houver
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Rollback de Versão

```bash
# Se algo deu errado, voltar para versão anterior
docker tag learnhub:v1.0.0 learnhub:latest
docker-compose -f docker-compose.prod.yml up -d

# Restaurar BD de backup se necessário
```

## 🔒 Segurança em Produção

### Firewall

```bash
# UFW (Uncomplicated Firewall)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### SSH Hardening

```bash
# Editar sshd_config
sudo nano /etc/ssh/sshd_config

# Mudanças recomendadas:
# Port 2222                          # Mudar porta padrão
# PermitRootLogin no                 # Desabilitar root
# PasswordAuthentication no          # Usar chaves SSH
# MaxAuthTries 3                     # Limitar tentativas
# MaxSessions 5                      # Limitar sessões

# Aplicar mudanças
sudo systemctl restart ssh
```

### Monitoramento

```bash
# Instalar docker-compose para monitoramento
docker-compose -f docker-compose.prod.yml ps

# Verificar uso de recursos
docker stats

# Health check
curl https://seu-dominio.com/health/
```

## 📊 Monitoramento e Alertas

### Health Check Endpoint

```bash
# Deve retornar 200 OK
curl -I https://seu-dominio.com/health/

# Com debug
curl -v https://seu-dominio.com/health/
```

### Setup de Logs Centralizados (Opcional)

```yaml
# Adicionar ao docker-compose.yml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🆘 Troubleshooting

### Container crasheando

```bash
# Ver logs de erro
docker-compose -f docker-compose.prod.yml logs web

# Executar comando interativo para debug
docker-compose -f docker-compose.prod.yml run --rm web bash

# Verificar variáveis de ambiente
docker-compose -f docker-compose.prod.yml exec web env | grep -i database
```

### Permissões de arquivo

```bash
# Se houver erro de permissão
docker-compose -f docker-compose.prod.yml exec web chmod -R 755 staticfiles

# Recriar diretórios
docker-compose -f docker-compose.prod.yml exec web mkdir -p staticfiles media
```

### Banco de dados cheio

```bash
# Verificar espaço
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d learnhub_db -c "SELECT pg_size_pretty(pg_database_size('learnhub_db'));"

# Fazer vacuum
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d learnhub_db -c "VACUUM FULL;"
```

## 📈 Scaling (Opcional)

Para múltiplos workers/replicas:

```yaml
version: '3.9'
services:
  web:
    # ... configuração normal ...
    deploy:
      replicas: 3
      
  nginx:
    # Balancear entre 3 web containers
    upstream django_app {
        server web:3000;
    }
```

Após atualizar:
```bash
docker-compose -f docker-compose.prod.yml up -d --scale web=3
```

## 📞 Suporte e Observabilidade

- Manter logs por pelo menos 30 dias
- Configurar alertas para errors
- Monitorar uso de CPU/Memória
- Manter atualizações de segurança
- Testar backups regularmente
