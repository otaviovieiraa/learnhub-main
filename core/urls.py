from django.urls import path
from app import views
from app.healthcheck import HealthCheckView

urlpatterns = [
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
