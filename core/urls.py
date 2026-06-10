from django.urls import path
from django.http import HttpResponse
from app import views
from app.healthcheck import HealthCheckView

# Ignore favicon requests
def favicon(request):
    return HttpResponse(status=204)

urlpatterns = [
    path('favicon.ico', favicon),
    path('', views.home, name='home'),
    path('health/', HealthCheckView.as_view(), name='health'),
    path('curso/<int:id>/', views.curso, name='curso'),
    path('curso/<int:id>/adicionar/', views.adicionar_curso, name='adicionar_curso'),
    path('curso/<int:id>/remover/', views.remover_curso, name='remover_curso'),
    path('curso/<int:curso_id>/aula/<int:aula_id>/', views.aula, name='aula'),
    path('api/salvar-progresso/', views.salvar_progresso, name='salvar_progresso'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('meus-cursos/', views.meus_cursos, name='meus_cursos'),
]
