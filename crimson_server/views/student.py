from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from crimson_server.models import Student

class Student(ViewSet):

    def list(self, request):
        try:
            user = User.objects.get(id=request.auth.user_id)
            students = Student.objects.filter(user=user)
            serializer = StudentSerializer(students, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('full_name', 'email', 'drive_url', 'is_active', )