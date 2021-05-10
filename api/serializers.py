from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
    def save(self):
        user = User(
            username = self.validated_data['username'],
            email= self.validated_data['email'],
            first_name= self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
        )
        user.save()
        return user