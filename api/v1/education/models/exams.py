from django.db import models


from api.v1.company.models.models import (
    Company,
)
from api.v1.education.models.class_group import (
    ClassGroups,
)


class ExamForStudy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    
    title = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.company.username}: {self.class_group.name}"
    
    
class ExamForStudyItems(models.Model):
    exam_for_study = models.ForeignKey(ExamForStudy, on_delete=models.PROTECT)
    title = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)



class ExamForStudyFiles(models.Model):
    exam_for_study = models.ForeignKey(ExamForStudy, on_delete=models.PROTECT)
    exam_for_study_items = models.ForeignKey(ExamForStudyItems, on_delete=models.PROTECT)

    files = models.FileField(upload_to='exams/for-study/files/')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False) 
    
    