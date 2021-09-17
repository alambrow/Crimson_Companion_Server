from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from django.http import HttpResponseServerError
from crimson_server.models import Student, CrimsonUser

class StudentView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        try:
            user = CrimsonUser.objects.get(id=request.auth.user_id)
            students = Student.objects.filter(user=user)
            serializer = StudentSerializer(students, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        user = CrimsonUser.objects.get(id=request.auth.user_id)
        student = Student()
        student.full_name = request.data["full_name"]
        student.email = request.data["email"]
        student.drive_url = request.data["drive_url"]
        student.is_active = True
        student.user = user
        try:
            student.save()
            serializer = StudentSerializer(student, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk=None):
        user = CrimsonUser.objects.get(id=request.auth.user_id)
        student = Student.objects.get(pk=pk)
        student.full_name = request.data["full_name"]
        student.email = request.data["email"]
        student.drive_url = request.data["drive_url"]
        student.is_active = request.data["is_active"]
        student.user = user

        try:
            student.save()
            return Response({'message': 'Student info updated.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def destroy(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response({'message': 'Student deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return HttpResponseServerError(ex)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'full_name', 'email', 'drive_url', 'is_active', 'user_id')
