from django.contrib import admin
from .models import Course, Lesson, UserEnrollment, LessonProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'nivel', 'total_aulas', 'criado_em')
    list_filter = ('categoria', 'nivel', 'criado_em')
    search_fields = ('titulo', 'descricao')
    readonly_fields = ('criado_em', 'atualizado_em')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'imagem')
        }),
        ('Categorização', {
            'fields': ('categoria', 'nivel', 'duracao')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'ordem', 'duracao_minutos', 'criado_em')
    list_filter = ('curso', 'criado_em')
    search_fields = ('titulo', 'curso__titulo')
    readonly_fields = ('criado_em',)
    ordering = ('curso', 'ordem')
    
    fieldsets = (
        ('Aula', {
            'fields': ('curso', 'titulo', 'descricao', 'ordem')
        }),
        ('Conteúdo', {
            'fields': ('video_url', 'duracao_minutos')
        }),
        ('Timestamps', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserEnrollment)
class UserEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'data_inscricao', 'progresso_total')
    list_filter = ('data_inscricao', 'curso', 'usuario')
    search_fields = ('usuario__username', 'curso__titulo')
    readonly_fields = ('data_inscricao', 'progresso_total', 'aulas_completadas')
    
    def progresso_total(self, obj):
        return f"{obj.progresso_total()}%"
    progresso_total.short_description = 'Progresso'
    
    def aulas_completadas(self, obj):
        total = obj.curso.lessons.count()
        completas = obj.aulas_completadas()
        return f"{completas}/{total}"
    aulas_completadas.short_description = 'Aulas Completas'


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'aula', 'porcentagem_assistida', 'completada', 'ultima_atualizacao')
    list_filter = ('completada', 'primeira_visualizacao', 'aula__curso')
    search_fields = ('usuario__username', 'aula__titulo')
    readonly_fields = ('primeira_visualizacao', 'ultima_atualizacao', 'porcentagem_assistida')
    
    def porcentagem_assistida(self, obj):
        return f"{obj.porcentagem_assistida()}%"
    porcentagem_assistida.short_description = 'Assistido'
