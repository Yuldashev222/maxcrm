from rest_framework import routers

from . import models

from .views import account_views


USER_CRUD_ROUTER = routers.SimpleRouter()

USER_CRUD_ROUTER.register('students', account_views.StudentAPIViewSet, basename='students')
# USER_CRUD_ROUTER.register('teachers', views.TeacherAPIViewSet)
# USER_CRUD_ROUTER.register('directors', views.DirectorAPIViewSet)
# USER_CRUD_ROUTER.register('mentors', views.MentorAPIViewSet)
# USER_CRUD_ROUTER.register('parents', views.ParentAPIViewSet)
# USER_CRUD_ROUTER.register('managers', views.ManagerAPIViewSet)
# USER_CRUD_ROUTER.register('hr_managers', views.HrManagerAPIViewSet)
# USER_CRUD_ROUTER.register('administrators', views.AdministratorAPIViewSet)
# USER_CRUD_ROUTER.register('marketers', views.MarketerAPIViewSet)
# USER_CRUD_ROUTER.register('accountants', views.AccountantAPIViewSet)
# USER_CRUD_ROUTER.register('cashiers', views.CashierAPIViewSet)
# USER_CRUD_ROUTER.register('developers', views.DeveloperAPIViewSet)












