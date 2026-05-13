from django.contrib import admin
from .models import Curso, Video, Inscricao, VideoAssistido


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'nivel', 'total_videos', 'duracao', 'criado_em')
    list_filter = ('categoria', 'nivel', 'criado_em')
    search_fields = ('titulo', 'descricao')
    readonly_fields = ('criado_em', 'atualizado_em')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'imagem')
        }),
        ('Detalhes do Curso', {
            'fields': ('categoria', 'nivel', 'duracao')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'tipo', 'duracao', 'ordem', 'publicado', 'criado_em')
    list_filter = ('curso', 'tipo', 'publicado', 'criado_em')
    search_fields = ('titulo', 'descricao', 'curso__titulo')
    readonly_fields = ('criado_em', 'atualizado_em')
    fieldsets = (
        ('Informações do Vídeo', {
            'fields': ('curso', 'titulo', 'descricao', 'tipo', 'url_video')
        }),
        ('Configurações', {
            'fields': ('duracao', 'ordem', 'publicado')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('usuario_email', 'curso', 'progresso', 'data_inscricao')
    list_filter = ('curso', 'data_inscricao')
    search_fields = ('usuario_email', 'curso__titulo')
    readonly_fields = ('data_inscricao',)


@admin.register(VideoAssistido)
class VideoAssistidoAdmin(admin.ModelAdmin):
    list_display = ('usuario_email', 'video', 'data_conclusao')
    list_filter = ('video__curso', 'data_conclusao')
    search_fields = ('usuario_email', 'video__titulo')
    readonly_fields = ('data_conclusao',)
