from unicodedata import name
from django.db import models

from api.v1.company.models.models import (
    Company,
)


# Courses Model
class Courses(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name
