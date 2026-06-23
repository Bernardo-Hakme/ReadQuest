from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .. import models
from .. import serializers

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def book_review_list(request):
    # User wants to see the review (e.g. feed)
    if request.method == 'GET':
        reviews = models.BookReview.objects.all().order_by('-created_at')
        serializer = serializers.BookReviewSerializer(reviews, many=True)
        return Response(serializer.data)    # response with translated data
    
    if request.method == 'POST':
        serializer = serializers.BookReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#TODO book review detail (put, delete)