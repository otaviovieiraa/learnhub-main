# Docker Security Guidelines for LearnHub

## 🔐 Implementações de Segurança

### 1. Sem Credenciais Hardcoded

✅ **Implementado**
- Todas as variáveis sensíveis estão em `.env`
- `.env` não está no git (adicione ao `.gitignore`)
- Apenas `.env.example` está versionado

```bash
# Verificar que .env não será commitado
grep ".env" .gitignore
```

### 2. Container Não Roda como Root

✅ **Implementado**
- Usuário `appuser` criado com UID 1000
- Permissões corrigidas nos arquivos
- `USER appuser` no Dockerfile

```dockerfile
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser
USER appuser
```

### 3. Imagem Alpine Otimizada

✅ **Implementado**
- `python:3.11-alpine` (50MB vs 900MB padrão)
- Multi-stage build: dependências de build separadas
- Apenas dependências de runtime na imagem final

**Tamanho comparativo:**
- Alpine Final: ~150MB
- Standard Final: ~1GB
- **Economia: 87%**

### 4. Healthchecks

✅ **Implementado**
- Django: endpoint `/health/` com verificação de BD
- PostgreSQL: `pg_isready` check
- Nginx: verificação do endpoint health

### 5. Network Isolation

✅ **Implementado**
- Bridge network `learnhub_network`
- Containers não expostos desnecessariamente
- Apenas porta 3000 (web) e 80/443 (nginx) expostas

### 6. Non-root em Produção

✅ **Implementado**
```yaml
security_opt:
  - no-new-privileges:true
```

---

## 📋 Checklist Pré-Deploy Produção

### Environment Variables
- [ ] `SECRET_KEY`: Gerar com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- [ ] `DATABASE_PASSWORD`: Senha forte (32+ caracteres)
- [ ] `ALLOWED_HOSTS`: Seus domínios reais
- [ ] `DEBUG`: Verificar que é `False`
- [ ] `DJANGO_SUPERUSER_PASSWORD`: Senha segura

### Configuração Django
- [ ] `SECURE_SSL_REDIRECT=True` em produção
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `SESSION_COOKIE_HTTPONLY=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_HTTPONLY=True`

### Banco de Dados
- [ ] Backup antes do deploy
- [ ] Credenciais PostgreSQL alteradas
- [ ] Migrations testadas em staging

### Docker
- [ ] Imagem testada em staging
- [ ] Registryseguro (Docker Hub, ECR, etc)
- [ ] Tags versionadas (semver: v1.0.0)
- [ ] `.dockerignore` completo

### Segurança
- [ ] HTTPS/TLS configurado (Nginx + Certbot)
- [ ] Headers de segurança adicionados
- [ ] Rate limiting configurado
- [ ] Logs centralizados

---

## 🛡️ Secrets Management

### Desenvolvimento
Arquivo `.env` local (não versionado)

### Staging/Produção

#### Docker Swarm
```bash
echo "your_secret_value" | docker secret create db_password -
```

#### Kubernetes
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: learnhub-secrets
type: Opaque
data:
  db-password: base64encoded_value
```

#### AWS Secrets Manager
```bash
aws secretsmanager create-secret \
  --name learnhub/db-password \
  --secret-string "your_password"
```

#### HashiCorp Vault
```bash
vault kv put secret/learnhub/db password="your_password"
```

---

## 🔍 Scanning de Segurança

### Container Image Scanning
```bash
# Trivy - escanear vulnerabilidades
trivy image learnhub:latest

# Docker Scout
docker scout cves learnhub:latest
```

### Dependency Scanning
```bash
# Safety - verificar dependências Python
pip install safety
safety check

# Verificar requirements.txt
pip-audit
```

### SAST (Static Analysis)
```bash
# Bandit - segurança Python
bandit -r app/

# SonarQube
docker run --rm -v $(pwd):/src sonarsource/sonar-scanner-cli
```

---

## 📊 Monitoramento de Segurança

### Logs Centralizados
```yaml
# Stack ELK (Elasticsearch, Logstash, Kibana)
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  
  logstash:
    image: docker.elastic.co/logstash/logstash:8.0.0
    
  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
```

### Alertas de Segurança
- Falhas de autenticação
- Erros críticos da aplicação
- Acesso a endpoints sensíveis
- Alterações de configuração

---

## 🔄 Atualizações e Patches

### Imagens Base
```bash
# Verificar updates Alpine
docker pull python:3.11-alpine

# Rebuild se houver patches de segurança
docker build --no-cache -t learnhub:latest .
```

### Dependências Python
```bash
# Verificar updates em requirements
pip list --outdated

# Atualizar requirements.txt regularmente
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

---

## 🚨 Incidente de Segurança

Se houver vazamento de secrets:

1. **Imediatamente:**
   - Revoke tokens/passwords
   - Remover repository access
   - Notificar usuários

2. **Rotação de Secrets:**
   ```bash
   # Gerar nova SECRET_KEY
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Audit Trail:**
   - Verificar logs de quem teve acesso
   - Quando foram exposto os secrets
   - Qual dano foi causado

4. **Preventivo:**
   - Implementar secret scanning (git-secrets, detect-secrets)
   - Audit automático de repositórios
   - Educação do time

---

## 📚 Referências

- [OWASP Docker Security Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [CIS Docker Benchmark](https://www.cisecurity.org/cis-benchmarks/)
- [Django Security Documentation](https://docs.djangoproject.com/en/4.2/topics/security/)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

