from datetime import datetime

# from django.forms import model_to_dict
from django.core import exceptions
from django.contrib.auth import password_validation, hashers, authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import update_last_login

from rest_framework import serializers, response
# from rest_framework_simplejwt import settings as simplejwt_settings, tokens as simplejwt_tokens

from . import models, services, enums
from api.v1.company.models.models import Company


# class PasswordField(serializers.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault("style", {})

#         kwargs["style"]["input_type"] = "password"
#         kwargs["write_only"] = True

#         super().__init__(*args, **kwargs)


# class TokenObtainSerializer(serializers.Serializer):
#     username_field = get_user_model().USERNAME_FIELD
#     token_class = None

#     default_error_messages = {
#         "no_active_account": _("No active account found with the given credentials")
#     }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields[self.username_field] = serializers.CharField()
#         self.fields["password"] = PasswordField()

#     def validate(self, attrs):
#         authenticate_kwargs = {
#             self.username_field: attrs[self.username_field],
#             "password": attrs["password"],
#         }
#         try:
#             authenticate_kwargs["request"] = self.context["request"]
#         except KeyError:
#             pass

#         self.user = authenticate(**authenticate_kwargs)

#         if not simplejwt_settings.api_settings.USER_AUTHENTICATION_RULE(self.user):
#             raise exceptions.AuthenticationFailed(
#                 self.error_messages["no_active_account"],
#                 "no_active_account",
#             )

#         return {}

#     @classmethod
#     def get_token(cls, user):
#         return cls.token_class.for_user(user)


# class TokenObtainPairSerializer(TokenObtainSerializer):
#     token_class = simplejwt_tokens.RefreshToken

#     def validate(self, attrs):
#         data = super().validate(attrs)

#         refresh = self.get_token(self.user)

#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)

#         if simplejwt_settings.api_settings.UPDATE_LAST_LOGIN:
#             update_last_login(None, self.user)

#         return data


# class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['name'] = user.first_name
#         # ...

#         return token


class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class StudentSerializer(serializers.ModelSerializer):
    creator_id = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = models.Student
        exclude = ('username', 'role', 'is_staff', 'is_admin', 'is_superuser')

        read_only_fields = ('creator',)

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        validated_data['role'] = enums.ProfileRoles.student.value

        return super().create(validated_data)

    def update(self, instance, validated_data):

        errors = {}
        company = validated_data.get('company')
        phone_number = validated_data.get('phone_number')

        # checking that the second phone number is not equal to the first phone number -----------
        second_phone_number = validated_data.get('second_phone_number')

        if (
                second_phone_number and second_phone_number == instance.phone_number or
                second_phone_number and phone_number and phone_number == second_phone_number
        ):
            errors['second_phone_number'] = ['the additional phone number is the same as the main phone number']
        # ----------------------------------------------------------------------------------------

        if company and phone_number:
            if company.id != instance.company.id or phone_number != instance.phone_number:

                if not services.username_not_in_database(company_id=company.id, phone_number=phone_number):
                    errors['company'] = ['this phone number is registered with this company']

        elif company:
            if company.id != instance.company_id:

                if not services.username_not_in_database(company_id=company.id, phone_number=instance.phone_number):
                    errors['company'] = ['this phone number is registered with this company']

        elif phone_number:
            if phone_number != instance.phone_number:

                if not services.username_not_in_database(company_id=instance.company_id, phone_number=phone_number):
                    errors['phone_number'] = ['this phone number is registered in the company']

        if errors:
            raise serializers.ValidationError(errors)

        return super().update(instance, validated_data)

    def validate(self, data):
        user = models.Student(**data)

        errors = dict()

        # date_start and date_finished validations  ----------------------
        date_start = data.get('date_start')
        date_finished = data.get('date_finished')
        today_date = datetime.today().date()

        if date_start and date_finished:

            if date_start < today_date:
                errors['date_start'] = ['start date before today\'s date.']

            if date_start >= date_finished:
                errors['date_finished'] = ['end date before start date.']

        elif date_start:

            if date_start < today_date:
                errors['date_start'] = ['start date before today\'s date.']

        elif date_finished:
            data['date_start'] = today_date
            if date_finished <= today_date:
                errors['date_finished'] = ['end date before today\'s date']
        # --------------------------------------------------------------------

        # password validations -----------------------------------------------
        password = data.get('password')
        if password:
            try:
                password_validation.validate_password(password=password, user=user)

            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)

            data['password'] = hashers.make_password(data['password'])
        # --------------------------------------------------------------------

        if errors:
            raise serializers.ValidationError(errors)

        return super(StudentSerializer, self).validate(data)

# class DirectorSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class TeacherSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class MentorSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class ParentSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class ManagerSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class HrManagerSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class AdministratorSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class MarketerSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class AccountantSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class CashierSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )


# class DeveloperSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = models.User
#         exclude = ('username', )
