from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from api.v1.company.models.history import (
    HistoryCompany
)
from api.v1.company.models.models import (
    Company
)


@receiver(post_save, sender=Company)
def create_history_company(sender, instance, created, **kwargs):
    if created:
        HistoryCompany.objects.create(company=instance, email=instance.email)


@receiver(post_save, sender=Company)
def update_history_company(sender, instance, created, **kwargs):
    if not created:
        HistoryCompany.objects.create(company=instance, email=instance.email)
