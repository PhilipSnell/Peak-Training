from .serializers import UserSerializer, TrainingSerializer, ExerciseSerializer, SetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from .models import TrainingEntry, ExerciseType, Set_Entry
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = []

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class Registration(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    # @api_view(['POST', ])
    def post(self, request):
        if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                user = serializer.save()
                data['response'] = "successfully registered a new user"
                data['email'] = user.email
                data['username'] = user.username
            else:
                data = serializer.errors
            return Response(data)

class SetEntry(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    # @api_view(['POST', ])
    def post(self, request):
        if request.method == 'POST':
            data = {}
            data['response'] = ""
            index = 1;
            for item in request.data:
                serializer = SetSerializer(data=item)

                set_entry = Set_Entry.objects.filter(t_id=item.get("t_id"))
                if set_entry:
                    set_entry.update(sets=item.get("sets"),reps=item.get("reps"),weights=item.get("weights"))
                    data['response'] = data['response'] + "entry "+str(index)+ " already exists, "

                else:
                    if serializer.is_valid():
                        serializer.save()
                        data['response'] = data['response'] + "entry "+str(index)+ " entered, "
                    else:
                        data = serializer.errors
                index += 1
            return Response(data)

class TrainingData(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        # print(request.data["username"]+ "- blah blah")
        email_lookup = request.data["username"]
        user = User.objects.filter(email=email_lookup)
        trainingData = TrainingEntry.objects.filter(user=user[0].id)

        serializer = TrainingSerializer(trainingData, many=True)

        return Response(serializer.data)

class ExerciseData(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        print(request.data['username']+ "- blah blah")
        email_lookup = "psnell63@gmail.com"
        user = User.objects.filter(email=email_lookup)
        exerciseData = ExerciseType.objects.all()
        serializer = ExerciseSerializer(exerciseData, many=True)

        return Response(serializer.data)

def imageDisplay(request,id):
    emp = get_object_or_404(ExerciseType, pk=id)

    return render(request, 'image_display.html', {'emp': emp})
