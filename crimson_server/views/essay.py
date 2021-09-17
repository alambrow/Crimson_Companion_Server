from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from crimson_server.models import Essay, CrimsonUser, Student
from django.http import HttpResponseServerError
import datetime

class EssayView(ViewSet):

    def list(self, request):
        try:
            user = CrimsonUser.objects.get(id=request.auth.user_id)
            
            student = self.request.query_params.get('student', None)
            upcoming = self.request.query_params.get('upcoming', None)
            day = self.request.query_params.get('day', None)

            if student is not None:
                essays = Essay.objects.filter(user=user, student=student).order_by('official_dd')
            elif upcoming is not None:
                essays = Essay.objects.filter(user=user).order_by('official_dd')[:int(upcoming)]
            elif day is not None:
                start_date = datetime.datetime.strptime(day, '%Y-%m-%d')
                end_date = start_date + datetime.timedelta(days=7)
                essays = Essay.objects.filter(user=user, official_dd__range=[start_date, end_date])
            else:
                essays = Essay.objects.filter(user=user).order_by('official_dd')
            
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