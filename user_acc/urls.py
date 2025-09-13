# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from django.urls import path
from .views import RegisterApi, LoginApi, LogoutApi, ProfileApi


urlpatterns = [
    path('regis/', RegisterApi.as_view()),
    path('login/', LoginApi.as_view()),

    path('logout/', LogoutApi.as_view()),
    path('profile/', ProfileApi.as_view())
]