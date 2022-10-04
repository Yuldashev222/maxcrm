from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True,
                                help_text='Company name must be unique.',
    )
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="uploads/companies/", null=True, blank=True)
    balance = models.FloatField(default=0)
    email = models.EmailField(null=True, blank=True)
    legal_address = models.CharField(max_length=255, null=True, blank=True)
    stir = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    main_target = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    mfo = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_branch = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    
    in_branch = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)
        

    def __str__(self):
        if self.email:
            return f"{self.name}: {self.email}"
        return f"{self.name}"
