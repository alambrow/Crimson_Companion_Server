from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponseServerError

class Profile(ViewSet):

    def list(self, request):
        try:
            user = User.objects.get(id=request.auth.user_id)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')
