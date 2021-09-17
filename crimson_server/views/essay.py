from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from crimson_server.models import Essay, CrimsonUser, Student
from django.http import HttpResponseServerError

class EssayView(ViewSet):

    def list(self, request):
        try:
            user = CrimsonUser.objects.get(id=request.auth.user_id)
            essays = Essay.objects.filter(user=user)
            serializer = EssaySerializer(
                essays, many=True, context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def retrieve(self, request, pk=None):
        try:
            essay = Essay.objects.get(id=pk)
            serializer = EssaySerializer(essay, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)  
    
    def create(self, request):
        user = CrimsonUser.objects.get(id=request.auth.user_id)
        student = Student.objects.get(id=request.data['student'])
        essay = Essay()
        essay.student = student
        essay.user = user
        essay.topic = request.data['topic']
        essay.official_dd = request.data['official_dd']
        essay.floating_dd = request.data['floating_dd']
        essay.is_complete = False
        essay.notes = request.data['notes']
        try:
            essay.save()
            serializer = EssaySerializer(essay, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        user = CrimsonUser.objects.get(id=request.auth.user_id)
        student = Student.objects.get(id=request.data['student'])
        essay = Essay.objects.get(id=pk)
        essay.student = student
        essay.user = user
        essay.topic = request.data['topic']
        essay.official_dd = request.data['official_dd']
        essay.floating_dd = request.data['floating_dd']
        essay.is_complete = request.data['is_complete']
        essay.notes = request.data['notes']
        
        try:
            essay.save()
            serializer = EssaySerializer(essay, context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def destroy(self, request, pk=None):
        try:
            essay = Essay.objects.get(id=pk)
            essay.delete()
            return Response({'message': 'Essay deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return HttpResponseServerError(ex)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'full_name', 'email', 'drive_url', 'is_active', 'user_id')

class EssaySerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False)

    class Meta:
        model = Essay
        fields = ('id', 'student', 'topic', 'official_dd', 'floating_dd', 'is_complete', 'notes', )