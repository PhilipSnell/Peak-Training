
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()
class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('id_field')

    def id_field(self, exercise):
        return exercise.id
    class Meta:
        model = ExerciseType

        fields = ('name',
                  'description',
                  'id',
                  'video',
                  'image'
                  )


class TrainingSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()
    id = serializers.SerializerMethodField('id_field')

    def id_field(self, training):
        return training.id
    class Meta:
        model = TrainingEntry
        fields = ("id",
                  'user',
                  'phase',
                  'week',
                  'day',
                  'reps',
                  'weight',
                  'sets',
                  'exercise',
                  'comment'
                  )

class SetFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetFeedback
        fields = (
            't_id',
            'feedback',
            'difficulty',
        )

class SetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Set_Entry
        fields = (
            't_id',
            'sets',
            'reps',
            'weights',
            'e_id'
        )

class TrackTextValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackingTextValue
        fields = (
            "value",
            "client",
            "date",
            "field_id",
        )


class TextfieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingTextField
        fields = (
            'id',
            'name',
            'type',
        )



class GroupSerializer(serializers.ModelSerializer):
    textfields = TextfieldSerializer(many=True)

    class Meta:
        model = TrackingGroup
        fields = (
            'name',
            'textfields',
        )


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
        extra_kwags= {
            'password': {'write_only':True}
        }
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
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

class getSetFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = SetFeedback
        fields = (
            'feedback',
            'difficulty',
        )


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

