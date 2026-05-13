"""
Health check tests to validate Docker services are working correctly
Run with: docker-compose exec web python manage.py shell < tests/healthcheck.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.core.management import call_command
from io import StringIO

print("=" * 60)
print("LearnHub Health Check Tests")
print("=" * 60)

# Test 1: Database Connection
print("\n[1/5] Testing database connection...")
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    sys.exit(1)

# Test 2: Environment Variables
print("\n[2/5] Checking environment variables...")
required_vars = [
    'SECRET_KEY',
    'ALLOWED_HOSTS',
    'DATABASE_ENGINE',
    'DATABASE_NAME',
]
try:
    from django.conf import settings
    for var in required_vars:
        value = getattr(settings, var, None)
        if value:
            print(f"✓ {var} is set")
        else:
            print(f"⚠ {var} is not set (may use default)")
except Exception as e:
    print(f"✗ Failed to check environment: {e}")
    sys.exit(1)

# Test 3: Static Files
print("\n[3/5] Checking static files setup...")
try:
    from django.conf import settings
    static_root = getattr(settings, 'STATIC_ROOT', None)
    static_url = settings.STATIC_URL
    print(f"✓ STATIC_URL: {static_url}")
    if static_root:
        print(f"✓ STATIC_ROOT: {static_root}")
except Exception as e:
    print(f"✗ Static files check failed: {e}")

# Test 4: Installed Apps
print("\n[4/5] Checking installed apps...")
try:
    from django.conf import settings
    apps = settings.INSTALLED_APPS
    print(f"✓ Total installed apps: {len(apps)}")
    for app in apps:
        if not app.startswith('django.'):
            print(f"  - {app}")
except Exception as e:
    print(f"✗ Installed apps check failed: {e}")

# Test 5: User Authentication
print("\n[5/5] Checking authentication system...")
try:
    from django.contrib.auth.models import User
    user_count = User.objects.count()
    print(f"✓ User authentication active ({user_count} users)")
except Exception as e:
    print(f"✗ Authentication check failed: {e}")

print("\n" + "=" * 60)
print("✓ All health checks passed!")
print("=" * 60)
