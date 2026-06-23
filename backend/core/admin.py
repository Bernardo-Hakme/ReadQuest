from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ReadingSession, BookReview, Kudos

# This ensures your custom streak fields show up nicely in the admin panel
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('ReadQuest Gamification', {'fields': ('bio', 'profile_picture', 'current_streak', 'highest_streak', 'last_read_date')}),
    )

# Register your models to the dashboard
admin.site.register(User, CustomUserAdmin)
admin.site.register(ReadingSession)
admin.site.register(BookReview)
admin.site.register(Kudos)