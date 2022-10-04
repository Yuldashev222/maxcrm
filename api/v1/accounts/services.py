from django.core.exceptions import ValidationError
from datetime import datetime

from api.v1.company.models.models import Company
from . import models

from rest_framework import response, status


def upload_location_avatar(instance, file):
    """
    Faylga joylashgan address | format: (media)/company/avatars/section/role/first_name-last_name-father_name/
    """
    return f'{instance.company}/avatars/{instance.section}/{instance.role}/{instance}/{file}'


def validate_size_image(file_in_obj):
    """
    Rasm hajmini tekshirish
    """

    size_limit = 2
    if file_in_obj.size > size_limit * 1024 * 1024:
        raise ValidationError(f'maximum file size: {size_limit}mb')


def validate_birthday(date):
    """
    Tugilgan sanasini tekshirish
    """

    today = datetime.now().date()
    if date >= today:
        raise ValidationError('Invalid date entered')
    

def username_not_in_database(company_id, phone_number):
    """
    username bazada takrorlanmasligini tekshirish
    """
    username = str(company_id) + '|' + str(phone_number)
    
    try:
        
        user = models.User.objects.get(username=username)
        return False
        
    except:
        
        return True