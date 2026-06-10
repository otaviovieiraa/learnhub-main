from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Course, Lesson, UserEnrollment, LessonProgress


def home(request):
    """Página inicial com lista de cursos"""
    cursos = Course.objects.all()
    user_enrollments = []
    
    if request.user.is_authenticated:
        user_enrollments = UserEnrollment.objects.filter(usuario=request.user).values_list('curso_id', flat=True)
    
    context = {
        'cursos': cursos,
        'user_enrollments': list(user_enrollments)
    }
    return render(request, 'home.html', context)


def curso(request, id):
    """Detalhes do curso com aulas"""
    curso = get_object_or_404(Course, id=id)
    aulas = curso.lessons.all()
    
    is_enrolled = False
    progresso = None
    
    if request.user.is_authenticated:
        enrollment = UserEnrollment.objects.filter(usuario=request.user, curso=curso).first()
        is_enrolled = enrollment is not None
        progresso = enrollment.progresso_total() if enrollment else 0
    
    context = {
        'curso': curso,
        'aulas': aulas,
        'is_enrolled': is_enrolled,
        'progresso': progresso,
        'total_aulas': aulas.count(),
    }
    return render(request, 'curso.html', context)


@login_required(login_url='/login/')
def aula(request, curso_id, aula_id):
    """Página de reprodução de aula com rastreamento de progresso"""
    curso = get_object_or_404(Course, id=curso_id)
    aula = get_object_or_404(Lesson, id=aula_id, curso=curso)
    
    # Verificar se usuário está inscrito no curso
    enrollment = get_object_or_404(UserEnrollment, usuario=request.user, curso=curso)
    
    # Obter ou criar progresso da aula
    progress, created = LessonProgress.objects.get_or_create(
        usuario=request.user,
        aula=aula
    )
    
    # Obter todas as aulas do curso com seu status de conclusão
    aulas_curso = curso.lessons.all()
    aulas_com_progresso = []
    
    for a in aulas_curso:
        prog = LessonProgress.objects.filter(usuario=request.user, aula=a).first()
        aulas_com_progresso.append({
            'id': a.id,
            'titulo': a.titulo,
            'ordem': a.ordem,
            'completada': prog.completada if prog else False,
            'porcentagem': prog.porcentagem_assistida() if prog else 0,
        })
    
    context = {
        'curso': curso,
        'aula': aula,
        'aulas_curso': aulas_com_progresso,
        'aula_atual': aula.id,
        'progresso_aula': progress.porcentagem_assistida(),
        'aula_completa': progress.completada,
        'proxima_aula': aulas_curso.filter(ordem__gt=aula.ordem).first(),
        'aula_anterior': aulas_curso.filter(ordem__lt=aula.ordem).last(),
        'progresso_curso': enrollment.progresso_total(),
    }
    
    return render(request, 'aula.html', context)


@login_required(login_url='/login/')
@require_POST
def salvar_progresso(request):
    """API para salvar progresso da aula (chamada via AJAX)"""
    try:
        data = json.loads(request.body)
        aula_id = data.get('aula_id')
        tempo_assistido = data.get('tempo_assistido', 0)
        completada = data.get('completada', False)
        
        aula = get_object_or_404(Lesson, id=aula_id)
        
        progress, created = LessonProgress.objects.get_or_create(
            usuario=request.user,
            aula=aula
        )
        
        progress.tempo_assistido = max(progress.tempo_assistido, tempo_assistido)
        progress.completada = completada
        progress.save()
        
        return JsonResponse({
            'success': True,
            'progresso': progress.porcentagem_assistida(),
            'completada': progress.completada
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required(login_url='/login/')
def adicionar_curso(request, id):
    """Inscrever usuário em um curso"""
    curso = get_object_or_404(Course, id=id)
    
    enrollment, created = UserEnrollment.objects.get_or_create(
        usuario=request.user,
        curso=curso
    )
    
    if created:
        messages.success(request, f'Você foi inscrito em "{curso.titulo}" com sucesso! 🎉')
    else:
        messages.info(request, f'Você já está inscrito em "{curso.titulo}"')
    
    return redirect(f'/curso/{id}/')


@login_required(login_url='/login/')
def remover_curso(request, id):
    """Remover inscrição do usuário em um curso"""
    curso = get_object_or_404(Course, id=id)
    enrollment = UserEnrollment.objects.filter(usuario=request.user, curso=curso).first()
    
    if enrollment:
        enrollment.delete()
        messages.success(request, f'Você foi removido de "{curso.titulo}"')
    
    return redirect('/meus-cursos/')


@login_required(login_url='/login/')
def meus_cursos(request):
    """Página com cursos inscritos e progresso"""
    enrollments = UserEnrollment.objects.filter(usuario=request.user).select_related('curso')
    
    cursos_com_progresso = []
    for enrollment in enrollments:
        cursos_com_progresso.append({
            'curso': enrollment.curso,
            'progresso': enrollment.progresso_total(),
            'aulas_completadas': enrollment.aulas_completadas(),
            'total_aulas': enrollment.curso.lessons.count(),
        })
    
    context = {
        'cursos': cursos_com_progresso
    }
    return render(request, 'meus_cursos.html', context)


def login_view(request):
    """Página de login"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=senha)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name or user.username}! 👋')
                return redirect('/')
            else:
                messages.error(request, 'Senha incorreta')
        except User.DoesNotExist:
            messages.error(request, 'Email não encontrado')
    
    return render(request, 'login.html')


def cadastro(request):
    """Página de cadastro"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '')
        email = request.POST.get('email', '')
        senha = request.POST.get('senha', '')
        
        if not all([nome, email, senha]):
            messages.error(request, 'Preencha todos os campos')
            return render(request, 'cadastro.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return render(request, 'cadastro.html')
        
        # Usar parte do email como username
        username = email.split('@')[0]
        
        # Garantir username único
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha,
            first_name=nome
        )
        
        login(request, user)
        messages.success(request, f'Bem-vindo, {nome}! 🎓')
        return redirect('/')
    
    return render(request, 'cadastro.html')


def logout_view(request):
    """Logout do usuário"""
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso!')
    return redirect('/')
