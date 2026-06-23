from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    current_streak = models.IntegerField(default=0)
    highest_streak = models.IntegerField(default=0)
    last_read_date = models.DateField(blank=True, null=True)

class ReadingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    book_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pages_read = models.IntegerField()
    duration_minutes = models.IntegerField()
    photo = models.ImageField(upload_to='sessions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} read {self.pages_read} pages of '{self.book_title}'"
    
class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    num_pages_total = models.IntegerField()
    language_read = models.CharField(max_length=255)
    rating = models.IntegerField()
    review_text = models.TextField()
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} review of '{self.book_title}'"
    
class Kudos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(ReadingSession, on_delete=models.CASCADE, null=True, blank=True, related_name='kudos')
    review = models.ForeignKey(BookReview, on_delete=models.CASCADE, null=True, blank=True, related_name='kudos')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Kudos"

        unique_together = ('user', 'session', 'review')
