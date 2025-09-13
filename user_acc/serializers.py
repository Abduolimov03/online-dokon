from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'address', 'age', 'password', 'password2', 'role']

    def validate(self, attrs):
        password = attrs.get('password', None)
        password2 = attrs.get('password2', None)

        if password is None and password2 is None:
            raise ValidationError('Parollar tolliq kiritilmagan')
        if password != password2:
            raise ValidationError('Parollar mos emas')

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'address', 'age', 'role']
        read_only_fields = ['username', 'email']
