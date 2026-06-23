from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .. import models
from .. import serializers

class KudosViewSet(viewsets.ModelViewSet):
    queryset = models.Kudos.objects.all()
    serializer_class = serializers.KudosSerializer 

    permission_classes = [IsAuthenticated]

# TODO avoid user to like multiple times
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# TODO rewrite it to function decorator style (like review/session_views.py)