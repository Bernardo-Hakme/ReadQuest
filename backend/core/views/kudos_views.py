from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .. import models
from .. import serializers

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def kudos_toggle(request):
    if request.method == 'POST':
        serializer = serializers.KudosSerializer(data=request.data)

        if serializer.is_valid():
            # 1. Grab values from the validated data (session review)
            session = serializer.validated_data.get('session')
            review = serializer.validated_data.get('review')

            # 2. Run duplicate check
            if session:
                kudo_row = models.Kudos.objects.filter(user=request.user, session=session)
            elif review:
                kudo_row = models.Kudos.objects.filter(user=request.user, review=review)
            else:
                return Response({"detail": "You must specify a session or a review to like"}, status=status.HTTP_400_BAD_REQUEST)
            

            # if kudo exists delete kudo
            if kudo_row.exists():
                kudo_row.delete()
                return Response({"detail": "Kudo removed successfully"}, status=status.HTTP_200_OK)
            else:
            # if kudo does not exist, create kudo
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)