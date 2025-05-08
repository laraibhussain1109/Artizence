from django.urls import path
from .views import UserCreateView, ProfileDetailView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='user-signup'),
    path('profile/', ProfileDetailView.as_view(), name='user-profile'),
]