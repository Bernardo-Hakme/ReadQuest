from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .. import models
from .. import serializers

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reading_session_list(request):
    # User wants to see the session (for feed e.g.)
    if request.method == 'GET':
        sessions = models.ReadingSession.objects.all().order_by('-created_at')
        serializer = serializers.ReadingSessionSerializer(sessions, many=True)

        return Response(serializer.data)
    
    # User wants to post a session
    if request.method == 'POST':
        serializer = serializers.ReadingSessionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# TODO reading session detail (put, delete)