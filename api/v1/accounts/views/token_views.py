from rest_framework import (
    response, 
    status, 
    serializers as rest_serializers
)

from rest_framework_simplejwt import (
    views as jwt_views, 
    exceptions as jwt_exceptions, 
    serializers as jwt_serializers,
    tokens as jwt_tokens
)

# token = jwt_tokens.RefreshToken('base64_encoded_token_string')
# token.blacklist()


class UserTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = jwt_serializers.TokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        company_id, phone_number = request.data.get('company_id'), request.data.get('phone_number')
        errors = dict()
        
        if not company_id:
            errors['company_id'] = ['This field is required.']
            
        if not phone_number:
            errors['phone_number'] = ['This field is required.']

        if not request.data.get('password'):
            errors['password'] = ['This field is required.']
            
        if errors:
            raise rest_serializers.ValidationError(errors)
            
        data = request.data.copy()
        data['username'] = str(company_id) + '|' + str(phone_number)
        del data['phone_number'], data['company_id']

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exceptions.TokenError as e:
            raise jwt_exceptions.InvalidToken(e.args[0])
        
        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)