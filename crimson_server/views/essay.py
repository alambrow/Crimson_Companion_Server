from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from crimson_server.models import Essay, CrimsonUser
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

class EssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ('id', 'student', 'topic', 'official_dd', 'floating_dd', 'is_complete', 'notes', )