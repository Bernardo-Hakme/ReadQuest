from rest_framework import serializers
from .models import User, ReadingSession, BookReview, Kudos

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer blueprint for translating User Profile and streak records.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'bio',
            'profile_picture',
            'current_streak',
            'highest_streak',
            'last_read_date',
        ]

class ReadingSessionSerializer(serializers.ModelSerializer):
    """
    Serializer blueprint for translating individual timed Reading Logs.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ReadingSession
        fields = [
            'id',
            'user',
            'book_title',
            'author',
            'pages_read',
            'duration_minutes',
            'photo',
            'created_at',
        ]


class BookReviewSerializer(serializers.ModelSerializer):
    """
    Serializer blueprint for translating Book Reviews and ratings.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = BookReview
        fields = [
            'id',
            'user',
            'book_title',
            'author',
            'num_pages_total',
            'language_read',
            'rating',
            'review_text',
            'photo',
            'created_at',
        ]


class KudosSerializer(serializers.ModelSerializer):
    """
    Serializer blueprint for translating social likes/kudos.
    """
    class Meta:
        model = Kudos
        fields = [
            'id',
            'user',
            'session',
            'review',
            'created_at',
        ]