from ..services import username_not_in_database
from rest_framework import (
    viewsets,
    response,
    status,
    permissions,
    serializers as rest_serializers,
)
from datetime import datetime

from django.conf import settings

from .. import models, serializers, enums, permissions as account_permissions
from api.v1.company.models.models import Company


class StudentAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentSerializer
    permission_classes = (permissions.IsAuthenticated, account_permissions.IsOwnerOrReadOnly)

    # parser_classes = (parsers.MultiPartParser, )

    def get_queryset(self):

        students = models.Student.objects.filter(
            is_deleted=False,
            is_active=True,
            # date_start__lte=datetime.today().date(), 
            # date_finished__gt=datetime.today().date()
        ).order_by('-date_joined')

        return students

    def create(self, request, *args, **kwargs):
        company_id, phone_number = request.data.get('company'), request.data.get('phone_number')

        if username_not_in_database(company_id, phone_number):
            data = request.data.copy()

            username = str(company_id) + '|' + str(phone_number)

            data['username'] = username
            data['section'] = enums.Sections.education.value

            if not data.get('is_active'):
                data['is_active'] = 'true'

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        else:
            company = Company.objects.get(id=int(company_id))
            errors = {
                'phone_number': 'this << {} >> phone number is registered from the << {} >> company.'.format(
                    phone_number, company.name.title())
            }
            return response.Response(data=errors, status=status.HTTP_409_CONFLICT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False

# class TeacherAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Teacher.objects.all()
#     serializer_class = serializers.TeacherSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.education.value
#             data['role'] = enums.ProfileRoles.teacher.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class DirectorAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Director.objects.all()
#     serializer_class = serializers.DirectorSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.managers.value
#             data['role'] = enums.ProfileRoles.director.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class MentorAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Mentor.objects.all()
#     serializer_class = serializers.MentorSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.education.value
#             data['role'] = enums.ProfileRoles.mentor.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class ParentAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Parent.objects.all()
#     serializer_class = serializers.ParentSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.education.value
#             data['role'] = enums.ProfileRoles.parent.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class ManagerAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Manager.objects.all()
#     serializer_class = serializers.ManagerSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.managers.value
#             data['role'] = enums.ProfileRoles.manager.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class HrManagerAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.HrManager.objects.all()
#     serializer_class = serializers.HrManagerSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.managers.value
#             data['role'] = enums.ProfileRoles.hr_manager.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class AdministratorAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Administrator.objects.all()
#     serializer_class = serializers.AdministratorSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.managers.value
#             data['role'] = enums.ProfileRoles.administrator.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class MarketerAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Marketer.objects.all()
#     serializer_class = serializers.MarketerSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.marketing.value
#             data['role'] = enums.ProfileRoles.marketer.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class AccountantAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Accountant.objects.all()
#     serializer_class = serializers.AccountantSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.accounting.value
#             data['role'] = enums.ProfileRoles.accountant.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class CashierAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Cashier.objects.all()
#     serializer_class = serializers.CashierSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.accounting.value
#             data['role'] = enums.ProfileRoles.cashier.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class DeveloperAPIViewSet(viewsets.ModelViewSet):

#     queryset = models.Developer.objects.all()
#     serializer_class = serializers.DeveloperSerializer
#     # parser_classes = (parsers.MultiPartParser, )

#     def create(self, request, *args, **kwargs):

#         company_id, phone_number = request.data.get('company'), request.data.get('phone_number')
#         username = str(company_id) + '|' + str(phone_number)

#         try:
#             user = models.User.objects.get(username=username)
#             company = Company.objects.get(id=int(company_id))
#             return response.Response({'phone_number': "this phone number is registered from the << {} >> company.".format(company.name.title())})

#         except:
#             data = request.data.copy()
#             data['username'] = username
#             data['section'] = enums.Sections.managers.value
#             data['role'] = enums.ProfileRoles.developer.value

#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
