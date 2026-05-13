#!/usr/bin/env python
"""
Django WSGI config for Gunicorn production server.
Configured to work with Docker and environment variables.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))

# Load environment variables
load_dotenv()

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Setup Django
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable?"
    ) from exc

# Optionally wrap with middleware for production features
# Example: Add security middleware, monitoring, etc.
if not os.getenv('DEBUG', 'True') == 'True':
    # Production middleware could go here
    pass
