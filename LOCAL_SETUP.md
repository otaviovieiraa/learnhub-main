# 🚀 Setup Local - LearnHub

## 1️⃣ Configurar Ambiente Python

### No Windows (PowerShell):
```powershell
# Criar virtual environment
python -m venv venv

# Ativar
.\venv\Scripts\Activate.ps1

# Se der erro de execução, rodar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### No Mac/Linux (Bash):
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

Se faltar algo:
```bash
pip install Django==4.2.8 psycopg2-binary==2.9.9 python-dotenv==1.0.0 whitenoise==6.6.0
```

---

## 3️⃣ Configurar Banco de Dados Local

### **Opção A: SQLite (Mais Fácil - Dev)**

Crie `.env` na raiz:
```env
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-prod
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

### **Opção B: PostgreSQL Local (Recomendado - Teste Real)**

Instale PostgreSQL:
- **Windows**: https://www.postgresql.org/download/windows/
- **Mac**: `brew install postgresql@15`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

Crie `.env`:
```env
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-prod
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=learnhub_db
DATABASE_USER=postgres
DATABASE_PASSWORD=sua_senha_postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Crie database (no psql):
```sql
CREATE DATABASE learnhub_db;
```

---

## 4️⃣ Rodar Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

Você verá:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

## 5️⃣ Carregar Dados de Exemplo

```bash
python manage.py populate_db
```

Output:
```
✓ Curso criado: Python
  ✓ 5 aulas adicionadas
✓ Curso criado: React
  ✓ 5 aulas adicionadas
...
✓ População do banco concluída com sucesso!
```

---

## 6️⃣ Criar Superuser

```bash
python manage.py createsuperuser
```

Ou automático:
```bash
python manage.py shell << EOF
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@local.com', 'admin123')
EOF
```

---

## 7️⃣ Rodar Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Você verá:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 8️⃣ Acessar Aplicação

| URL | Descrição |
|-----|-----------|
| `http://localhost:8000/` | Home |
| `http://localhost:8000/admin/` | Admin (user: admin, pass: admin123) |
| `http://localhost:8000/cadastro/` | Registrar |
| `http://localhost:8000/login/` | Login |

---

## 🔧 Comandos Úteis

```bash
# Ver todos os comandos disponíveis
python manage.py help

# Resetar banco (CUIDADO - apaga tudo!)
python manage.py migrate learnhub zero
python manage.py migrate

# Acessar shell Python do Django
python manage.py shell

# Limpar banco e recarregar dados
python manage.py flush --no-input
python manage.py migrate
python manage.py populate_db

# Colecionar estáticos
python manage.py collectstatic --noinput

# Rodar testes (quando criados)
python manage.py test

# Ver informações do banco
python manage.py dbshell
```

---

## 📊 Exemplo de Teste Completo

```bash
# 1. Ativar venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate    # Mac/Linux

# 2. Instalar
pip install -r requirements.txt

# 3. Preparar banco
python manage.py migrate
python manage.py populate_db
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@local.com', 'admin123')"

# 4. Rodar servidor
python manage.py runserver

# 5. No navegador:
# - http://localhost:8000/admin/ (user: admin, pass: admin123)
# - http://localhost:8000/cadastro/ (registrar conta)
# - http://localhost:8000/ (homepage)
```

---

## ❌ Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
```bash
pip install -r requirements.txt
```

### "could not connect to server"
Banco de dados não está rodando. Inicie PostgreSQL:
- **Windows**: Services > postgresql
- **Mac**: `brew services start postgresql@15`
- **Linux**: `sudo service postgresql start`

### "permission denied" (venv)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Porta 8000 em uso
```bash
python manage.py runserver 8001
```

---

## ✅ Checklist Completo

- [ ] Python 3.9+
- [ ] venv ativado
- [ ] requirements.txt instalado
- [ ] .env criado com DB_ENGINE sqlite3 ou postgresql
- [ ] migrations rodadas
- [ ] populate_db rodado
- [ ] superuser criado
- [ ] servidor rodando sem erros

**Pronto para testar!** 🚀
