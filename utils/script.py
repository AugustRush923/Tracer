import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tracer.settings')

django.setup()


if __name__ == '__main__':
    from users.models import PriceStrategy

    PriceStrategy.objects.create(
        title='个人免费版',
        price=0,
        project_num=3,
        project_member=2,
        project_space=50,
        single_file=5,
    )
