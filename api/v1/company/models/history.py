from django.db import models

from api.v1.company.models.models import Company
from config.settings import ACTIONS_IN_MODEL
# Create your models here.


class HistoryCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    model_event = models.CharField(max_length=1, choices=ACTIONS_IN_MODEL, default='created')
    
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="uploads/history-companies/", null=True, blank=True)
    balance = models.FloatField(default=0, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    legal_address = models.CharField(max_length=255, null=True, blank=True)
    stir = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    main_target = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    mfo = models.CharField(max_length=100, null=True, blank=True)
    
    last_updated = models.DateTimeField(blank=True, null=True, editable=False)
    created_at = models.DateTimeField(blank=True, null=True, editable=False)
    is_branch = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}: {self.email}"