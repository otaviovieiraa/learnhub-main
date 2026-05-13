from django.db import models
from django.utils import timezone


class Curso(models.Model):
    NIVEL_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    
    titulo = models.CharField(max_length=200, unique=True)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='iniciante')
    duracao = models.CharField(max_length=50, help_text="Ex: 40h")
    imagem = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
    
    def __str__(self):
        return self.titulo
    
    @property
    def total_duracao_videos(self):
        """Calcula duração total em minutos"""
        return sum(v.duracao for v in self.videos.all())
    
    @property
    def total_videos(self):
        """Total de vídeos no curso"""
        return self.videos.count()


class Video(models.Model):
    TIPO_CHOICES = [
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('local', 'Upload Local'),
        ('outro', 'Outro'),
    ]
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='videos')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='youtube')
    url_video = models.URLField(help_text="URL do vídeo (YouTube, Vimeo, etc)")
    duracao = models.IntegerField(help_text="Duração em minutos")
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição")
    publicado = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['curso', 'ordem', 'criado_em']
        verbose_name = 'Vídeo'
        verbose_name_plural = 'Vídeos'
        unique_together = ('curso', 'titulo')
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"


class Inscricao(models.Model):
    usuario_email = models.EmailField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField(auto_now_add=True)
    progresso = models.FloatField(default=0.0, help_text="Porcentagem de progresso 0-100")
    
    class Meta:
        ordering = ['-data_inscricao']
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = ('usuario_email', 'curso')
    
    def __str__(self):
        return f"{self.usuario_email} - {self.curso.titulo}"


class VideoAssistido(models.Model):
    usuario_email = models.EmailField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='assistidos')
    data_conclusao = models.DateTimeField(auto_now_add=True)
    tempo_assistido = models.IntegerField(default=0, help_text="Tempo em segundos")
    
    class Meta:
        ordering = ['-data_conclusao']
        verbose_name = 'Vídeo Assistido'
        verbose_name_plural = 'Vídeos Assistidos'
        unique_together = ('usuario_email', 'video')
    
    def __str__(self):
        return f"{self.usuario_email} - {self.video.titulo}"
