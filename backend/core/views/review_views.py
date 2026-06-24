from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .. import models
from .. import serializers

# See and append to a list of reviews (from owner or other users)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def book_review_list(request):
    # User wants to see the review (e.g. feed)
    if request.method == 'GET':
        reviews = models.BookReview.objects.all().order_by('-created_at')
        serializer = serializers.BookReviewSerializer(reviews, many=True)
        return Response(serializer.data)    # response with translated data
    
    # post a review and add to table of reviews
    if request.method == 'POST':
        serializer = serializers.BookReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def book_review_detail(request, primary_key):
    # Get a review row in the db
    try:
        review = models.BookReview.objects.get(pk=primary_key)
    except models.BookReview.DoesNotExist:
        return Response({"detail": "Review log not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        # User wants to see a single review
        if request.method == 'GET':
            serializer = serializers.BookReviewSerializer(review)
            return Response(serializer.data)

        # User wants to edit a review
        if request.method == 'PUT':
            # Check if user is owner
            if review.user != request.user:
                return Response({"detail": "You do not have permission to edit this log"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = serializers.BookReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # User wants to delete a review
        if request.method == 'DELETE':
            # Check if user is owner
            if review.user != request.user:
                return Response({"detail": "You do not have permission to delete this log"}, status=status.HTTP_403_FORBIDDEN)
            
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)