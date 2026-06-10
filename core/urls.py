from django.urls import path
from django.http import HttpResponse
from app import views
from app.healthcheck import HealthCheckView

# Ignore favicon requests
def favicon(request):
    return HttpResponse(status=204)

urlpatterns = [
    path('favicon.ico', favicon),
    path('', views.home),
    path('health/', HealthCheckView.as_view()),
    path('curso/<int:id>/', views.curso),
    path('curso/<int:id>/adicionar/', views.adicionar_curso),
    path('curso/<int:id>/remover/', views.remover_curso),
    path('login/', views.login_view),
    path('cadastro/', views.cadastro),
    path('logout/', views.logout_view),
    path('meus-cursos/', views.meus_cursos),
]
