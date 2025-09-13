from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from .models import CustomUser
from rest_framework.response import Response
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


class RegisterApi(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Siz royxatdan otdingiz', 'status':status.HTTP_201_CREATED})
        return Response({'err':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})


class LoginApi(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']

        if not CustomUser.objects.filter(email=email).exists():
            return Response({
                'err':'Bunday loginli foydalanuvchi mavjud emas',
                'status':status.HTTP_400_BAD_REQUEST
            })

        user = authenticate(email=email, password=password)
        token = RefreshToken.for_user(user)

        data = {
            'refresh': str(token),
            'access':str(token.access_token),
            'status':status.HTTP_200_OK
        }
        return Response(data)


class LogoutApi(APIView):
    def post(self, request):
        data = request.data
        try:
            token = RefreshToken(data['refresh'])
            token.blacklist()
            return Response({'msg':'Siz dasturdan chiqdingiz', 'status':status.HTTP_200_OK})
        except Exception as e:
            return Response(
                {
                    "err":str(e),
                    "status":status.HTTP_400_BAD_REQUEST
                }
            )

class ProfileApi(APIView):
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response({
            'data':serializer.data,
            'status':status.HTTP_200_OK
        })

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'status': status.HTTP_200_OK
            })