import os
from business.models import init_models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YelpViz.settings")

print "Initializing models"
init_models()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
