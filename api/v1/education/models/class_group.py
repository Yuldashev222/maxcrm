import datetime
from django.db import models


from api.v1.accounts.models import (
    Mentor,
    Teacher,
    Student
)
from api.v1.company.models.models import (
    Company
)
from api.v1.education.models.mixins import (
    WeeksMixin
)




# Rooms Model
class Rooms(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True, null=True)
    number_room = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.number_room}"


# Groups Model
class ClassGroups(WeeksMixin, models.Model):
    # teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    room = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    from_time = models.TimeField()
    to_time = models.TimeField()
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.teacher.first_name}"
    
    @property
    def get_room(self):
        pass
    
    @property
    def get_all_mentors_count(self):
        mentors = MentorsInGroup.objects.select_related(
            'class_group', 'mentor',
        ).filter(is_active=True, is_deleted=False, class_group_id=self.pk)
        return mentors.count()
    
    @property
    def get_all_mentors_data(self):
        mentors = MentorsInGroup.objects.select_related(
            'class_group', 'mentor',
        ).filter(is_active=True, is_deleted=False, class_group_id=self.pk)
        return mentors.values('first_name', 'last_name', 'tel_number', 'email', 'father_name', 'gender', 'birthday', 'avatar')
    
    @property
    def get_all_students_count(self):
        students = ClassGroupStudents.objects.select_related(
            'class_group', 'student',
        ).filter(is_active=True, is_deleted=False, class_group_id=self.pk)
        return students.count()
    
    @property
    def get_all_students_data(self):
        students = ClassGroupStudents.objects.select_related(
            'class_group', 'student',
        ).filter(is_active=True, is_deleted=False, class_group_id=self.pk)
        return students.values('first_name', 'last_name', 'tel_number', 'email', 'father_name', 'gender', 'birthday', 'avatar')


# Teachers in group
class TeachersInGroup(models.Model):
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_group.name} - {self.mentor.first_name}"
    
# Montors in group
class MentorsInGroup(models.Model):
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    mentor = models.ForeignKey(Mentor, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.class_group.name} - {self.mentor.first_name}"

# Studens in group
class ClassGroupStudents(models.Model):
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    student = models.OneToOneField(Student, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_group.name} - {self.student.first_name}"






