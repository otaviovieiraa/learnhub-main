from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Course, Lesson

class Command(BaseCommand):
    help = 'Popula o banco de dados com cursos e aulas de exemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando população do banco de dados...'))
        
        # Criar cursos
        courses_data = [
            {
                'titulo': 'Python',
                'descricao': 'Do zero ao avançado. Aprenda a linguagem mais versátil do mercado com projetos reais.',
                'imagem': 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600&q=80',
                'categoria': 'Back-end',
                'nivel': 'Iniciante',
                'duracao': '40h',
                'aulas_data': [
                    {'titulo': 'Introdução ao Python', 'duracao_minutos': 25, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Variáveis e Tipos', 'duracao_minutos': 30, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Estruturas de Controle', 'duracao_minutos': 35, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Funções', 'duracao_minutos': 40, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Programação Orientada a Objetos', 'duracao_minutos': 50, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                ]
            },
            {
                'titulo': 'React',
                'descricao': 'Frontend moderno com hooks, context API e integração com APIs REST.',
                'imagem': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600&q=80',
                'categoria': 'Front-end',
                'nivel': 'Intermediário',
                'duracao': '30h',
                'aulas_data': [
                    {'titulo': 'Introdução a React', 'duracao_minutos': 20, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'JSX e Componentes', 'duracao_minutos': 30, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Hooks - useState', 'duracao_minutos': 35, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Hooks - useEffect', 'duracao_minutos': 30, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Context API', 'duracao_minutos': 40, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                ]
            },
            {
                'titulo': 'Django',
                'descricao': 'Backend completo com autenticação, REST API e deploy em produção.',
                'imagem': 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&q=80',
                'categoria': 'Back-end',
                'nivel': 'Intermediário',
                'duracao': '35h',
                'aulas_data': [
                    {'titulo': 'Setup Inicial', 'duracao_minutos': 15, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Modelos (Models)', 'duracao_minutos': 40, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Views e Templates', 'duracao_minutos': 45, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Autenticação', 'duracao_minutos': 35, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'REST API', 'duracao_minutos': 50, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                ]
            },
            {
                'titulo': 'Machine Learning',
                'descricao': 'Algoritmos, scikit-learn, redes neurais e projetos com dados reais.',
                'imagem': 'https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=600&q=80',
                'categoria': 'IA & Data',
                'nivel': 'Avançado',
                'duracao': '50h',
                'aulas_data': [
                    {'titulo': 'Introdução a ML', 'duracao_minutos': 30, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Regressão Linear', 'duracao_minutos': 45, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Classificação', 'duracao_minutos': 50, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Clustering', 'duracao_minutos': 40, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Redes Neurais', 'duracao_minutos': 60, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                ]
            },
            {
                'titulo': 'TypeScript',
                'descricao': 'JavaScript com tipagem estática. Código mais robusto e produtivo.',
                'imagem': 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=600&q=80',
                'categoria': 'Front-end',
                'nivel': 'Iniciante',
                'duracao': '20h',
                'aulas_data': [
                    {'titulo': 'Introdução a TypeScript', 'duracao_minutos': 20, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Tipos Básicos', 'duracao_minutos': 25, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Interfaces', 'duracao_minutos': 30, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Generics', 'duracao_minutos': 35, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                ]
            },
            {
                'titulo': 'Docker & DevOps',
                'descricao': 'Containers, CI/CD, Kubernetes e deploy em cloud.',
                'imagem': 'https://images.unsplash.com/photo-1605745341112-85968b19335b?w=600&q=80',
                'categoria': 'DevOps',
                'nivel': 'Avançado',
                'duracao': '28h',
                'aulas_data': [
                    {'titulo': 'Docker Basics', 'duracao_minutos': 35, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Docker Compose', 'duracao_minutos': 40, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'Kubernetes', 'duracao_minutos': 50, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                    {'titulo': 'CI/CD', 'duracao_minutos': 45, 'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'},
                ]
            }
        ]
        
        for course_data in courses_data:
            aulas_data = course_data.pop('aulas_data')
            course, created = Course.objects.get_or_create(titulo=course_data['titulo'], defaults=course_data)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Curso criado: {course.titulo}'))
                
                # Criar aulas
                for idx, aula_data in enumerate(aulas_data, 1):
                    aula_data['ordem'] = idx
                    aula_data['curso'] = course
                    Lesson.objects.get_or_create(
                        curso=course,
                        ordem=idx,
                        defaults=aula_data
                    )
                self.stdout.write(self.style.SUCCESS(f'  ✓ {len(aulas_data)} aulas adicionadas'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Curso já existe: {course.titulo}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ População do banco concluída com sucesso!'))
