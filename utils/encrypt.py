import hashlib
from django.conf import settings


def md5_encrypt(password_string):
    md5 = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    md5.update(password_string.encode('utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    result = md5_encrypt("123456")
    print(result)
