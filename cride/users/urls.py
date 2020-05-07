""" Users urls"""

# Django
from django.urls import include, path

# Views
from cride.users.views import users as user_views

# Django REST
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
	path('', include(router.urls))
]
