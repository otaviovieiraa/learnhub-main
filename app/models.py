from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """Modelo de Cursos"""
    CATEGORY_CHOICES = [
        ('Back-end', 'Back-end'),
        ('Front-end', 'Front-end'),
        ('DevOps', 'DevOps'),
        ('IA & Data', 'IA & Data'),
        ('Mobile', 'Mobile'),
    ]
    
    LEVEL_CHOICES = [
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    ]
    
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.URLField()
    categoria = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    nivel = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    duracao = models.CharField(max_length=50)  # ex: "40h"
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-criado_em']
        verbose_name_plural = 'Cursos'
    
    def __str__(self):
        return self.titulo
    
    def total_aulas(self):
        """Retorna total de aulas do curso"""
        return self.lessons.count()
    
    def total_duracao_minutos(self):
        """Retorna duração total em minutos"""
        total = self.lessons.aggregate(models.Sum('duracao_minutos'))['duracao_minutos__sum'] or 0
        return total


class Lesson(models.Model):
    """Modelo de Aulas dentro de um Curso"""
    curso = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    video_url = models.URLField()  # URL do vídeo (YouTube, Vimeo, etc)
    ordem = models.PositiveIntegerField(default=1)
    duracao_minutos = models.PositiveIntegerField(default=10)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['ordem']
        unique_together = ('curso', 'ordem')
        verbose_name_plural = 'Aulas'
    
    def __str__(self):
        return f"{self.curso.titulo} - Aula {self.ordem}: {self.titulo}"


class UserEnrollment(models.Model):
    """Modelo de Inscrição - Rastreia qual usuário está inscrito em qual curso"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscricoes')
    curso = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='inscritos')
    data_inscricao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'curso')
        verbose_name_plural = 'Inscrições'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo}"
    
    def progresso_total(self):
        """Calcula porcentagem de progresso geral no curso"""
        total_aulas = self.curso.lessons.count()
        if total_aulas == 0:
            return 0
        
        aulas_completas = LessonProgress.objects.filter(
            usuario=self.usuario,
            aula__curso=self.curso,
            completada=True
        ).count()
        
        return int((aulas_completas / total_aulas) * 100)
    
    def aulas_completadas(self):
        """Retorna número de aulas completadas"""
        return LessonProgress.objects.filter(
            usuario=self.usuario,
            aula__curso=self.curso,
            completada=True
        ).count()


class LessonProgress(models.Model):
    """Modelo de Progresso - Rastreia o progresso do usuário em cada aula"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresso_aulas')
    aula = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progresso')
    tempo_assistido = models.PositiveIntegerField(default=0)  # em segundos
    completada = models.BooleanField(default=False)
    primeira_visualizacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('usuario', 'aula')
        verbose_name_plural = 'Progresso de Aulas'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.aula.titulo} ({'Completa' if self.completada else 'Em progresso'})"
    
    def porcentagem_assistida(self):
        """Calcula porcentagem do vídeo assistido"""
        duracao_total = self.aula.duracao_minutos * 60  # converter para segundos
        if duracao_total == 0:
            return 0
        return int((self.tempo_assistido / duracao_total) * 100)
