from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import password_validation
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import datetime

from rest_framework import serializers

from config.settings import DAYS
from .managers import *
from .enums import Gender, ProfileRoles, Regions, Sections
from .services import upload_location_avatar, validate_birthday, validate_size_image
from api.v1.company.models.models import Company

from multiselectfield import MultiSelectField
from phonenumber_field import modelfields, widgets
from simple_history.models import HistoricalRecords


class SocialLink(models.Model):
    name = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='social_links')

    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    first_name = models.CharField(verbose_name='Name', max_length=50)
    last_name = models.CharField(verbose_name='Surname', max_length=50)
    phone_number = modelfields.PhoneNumberField()
    password = models.CharField(max_length=128)

    role = models.CharField(max_length=20, choices=ProfileRoles.choices())

    section = models.CharField(max_length=12, choices=Sections.choices())
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='workers_and_students')

    creator = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='create_accounts')

    email = models.EmailField(max_length=50, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    last_login = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_start = models.DateField(help_text='date of starting work or study', blank=True, null=True)
    date_finished = models.DateField(help_text='date of completion of work or studies', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_remote = models.BooleanField(default=False)

    historical_records = HistoricalRecords()

    username = models.CharField(unique=True, max_length=23)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['company_id', 'phone_number', 'first_name', 'last_name', 'role']

    objects = MyAccountManager()

    gender = models.CharField(max_length=5, choices=Gender.choices(), default=Gender.man.value)
    birthday = models.DateField(blank=True, null=True, validators=[validate_birthday])
    description = models.TextField(max_length=1000, blank=True, null=True)

    passport_serial_num = models.CharField(
        max_length=9,
        help_text='Enter passport series and number. Ps: 9 digits!',
        blank=True,
        null=True)

    j_sh_sh_ir_num = models.CharField(
        max_length=14,
        help_text='Enter jshshir number. Ps: 14 digits!',
        blank=True,
        null=True)

    avatar = models.ImageField(
        upload_to=upload_location_avatar,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'svg']), validate_size_image],
        blank=True,
        null=True,
    )

    # birth address
    region_1 = models.CharField(max_length=15, choices=Regions.choices(), help_text='province of birth')
    city_1 = models.CharField(max_length=100, blank=True, null=True, help_text='hometown')
    street_1 = models.CharField(max_length=100, blank=True, null=True, help_text='birth street')

    # constant address
    region_2 = models.CharField(max_length=15, choices=Regions.choices(), blank=True, null=True,
                                help_text='your current state of residence')
    city_2 = models.CharField(max_length=100, blank=True, null=True, help_text='your current city of residence')
    street_2 = models.CharField(max_length=100, blank=True, null=True, help_text='your current residential address')

    second_phone_number = modelfields.PhoneNumberField(blank=True, help_text='second phone number')

    # where did you find out about us?
    about_us = models.CharField(max_length=300, blank=True, null=True, help_text='How did you hear about us?')

    # connections
    days = MultiSelectField(choices=DAYS, max_length=20, blank=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        if self.father_name:
            return self.first_name + '-' + self.last_name + '-' + self.father_name
        return self.first_name + '-' + self.last_name

    def activity_by_date(self):

        today_date = datetime.today().date()
        if self.date_start >= today_date and self.date_finished > today_date:
            return True
        return False

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):

        self.username = f'{self.company_id}|{self.phone_number}'

        super().save(*args, **kwargs)

        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None


class Director(User):
    objects = DirectorsManager()

    class Meta:
        proxy = True


class Teacher(User):
    objects = TeachersManager()

    class Meta:
        proxy = True


class Mentor(User):
    objects = MentorsManager()

    class Meta:
        proxy = True


class Student(User):
    objects = StudentsManager()

    class Meta:
        proxy = True


class Parent(User):
    objects = ParentsManager()

    class Meta:
        proxy = True


class Manager(User):
    objects = ManagersManager()

    class Meta:
        proxy = True


class HrManager(User):
    objects = HrManagersManager()

    class Meta:
        proxy = True


class Administrator(User):
    objects = AdministratorsManager()

    class Meta:
        proxy = True


class Marketer(User):
    objects = MarketersManager()

    class Meta:
        proxy = True


class Accountant(User):
    objects = AccountantsManager()

    class Meta:
        proxy = True


class Cashier(User):
    objects = CashiersManager()

    class Meta:
        proxy = True


class Developer(User):
    objects = CashiersManager()

    class Meta:
        proxy = True
