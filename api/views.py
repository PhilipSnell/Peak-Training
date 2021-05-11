from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

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
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission

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

