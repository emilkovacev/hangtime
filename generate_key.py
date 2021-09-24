from django.core.management.utils import get_random_secret_key  

with open('hangtime/.env', 'r+') as f:
    f.write(f'SECRET_KEY={get_random_secret_key()}')

