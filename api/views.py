from datetime import datetime
from multiprocessing import context

from sqlalchemy import false, true
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
import myfitnesspal as mfp

User = get_user_model()


def updateLastActive(user):
    user.last_login = datetime.now()
    user.save()


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


class getSetFeedback(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    # @api_view(['POST', ])
    def post(self, request):
        if request.method == 'POST':
            try:
                setFeedback = SetFeedback.objects.get(
                    t_id=request.data.get('t_id'))
                serializer = getSetFeedbackSerializer(setFeedback)
                return Response(serializer.data)
            except:
                return Response({"feedback": "", "difficulty": ""})


class SetEntryFeedback(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    # @api_view(['POST', ])
    def post(self, request):
        if request.method == 'POST':
            data = {}
            data['response'] = ""

            serializer = SetFeedbackSerializer(data=request.data)

            set_feedback = SetFeedback.objects.filter(
                t_id=request.data.get("t_id"))
            if set_feedback:
                set_feedback = SetFeedback.objects.get(
                    t_id=request.data.get("t_id"))
                if request.data.get("feedback") != "dif":

                    set_feedback.feedback = request.data.get("feedback")
                    set_feedback.save()

                if request.data.get("difficulty") != "":
                    set_feedback.difficulty = request.data.get("difficulty")
                    set_feedback.save()

                data['response'] = data['response'] + \
                    "entry already exists, updated "

            else:
                if serializer.is_valid():
                    serializer.save()
                    data['response'] = data['response'] + \
                        "feedback " " entered, "
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
                    set_entry.sets = item.get("sets")
                    set_entry.reps = item.get("reps")
                    set_entry.weights = item.get("weights")
                    set_entry.save()
                    data['response'] = data['response'] + "entry " + \
                        str(index) + " already exists, updated, "

                else:
                    if serializer.is_valid():
                        serializer.save()
                        data['response'] = data['response'] + \
                            "entry "+str(index) + " entered, "
                    else:
                        data = serializer.errors

                serializer = SetFeedbackSerializer(data=item)

                set_feedback = SetFeedback.objects.filter(
                    t_id=item.get("t_id"))
                if set_feedback:
                    set_feedback = SetFeedback.objects.get(
                        t_id=item.get("t_id"))
                    if item.get("comment") != "dif":

                        set_feedback.comment = item.get("comment")
                        set_feedback.save()

                    if item.get("difficulty") != "":
                        set_feedback.difficulty = item.get("difficulty")
                        set_feedback.save()

                else:
                    if serializer.is_valid():
                        serializer.save()

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
        user = User.objects.get(email=email_lookup)
        updateLastActive(user)
        phases = Phase.objects.filter(user=user)
        for phase in phases:
            try:
                activeWeek = phase.weeks.get(isActive=True)
                activeWeek.updated = False
                activeWeek.save()
                trainingData = TrainingEntry.objects.filter(
                    user=user, phase=activeWeek.phase, week=activeWeek.week)
                break
            except:
                trainingData = None
                print('active week not found')

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
        updateLastActive(user[0])
        groupData = TrackingGroup.objects.filter(clientToggle__in=user)

        serializer = GroupSerializer(groupData,context={'user_id':user[0].id}, many=True)

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
                user = User.objects.get(email=email)
                updateLastActive(user)
            index = 1
            for item in textVals:

                textVal = TrackingTextValue.objects.filter(field_id=item.get("field_id"),
                                                           date=parse_date(
                                                               item.get('date')[0:10]),
                                                           client=user)
                textVal.update(value=item.get("value"))
                textVal = TrackingTextValue.objects.filter(field_id=item.get("field_id"),
                                                           date=parse_date(
                                                               item.get('date')[0:10]),
                                                           client=user)
                if textVal:
                    textVal.update(value=item.get("value"))
                    data['response'] = data['response'] + \
                        "entry "+str(index) + " already exists, "

                else:
                    item["client"] = user.id
                    serializer = TrackTextValueSerializer(data=item,)
                    if serializer.is_valid():
                        valueObject = serializer.save()
                        field = TrackingTextField.objects.get(
                            id=valueObject.field_id)
                        field.values.add(valueObject)
                        field.save()
                        data['response'] = data['response'] + \
                            "entry "+str(index) + " entered, "
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
        user = User.objects.get(email=email_lookup)
        updateLastActive(user)
        textValues = TrackingTextValue.objects.filter(client=user)
        print(textValues)
        serializer = TrackTextValueSerializer(textValues, many=True)
        return Response(serializer)


class SyncMyFitnessPal(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def patch(self, request):
        email_lookup = request.data["username"]
        user = User.objects.get(email=email_lookup)
        updateLastActive(user)
        try:
            myfitnesspal = MyFitnessPal.objects.get(user=user)
            mfpclient = mfp.Client(myfitnesspal.username)
            response = {
                "sync_required":False
            }
        except:
            response = {
                "sync_required":True
            }
        return Response(response)



    def post(self, request):
        email_lookup = request.data["username"]
        user = User.objects.get(email=email_lookup)
        username = request.data["mfp-username"]
        password = request.data["password"]
        print(username)
        print(password)
        try:
            myfitnesspal = MyFitnessPal.objects.get(user=user)
            myfitnesspal.username=username
            myfitnesspal.save()
        except MyFitnessPal.DoesNotExist:
            myfitnesspal = MyFitnessPal(user=user, username=username)
            myfitnesspal.save()
        try:
            mfpclient = mfp.Client(username=username, password=password)
            mfp.keyring_utils.store_password_in_keyring(username, password)
            
            response = {
                "sync_complete":True
            }
        except:
            response = {
                "sync_complete":False
            }

        return Response(response)

class CheckForUpdates(APIView):
    def post(self, request):
        email_lookup = request.data["username"]
        try:
            user = User.objects.get(email=email_lookup)
        except User.DoesNotExist:
            return Response()
        
        updateLastActive(user)
        phases = Phase.objects.filter(user=user).order_by('-id')
        for phase in phases:
            try:
                activeWeek = phase.weeks.get(isActive=True)
                response = activeWeek.updated
                response = {
                    "update":response
                }
                break
            except:
                trainingData = None
                print('active week not found')
                return Response()

        return Response(response)
        



def imageDisplay(request, id):
    emp = get_object_or_404(ExerciseType, pk=id)

    return render(request, 'image_display.html', {'emp': emp})

