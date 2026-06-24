from django.utils import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import auth_views, profile_views, review_views, kudos_views, session_views

urlpatterns = [
    # auth
    path('auth/register/', auth_views.register_user, name='auth-register'),
    path('auth/login/', obtain_auth_token, name='auth-login'),

    # reading sessions
    path('sessions/', session_views.reading_session_list, name='session-list'),
    path('sessions/<int:primary_key>/', session_views.reading_session_detail, name='session-detail'),
    
    # book reviews
    path('reviews/', review_views.book_review_list, name='review-list'),
    path('reviews/<int:primary_key>/', review_views.book_review_detail, name='review-detail'),

    # kudos toggle
    path('kudos/toggle/', kudos_views.kudos_toggle, name='kudos-toggle'),

    # profile
    path('profile/', profile_views.user_profile, name='user-profile'),
]