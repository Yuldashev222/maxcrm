from unicodedata import name
from django.db import models

from api.v1.accounts.models import (
    Mentor,
    Teacher,
    Student
)
from api.v1.company.models.models import (
    Company
)
from api.v1.education.models.courses import (
    Courses
)
from api.v1.education.models.lessons import (
    Attendance,
    AttendanceStudent,
    Lesson,
    LessonTask,
    TaskItems
)
from api.v1.education.models.mixins import (
    WeeksMixin
)
from api.v1.education.models.class_group import (
    ClassGroupStudents,
    ClassGroups,
    MentorsInGroup,
    Rooms,
    TeachersInGroup
)


# Courses Model
class CoursesHistory(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name


# Rooms Model
class RoomsHistory(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True, null=True)
    number_room = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.number_room}"


# Groups Model
class ClassGroupsHistory(WeeksMixin, models.Model):
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
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
class TeachersInGroupHistory(models.Model):
    teachers_in_group = models.ForeignKey(TeachersInGroup, on_delete=models.PROTECT)
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
class MentorsInGroupHistory(models.Model):
    mentors_in_group = models.ForeignKey(MentorsInGroup, on_delete=models.PROTECT)
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
class ClassGroupStudentsHistory(models.Model):
    students_in_group = models.ForeignKey(ClassGroupStudents, on_delete=models.PROTECT)
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    student = models.OneToOneField(Student, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_group.name} - {self.student.first_name}"
    
    


class LessonHistory(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
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
class AttendanceHistory(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.PROTECT)
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
    

class AttendanceStudentHistory(models.Model):
    attendance_students = models.ForeignKey(AttendanceStudent, on_delete=models.PROTECT)
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


class LessonTaskHistory(models.Model):
    lesson_task = models.ForeignKey(LessonTask, on_delete=models.PROTECT)
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

class TaskItemsHistory(models.Model):
    task_items = models.ForeignKey(TaskItems, on_delete=models.PROTECT)
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
    
    
    
