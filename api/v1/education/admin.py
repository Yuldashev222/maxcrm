from django.contrib import admin


from api.v1.education.models.courses import (
    Courses,
)
from api.v1.education.models.class_group import (
    Rooms,
    ClassGroups
)
from api.v1.education.models.history import (
    AttendanceHistory,
    AttendanceStudentHistory,
    ClassGroupStudentsHistory,
    ClassGroupsHistory,
    CoursesHistory,
    LessonHistory,
    LessonTaskHistory,
    MentorsInGroupHistory,
    RoomsHistory,
    TaskItemsHistory,
    TeachersInGroupHistory
)
from api.v1.education.models.lessons import (
    Lesson,
    Attendance,
    AttendanceStudent,
    LessonTask,
    TaskItems
)

from api.v1.education.models.exams import (
    ExamForStudy,
    ExamForStudyItems,
    ExamForStudyFiles
)

# Register your models here.



@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'is_active', 'is_deleted')


@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number_room', 'is_active', 'is_deleted')
    
@admin.register(ClassGroups)
class ClassGroupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'from_time', 'to_time', 'is_active', 'is_deleted')
    

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_group', 'teacher', 'theme', 'created_at', 'is_active', 'is_deleted')
    
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'current_date', 'created_at', 'is_active', 'is_deleted')
    
    
@admin.register(AttendanceStudent)
class AttendanceStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'attendance', 'student', 'came', 'created_at', 'is_active', 'is_deleted')
    
@admin.register(LessonTask)
class LessonTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'teacher', 'description', 'expire_date', 'created_at', 'is_active', 'is_deleted')
    
@admin.register(TaskItems)
class TaskItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson_task', 'task_text', 'expire_date', 'created_at', 'is_active', 'is_deleted') 
    


@admin.register(ExamForStudy)
class ExamForStudyAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'class_group', 'title', 'created_at', 'is_active', 'is_deleted') 
    

@admin.register(ExamForStudyItems)
class ExamForStudyItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam_for_study', 'title', 'created_at', 'is_active', 'is_deleted')    
    

@admin.register(ExamForStudyFiles)
class ExamForStudyFilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam_for_study', 'exam_for_study_items', 'files', 'created_at', 'is_active', 'is_deleted')   
    


# History models admin register
admin.site.register(CoursesHistory)
admin.site.register(RoomsHistory)
admin.site.register(ClassGroupsHistory)
admin.site.register(TeachersInGroupHistory)
admin.site.register(MentorsInGroupHistory)
admin.site.register(ClassGroupStudentsHistory)
admin.site.register(LessonHistory)
admin.site.register(AttendanceHistory)
admin.site.register(AttendanceStudentHistory)
admin.site.register(LessonTaskHistory)
admin.site.register(TaskItemsHistory)
    
