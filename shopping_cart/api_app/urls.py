from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('profiles/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('profiles/<int:pk>/delete/', ProfileDeleteAPIView.as_view(), name='profile-delete'),
    path('profiles/bulk-delete/', ProfileBulkDeleteAPIView.as_view(), name='profile-bulk-delete'),
]

