# 🚀 LearnHub - Hub de Estudos Real

## 📋 Mudanças Implementadas

Seu projeto foi transformado de uma plataforma simples para um **hub de estudos profissional** como Udemy, com as seguintes funcionalidades:

### ✅ 1. **Persistência de Usuários no Banco de Dados**
- Usuários agora são salvos no PostgreSQL usando Django's `User` model
- Suporta registro, login e logout real
- Dados persistem mesmo após desconexão

### ✅ 2. **Cursos com Múltiplas Aulas**
- Cada curso pode ter **múltiplas aulas/videoaulas**
- Aulas organizadas em ordem sequencial
- Suporte a diferentes durações de aula
- URLs estruturadas: `/curso/{id}/aula/{id}/`

### ✅ 3. **Rastreamento de Progresso**
- Cada usuário tem seu progresso **salvo por aula**
- Porcentagem de conclusão por aula
- Porcentagem total de conclusão do curso
- Tracking de tempo assistido

### ✅ 4. **Modelos de Banco de Dados**

#### **Course** (Cursos)
```python
- titulo
- descricao
- imagem
- categoria (Back-end, Front-end, DevOps, IA & Data)
- nivel (Iniciante, Intermediário, Avançado)
- duracao
- criado_em / atualizado_em
```

#### **Lesson** (Aulas)
```python
- curso (ForeignKey)
- titulo
- descricao
- video_url
- ordem
- duracao_minutos
- criado_em
```

#### **UserEnrollment** (Inscrições)
```python
- usuario (ForeignKey)
- curso (ForeignKey)
- data_inscricao
- Métodos:
  - progresso_total(): % de conclusão do curso
  - aulas_completadas(): número de aulas completas
```

#### **LessonProgress** (Progresso por Aula)
```python
- usuario (ForeignKey)
- aula (ForeignKey)
- tempo_assistido (segundos)
- completada (boolean)
- primeira_visualizacao / ultima_atualizacao
- Métodos:
  - porcentagem_assistida(): % do vídeo assistido
```

---

## 🔧 Como Usar

### **1. Rodar Migrations (IMPORTANTE!)**

```bash
# Dentro do container
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Ou durante build
docker-compose up -d --build
```

### **2. Acessar Admin do Django**

O script de inicialização cria um superuser automático:
- **URL**: `http://localhost:3010/admin/`
- **Usuário**: `admin`
- **Senha**: `admin123`

✨ **Mude a senha em produção!**

### **3. Gerenciar Cursos e Aulas via Admin**

1. Acesse `/admin/`
2. Clique em **Courses** para criar/editar cursos
3. Clique em **Lessons** para adicionar aulas aos cursos
4. Defina a ordem das aulas (campo "ordem")

### **4. Visualizar Progresso**

- **Como Admin**: Veja em `UserEnrollment` e `LessonProgress`
- **Como Usuário**: Veja a porcentagem em "Meus Cursos"

---

## 📁 Estrutura de Arquivos Alterada

```
app/
├── models.py (NEW - Modelos de dados)
├── admin.py (UPDATED - Admin interface)
├── views.py (UPDATED - Lógicas com banco de dados)
├── management/
│   └── commands/
│       └── populate_db.py (NEW - Carrega dados de exemplo)
│
core/
├── urls.py (UPDATED - Novas rotas)
└── settings.py (precisa registrar 'app')

scripts/
└── entrypoint.sh (UPDATED - Cria migrations e superuser)
```

---

## 🎥 Fluxo de Aula

1. **Usuário acessa**: `/curso/{id}/aula/{id}/`
2. **Sistema carrega**: `Lesson` e `LessonProgress`
3. **JavaScript rastreia**: tempo assistido
4. **Envia AJAX**: POST `/api/salvar-progresso/`
5. **Backend salva**: `LessonProgress.tempo_assistido`
6. **Frontend exibe**: porcentagem atualizada

---

## 🔗 Endpoints Principais

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/` | Home com cursos |
| GET | `/curso/{id}/` | Detalhes do curso |
| GET | `/curso/{id}/aula/{id}/` | Reprodutor de aula ✨ |
| POST | `/api/salvar-progresso/` | Salvar progresso (AJAX) ✨ |
| POST | `/curso/{id}/adicionar/` | Inscrever em curso |
| POST | `/curso/{id}/remover/` | Remover inscrição |
| GET | `/meus-cursos/` | Meus cursos e progresso |
| POST | `/login/` | Login |
| POST | `/cadastro/` | Registro |
| GET | `/logout/` | Logout |

✨ = Novas rotas

---

## 📊 Queries de Exemplo

```python
# Obter progresso do usuário em um curso
from app.models import UserEnrollment
enrollment = UserEnrollment.objects.get(usuario=user, curso=course)
progresso = enrollment.progresso_total()  # Ex: 75%

# Obter aulas completadas
aulas_completas = enrollment.aulas_completadas()  # Ex: 3 aulas

# Marcar aula como completa
from app.models import LessonProgress
progress = LessonProgress.objects.get(usuario=user, aula=aula)
progress.completada = True
progress.save()
```

---

## 🛠 Próximas Melhorias (Opcional)

- [ ] Upload de certificados
- [ ] Sistema de comentários em aulas
- [ ] Fórum de discussão
- [ ] Integração com pagamento
- [ ] Sistema de recomendação de cursos
- [ ] Mobile app
- [ ] Live classes

---

## ⚠️ Importante

1. **Migrations**: Execute `python manage.py makemigrations && python manage.py migrate`
2. **Superuser**: Mude a senha do admin em produção!
3. **Static Files**: Collect com `python manage.py collectstatic`
4. **CSRF Token**: Adicione `{% csrf_token %}` em formulários HTML

---

## 🚀 Deploy

```bash
# Build
docker-compose -f docker-compose.prod.yml build

# Start
docker-compose -f docker-compose.prod.yml up -d

# Check
docker-compose -f docker-compose.prod.yml logs -f web
```

---

**Seu LearnHub está pronto para ser um hub de estudos real! 🎓**
