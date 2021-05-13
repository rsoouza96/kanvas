from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    user_set = UserSerializer(many=True, read_only=True)


class CoursePUTSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    user_ids = serializers.ListField(child=serializers.IntegerField())


class CourseAddUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    course_id = serializers.IntegerField()
    user_set = serializers.ListField(child=serializers.IntegerField())


class ActivitiesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    repo = serializers.CharField()
    grade = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()


class ActivitiesGradeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    grade = serializers.IntegerField()