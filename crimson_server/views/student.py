from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from django.http import HttpResponseServerError
from crimson_server import models
from crimson_server.models import Student, CrimsonUser

class StudentView(ViewSet):

    def list(self, request):
        try:
            user = CrimsonUser.objects.get(id=request.auth.user_id)
            students = Student.objects.filter(user=user)
            serializer = StudentSerializer(students, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        try:
            user = CrimsonUser.objects.get(id=request.auth.user_id)
            student = Student()
            student.full_name = request.data["full_name"]
            student.email = request.data["email"]
            student.drive_url = request.data["drive_url"]
            student.is_active = True
            student.user = user
            student.save()
            serializer = StudentSerializer(student, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex}, status=status.HTTP_400_BAD_REQUEST)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('full_name', 'email', 'drive_url', 'is_active', 'user_id')
