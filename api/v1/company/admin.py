from django.contrib import admin

from api.v1.company.models.models import (
    Company,
)
from api.v1.company.models.history import (
    HistoryCompany
)
# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'email')
    

@admin.register(HistoryCompany)
class HistoryCompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'email')
