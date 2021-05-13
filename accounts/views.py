from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from .models import Course, Activity
from .permissions import IsSuperuser, IsAuthenticated
from .serializers import UserSerializer, LoginSerializer, CourseSerializer, CourseAddUserSerializer, ActivitiesSerializer, ActivitiesGradeSerializer, CoursePUTSerializer


class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        verify_user = User.objects.filter(username = request.data["username"]).exists()
        if verify_user:
            return Response(status=status.HTTP_409_CONFLICT)

        data = serializer.data
        user = User.objects.create_user(**data, password=request.data["password"])

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=request.data["username"], password=request.data["password"])

        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        token = Token.objects.get_or_create(user=user)[0]

        return Response({"token": token.key}, status=status.HTTP_200_OK)


class CourseView(APIView):
    queryset = Course.objects.none()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperuser]
    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        course = Course.objects.create(**data)
        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseRegistrationView(APIView):
    queryset = Course.objects.none()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperuser]
    def put(self, request):
        serializer = CoursePUTSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        users_in_db = Course.objects.get(id = request.data["course_id"])
        users_in_course = users_in_db.user_set.all()

        for student in users_in_course:
            if student.id not in serializer.data["user_ids"]:
                users_in_db.user_set.remove(student.id)
        
        for new_student in serializer.data["user_ids"]:
            users_in_db.user_set.add(new_student)

        serializer = CourseSerializer(users_in_db)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivitiesView(APIView):
    queryset = Activity.objects.none()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_activities = Activity.objects.filter(user_id=request.user.id)
        if request.data['repo'] in [activity.repo for activity in Activity.objects.filter(user_id=request.user.id)]:
            return Response(status=status.HTTP_409_CONFLICT)
        
        data = request.data
        data['user_id'] = request.user.id

        serializer = ActivitiesSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data

        activity = Activity.objects.create(**data)

        serializer = ActivitiesSerializer(activity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def put(self, request):
        activity = get_object_or_404(Activity, id=request.data['id'])
        serializer = ActivitiesGradeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        activity.grade = serializer.data['grade']
        activity.save()

        serializer = ActivitiesSerializer(activity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        if request.user.is_staff == False and request.user.is_superuser == False:
            queryset = Activity.objects.filter(user_id=request.user.id)
            serializer = ActivitiesSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.user.is_staff or request.user.is_superuser:
            queryset = Activity.objects.all()
            serializer = ActivitiesSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ActivityFilterView(APIView):
    queryset = Activity.objects.none()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        get_object_or_404(User, id=user_id)
        queryset = Activity.objects.filter(user_id=user_id)
        serializer = ActivitiesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)