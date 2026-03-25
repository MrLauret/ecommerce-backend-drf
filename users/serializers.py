from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User

class UserSerializer(ModelSerializer):
    email = serializers.EmailField(
        error_messages={
            "required": "Vui lòng nhập Email",
            "blank": "Vui lòng không được để trống",
            "invalid": "Email không hợp lệ"
        }
    )
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "avatar", "sex"]
        extra_kwargs = {
            "password": {"write_only": True}
        }


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)