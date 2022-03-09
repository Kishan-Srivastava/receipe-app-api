from rest_framework import generics, authentication,permissions
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from user.api.serializers import UserSerializer,UserAuthTokenSerializer

class UserCreateAPIView(generics.CreateAPIView):

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class UserRUAPIView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        return self.request.user


class UserAuthToken(ObtainAuthToken):

    serializer_class = UserAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES