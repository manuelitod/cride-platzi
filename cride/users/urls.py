""" Users urls"""

# Django
from django.urls import path

# Views
from cride.users.views import (
	UserLoginAPIView,
	UserSignUpAPIView,
	UserVerificationAPIView
)

urlpatterns = [
	path('users/login/', UserLoginAPIView.as_view(), name='login'),
	path('users/signup/', UserSignUpAPIView.as_view(), name='signup'),
	path('users/verify/', UserVerificationAPIView.as_view(), name='verify_user')
]
