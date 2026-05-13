from django.shortcuts import render, redirect
from django.contrib import messages

# Simulated DB
cursos = [
    {"id":1,"titulo":"Python","descricao":"Do zero ao avançado. Aprenda a linguagem mais versátil do mercado com projetos reais.","imagem":"https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600&q=80","categoria":"Back-end","nivel":"Iniciante","duracao":"40h","aulas":80},
    {"id":2,"titulo":"React","descricao":"Frontend moderno com hooks, context API e integração com APIs REST.","imagem":"https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600&q=80","categoria":"Front-end","nivel":"Intermediário","duracao":"30h","aulas":60},
    {"id":3,"titulo":"Django","descricao":"Backend completo com autenticação, REST API e deploy em produção.","imagem":"https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&q=80","categoria":"Back-end","nivel":"Intermediário","duracao":"35h","aulas":70},
    {"id":4,"titulo":"Machine Learning","descricao":"Algoritmos, scikit-learn, redes neurais e projetos com dados reais.","imagem":"https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=600&q=80","categoria":"IA & Data","nivel":"Avançado","duracao":"50h","aulas":100},
    {"id":5,"titulo":"TypeScript","descricao":"JavaScript com tipagem estática. Código mais robusto e produtivo.","imagem":"https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=600&q=80","categoria":"Front-end","nivel":"Iniciante","duracao":"20h","aulas":40},
    {"id":6,"titulo":"Docker & DevOps","descricao":"Containers, CI/CD, Kubernetes e deploy em cloud.","imagem":"https://images.unsplash.com/photo-1605745341112-85968b19335b?w=600&q=80","categoria":"DevOps","nivel":"Avançado","duracao":"28h","aulas":55},
]

def get_user(request):
    return request.session.get('user')

def home(request):
    user = get_user(request)
    enrolled = request.session.get('enrolled', [])
    return render(request, 'home.html', {"cursos": cursos, "user": user, "enrolled": enrolled})

def curso(request, id):
    user = get_user(request)
    if not user:
        messages.error(request, 'Você precisa estar logado para acessar os cursos.')
        return redirect('/login/')
    c = next((x for x in cursos if x["id"] == id), None)
    enrolled = request.session.get('enrolled', [])
    is_enrolled = id in enrolled
    return render(request, 'curso.html', {"curso": c, "user": user, "is_enrolled": is_enrolled})

def adicionar_curso(request, id):
    if not get_user(request):
        return redirect('/login/')
    enrolled = request.session.get('enrolled', [])
    if id not in enrolled:
        enrolled.append(id)
        request.session['enrolled'] = enrolled
        messages.success(request, 'Curso adicionado com sucesso! 🎉')
    return redirect(f'/curso/{id}/')

def remover_curso(request, id):
    if not get_user(request):
        return redirect('/login/')
    enrolled = request.session.get('enrolled', [])
    if id in enrolled:
        enrolled.remove(id)
        request.session['enrolled'] = enrolled
        messages.success(request, 'Curso removido da sua lista.')
    return redirect('/meus-cursos/')

def login_view(request):
    if get_user(request):
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()
        # Fake auth: qualquer email/senha não vazio
        if email and senha and '@' in email:
            nome = email.split('@')[0].capitalize()
            request.session['user'] = {'nome': nome, 'email': email}
            messages.success(request, f'Bem-vindo de volta, {nome}! 👋')
            return redirect('/')
        else:
            messages.error(request, 'Email ou senha inválidos.')
    return render(request, 'login.html', {})

def cadastro(request):
    if get_user(request):
        return redirect('/')
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()
        if nome and email and senha and '@' in email:
            request.session['user'] = {'nome': nome, 'email': email}
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {nome}! 🚀')
            return redirect('/')
        else:
            messages.error(request, 'Preencha todos os campos corretamente.')
    return render(request, 'cadastro.html', {})

def logout_view(request):
    request.session.flush()
    return redirect('/login/')

def meus_cursos(request):
    user = get_user(request)
    if not user:
        return redirect('/login/')
    enrolled = request.session.get('enrolled', [])
    meus = [c for c in cursos if c["id"] in enrolled]
    return render(request, 'meus_cursos.html', {"cursos": meus, "user": user, "enrolled": enrolled})
