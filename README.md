## 📌 Estrutura do Projeto

O projeto segue a arquitetura padrão do Django, organizada da seguinte forma:

```
learnhub/
│
├── app/                     # Aplicação principal
│   ├── views.py            # Lógica das páginas (views)
│   └── __pycache__/        # Arquivos compilados (automático)
│
├── core/                    # Configurações do projeto Django
│   ├── settings.py         # Configurações gerais (apps, banco, etc)
│   ├── urls.py             # Rotas principais do sistema
│   └── __pycache__/
│
├── templates/               # Templates HTML (interface do usuário)
│   ├── base.html           # Template base (layout principal)
│   ├── home.html           # Página inicial
│   ├── login.html          # Tela de login
│   ├── cadastro.html       # Tela de cadastro
│   ├── curso.html          # Página de curso
│   └── meus_cursos.html    # Área do usuário (cursos)
│
├── static/                  # Arquivos estáticos
│   └── style.css           # Estilos da aplicação
│
├── manage.py               # Gerenciador do Django
```

