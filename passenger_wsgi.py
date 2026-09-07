import os
import sys

# Define o caminho do seu projeto (mude 'meu_projeto_django' para o nome da sua pasta)
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'projeto_sabiaviagens'))

# Aponta para o arquivo wsgi do seu app Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'projeto_sabiaviagens.projeto_sabiaviagens.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
 
