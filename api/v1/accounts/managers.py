from django.contrib.auth.models import BaseUserManager
from django.db.models import manager
from .enums import *

class MyAccountManager(BaseUserManager):
    
    def create_user(self, username, phone_number, company_id, first_name, last_name, role, password=None):
        if not company_id:
            raise ValueError('Users must have an company_id id!!!')
        if not username:
            raise ValueError('Users must have an username!!!')
        if not phone_number:
            raise ValueError('Users must have an tel number!!!')
        if not first_name:
            raise ValueError('Users must have an name!!!')
        if not last_name:
            raise ValueError('Users must have an surname!!!')
        if not role:
            raise ValueError('Users must have an role!!!')
        
        user = self.model(
            username=username,
            phone_number=phone_number,
            company_id=company_id,
            first_name=first_name,
            role=role,
            last_name=last_name
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    
    def create_superuser(self, username, phone_number, company_id, first_name, last_name, role, password):
        user = self.create_user(
            username=username,
            phone_number=phone_number,
            company_id=company_id,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user



class DirectorsManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.director.value)



class TeachersManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.teacher.value)



class MentorsManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.mentor.value)



class StudentsManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.student.value)



class ParentsManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.parent.value)



class ManagersManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.manager.value)



class HrManagersManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.hr_manager.value)



class AdministratorsManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.administrator.value)



class MarketersManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.marketer.value)



class AccountantsManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.accountant.value)



class CashiersManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.cashier.value)



class DevelopersManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoles.developer.value)