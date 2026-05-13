# Health check endpoint view
from django.http import JsonResponse
from django.views import View


class HealthCheckView(View):
    """Health check endpoint for monitoring and orchestration"""
    
    def get(self, request):
        """Return 200 OK if service is healthy"""
        try:
            from django.db import connection
            
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            
            return JsonResponse({
                'status': 'healthy',
                'database': 'connected'
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'status': 'unhealthy',
                'error': str(e)
            }, status=503)
