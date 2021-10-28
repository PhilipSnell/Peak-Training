from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from .models import *
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date

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


class SetEntryFeedback(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    # @api_view(['POST', ])
    def post(self, request):
        if request.method == 'POST':
            data = {}
            data['response'] = ""

            serializer = SetFeedbackSerializer(data=request.data)

            set_feedback = SetFeedback.objects.filter(t_id=request.data.get("t_id"))
            if set_feedback:
                set_feedback = SetFeedback.objects.get(t_id=request.data.get("t_id"))
                if request.data.get("feedback") != "dif":

                    set_feedback.feedback=request.data.get("feedback")
                    set_feedback.save()

                if request.data.get("difficulty") != "":
                    set_feedback.difficulty=request.data.get("difficulty")
                    set_feedback.save()

                data['response'] = data['response'] + "entry already exists, updated "

            else:
                if serializer.is_valid():
                    serializer.save()
                    data['response'] = data['response'] + "feedback " " entered, "
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
            index = 1
            for item in request.data:
                serializer = SetSerializer(data=item)

                set_entry = Set_Entry.objects.filter(t_id=item.get("t_id"))
                if set_entry:
                    set_entry = Set_Entry.objects.get(t_id=item.get("t_id"))
                    set_entry.sets=item.get("sets")
                    set_entry.reps=item.get("reps")
                    set_entry.weights=item.get("weights")
                    set_entry.save()
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
        phases = Phase.objects.filter(user=user[0].id)
        for phase in phases:
            try:
                activeWeek = phase.weeks.get(isActive=True)
            except:
                print('active week not found')
        trainingData = TrainingEntry.objects.filter(user=user[0].id, phase = activeWeek.phase, week = activeWeek.week)

        serializer = TrainingSerializer(trainingData, many=True)

        return Response(serializer.data)

class ExerciseData(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        exerciseData = ExerciseType.objects.all()
        serializer = ExerciseSerializer(exerciseData, many=True)

        return Response(serializer.data)

class TrackingData(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        email_lookup = request.data["username"]
        user = User.objects.filter(email=email_lookup)
        groupData = TrackingGroup.objects.filter(clientToggle__in=user)

        serializer = GroupSerializer(groupData, many=True)

        return Response(serializer.data)

class TrackingValuesUpdate(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    # @api_view(['POST', ])
    def post(self, request):
        if request.method == 'POST':
            data = {}
            data['response'] = ""
            textVals = {}

            if request.data:
                textVals = request.data.get("textVals")
                email = request.data.get("client")
            index = 1
            for item in textVals:
                print(item.get('date')[0:10])
                textVal = TrackingTextValue.objects.filter(field_id=item.get("field_id"),
                                                           date=parse_date(item.get('date')[0:10]),
                                                           client=User.objects.get(email=email))
                textVal.update(value=item.get("value"))
                textVal = TrackingTextValue.objects.filter(field_id=item.get("field_id"),
                                                           date=parse_date(item.get('date')[0:10]),
                                                           client=User.objects.get(email=email))
                if textVal:
                    textVal.update(value=item.get("value"))
                    data['response'] = data['response'] + "entry "+str(index) + " already exists, "

                else:
                    item["client"] = User.objects.get(email=email).id
                    serializer = TrackTextValueSerializer(data=item,)
                    if serializer.is_valid():
                        serializer.save()
                        data['response'] = data['response'] + "entry "+str(index) + " entered, "
                    else:
                        data = serializer.errors
                index += 1
            print(data)
            return Response(data)

class TrackingValuesGet(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        email_lookup = request.data["username"]
        user = User.objects.filter(email=email_lookup)
        textValues = TrackingTextValue.objects.filter(client=user)
        print(textValues)   
        serializer = TrackTextValueSerializer(textValues, many=True)
        return Response(serializer)

def imageDisplay(request,id):
    emp = get_object_or_404(ExerciseType, pk=id)

    return render(request, 'image_display.html', {'emp': emp})
