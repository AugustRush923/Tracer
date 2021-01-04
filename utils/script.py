import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tracer.settings')

django.setup()


if __name__ == '__main__':
    from users.models import Register

    Register.objects.create(username='abc', password='12345678', email='abc@gmail.com', phone_number='13211112221')
