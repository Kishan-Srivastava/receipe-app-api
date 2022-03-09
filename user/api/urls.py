from django.contrib import admin
from django.urls import path,include

from user.api import views

app_name = 'user'

urlpatterns = [
    path('create/', views.UserCreateAPIView.as_view(),name='create'),
    path('token/',views.UserAuthToken.as_view(),name='token'),
    path('me/',views.UserRUAPIView.as_view(),name='me')
]
