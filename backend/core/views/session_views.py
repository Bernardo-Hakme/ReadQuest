from django.utils import timezone
from datetime import timedelta
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
            now = timezone.now()
            
            last_session = models.ReadingSession.objects.filter(author=request.user).order_by('-created_at').first()
            
            user_profile = request.user

            if last_session:
                time_since_last_session = now - last_session.created_at

                if time_since_last_session < timedelta(hours=24):
                    user_profile.current_streak += 1
                else:
                    user_profile = 1
            else:
                user_profile.streak = 1

            if user_profile.current_streak > user_profile.highest_streak:
                user_profile.highest_streak = user_profile.current_streak

            user_profile.save()

            serializer.save(user=request.user)            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def reading_session_detail(request, primary_key):
    try:
        # get the id of a reading session row
        session = models.ReadingSession.objects.get(pk=primary_key)
    except models.ReadingSession.DoesNotExist:
        return Response({"detail": "Reading log not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        # User wants to see a specific Session
        if request.method == 'GET':
            serializer = serializers.ReadingSessionSerializer(session)
            return Response(serializer.data)
        
        #User wants to edit a specific Session
        if request.method == 'PUT':
            # if user is not owner of the posted session
            if session.user != request.user:
                return Response({"detail": "You do not have permission to edit this log"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = serializers.ReadingSessionSerializer(session, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # User wants to delete a session
        if request.method == 'DELETE':
            # check if user is owner of post
            if session.user != request.user:
                return Response({"detail": "You do not have permission to delete this log"}, status=status.HTTP_403_FORBIDDEN)

            session.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
