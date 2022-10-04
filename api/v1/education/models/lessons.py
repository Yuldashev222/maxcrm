import datetime
from django.db import models



from api.v1.accounts.models import (
    Mentor,
    Teacher,
    Student
)
from api.v1.education.models.class_group import (
    ClassGroups
)


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    theme = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_group.name}: {self.theme}"
    
    

# Attendance in every lesson group
class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    current_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_group.name}"
    
    @property
    def get_group_students_today(self):
        todays_student = AttendanceStudent.objects.select_related(
            'attendance', 'student',
        ).filter(is_active=True, is_deleted=False, attendance_id=self.pk, came=True, date=datetime.datetime.today())
        data = {
            'count':todays_student.count(),
            'students':todays_student.values('student__first_name', 'student__last_name')
        }
        return data
    
    @property
    def get_group_students_not_come_today(self):
        not_come_today_student = AttendanceStudent.objects.select_related(
            'attendance', 'student',
        ).filter(is_active=True, is_deleted=False, attendance_id=self.pk, came=False, date=datetime.datetime.today())
        data = {
            'count':not_come_today_student.count(),
            'students':not_come_today_student.values('student__first_name', 'student__last_name')
        }
        return data
    

class AttendanceStudent(models.Model):
    attendance = models.OneToOneField(Attendance, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    came = models.BooleanField(default=False)
    reason = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attendance.class_group.name} - {self.student.first_name}: {self.came}"


class LessonTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    expire_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lesson.theme} - {self.is_active}"

class TaskItems(models.Model):
    lesson_task = models.ForeignKey(LessonTask, on_delete=models.PROTECT)
    task_text = models.TextField()
    expire_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lesson_task.description} - {self.is_active}"