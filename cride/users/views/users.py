""" Users view"""

# Django REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

# Serializers
from cride.users.serializers.users import (
	UserLoginSerializer,
	UserModelSerializer,
	UserSignUpSerializer,
	UserVerificationSerializer
)

class UserViewSet(viewsets.GenericViewSet):
	""" User view set.
		Handle signup, login and account verification methods
	"""
	@action(detail=False, methods=['post'])
	def login(self, request):
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user, token = serializer.save()
		data = {
			'user': UserModelSerializer(user).data,
			'token': token
		}
		return Response(data, status=status.HTTP_201_CREATED)

	@action(detail=False, methods=['post'])
	def signup(self, request):
		serializer = UserSignUpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = UserModelSerializer(user).data
		return Response(data, status=status.HTTP_201_CREATED)
	
	@action(detail=False, methods=['post'])
	def verify(self, request):
		serializer = UserVerificationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		data = {'message': 'Your email has been verified. Now go and share rides.'}
		return Response(data, status=status.HTTP_200_OK)
