# Generated migration for initial database setup

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, unique=True)),
                ('descricao', models.TextField()),
                ('categoria', models.CharField(max_length=100)),
                ('nivel', models.CharField(choices=[('iniciante', 'Iniciante'), ('intermediario', 'Intermediário'), ('avancado', 'Avançado')], default='iniciante', max_length=20)),
                ('duracao', models.CharField(help_text='Ex: 40h', max_length=50)),
                ('imagem', models.URLField(blank=True, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
                'ordering': ['-criado_em'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('youtube', 'YouTube'), ('vimeo', 'Vimeo'), ('local', 'Upload Local'), ('outro', 'Outro')], default='youtube', max_length=20)),
                ('url_video', models.URLField(help_text='URL do vídeo (YouTube, Vimeo, etc)')),
                ('duracao', models.IntegerField(help_text='Duração em minutos')),
                ('ordem', models.IntegerField(default=0, help_text='Ordem de exibição')),
                ('publicado', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='app.curso')),
            ],
            options={
                'verbose_name': 'Vídeo',
                'verbose_name_plural': 'Vídeos',
                'ordering': ['curso', 'ordem', 'criado_em'],
                'unique_together': {('curso', 'titulo')},
            },
        ),
        migrations.CreateModel(
            name='VideoAssistido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_email', models.EmailField(max_length=254)),
                ('data_conclusao', models.DateTimeField(auto_now_add=True)),
                ('tempo_assistido', models.IntegerField(default=0, help_text='Tempo em segundos')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assistidos', to='app.video')),
            ],
            options={
                'verbose_name': 'Vídeo Assistido',
                'verbose_name_plural': 'Vídeos Assistidos',
                'ordering': ['-data_conclusao'],
                'unique_together': {('usuario_email', 'video')},
            },
        ),
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_email', models.EmailField(max_length=254)),
                ('data_inscricao', models.DateTimeField(auto_now_add=True)),
                ('progresso', models.FloatField(default=0.0, help_text='Porcentagem de progresso 0-100')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscricoes', to='app.curso')),
            ],
            options={
                'verbose_name': 'Inscrição',
                'verbose_name_plural': 'Inscrições',
                'ordering': ['-data_inscricao'],
                'unique_together': {('usuario_email', 'curso')},
            },
        ),
    ]
