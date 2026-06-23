from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .. import models
from .. import serializers

class ReadingSessionViewSet(viewsets.ModelViewSet):
    queryset = models.ReadingSession.objects.all()
    serializer_class = serializers.ReadingSessionSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)