from django.contrib import admin


from simple_history import register, admin as history_admin


from .models import *


admin.site.register([
    Director,
    Mentor,
    Parent,
    Manager,
    HrManager,
    Administrator,
    Marketer,
    Accountant,
    Cashier,
])


register(Student, app=__package__, table_name='StudentHistory')
class StudentHistoryAdmin(history_admin.SimpleHistoryAdmin):
    list_display = ("id", "first_name", 'last_name', )
    history_list_display = ("first_name", 'last_name')
    search_fields = ('phone_number', )



register(Teacher, app=__package__, table_name='TeacherHistory')
class TeacherHistoryAdmin(history_admin.SimpleHistoryAdmin):
    list_display = ("id", "first_name", 'last_name', )
    history_list_display = ("first_name", )
    search_fields = ('phone_number', )
    

admin.site.register(Student, StudentHistoryAdmin)
admin.site.register(Teacher, TeacherHistoryAdmin)




