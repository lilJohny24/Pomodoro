import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pytest_plugins = [
    'tests.fixtures.auth.auth_service',          # tests/fixtures/auth/auth_service.py
    'tests.fixtures.auth.clients',               # tests/fixtures/auth/clients.py  
    'tests.fixtures.users.user_repository',
    'tests.fixtures.settings',
    'tests.fixtures.users.user_model'
]   