from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BaseAuthentication

from . import serializers

class UserApiView(generics.RetrieveAPIView):
    """
    This view has session and base authentication for testing purposes
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [SessionAuthentication, BaseAuthentication]
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user

class RegisterApiView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return Response({
            'user': serializers.UserSerializer(user).data,
            'token': AuthToken.objects.create(user)[1]
        })
    
class LoginApiView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validate_data
        return Response({
            'user': serializers.UserSerializer(user).data,
            'token': AuthToken.objects.create(user)[1]
        })