""" Users view"""

# Django REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Serializers
from cride.users.serializers.users import (
	UserLoginSerializer,
	UserModelSerializer,
	UserSignUpSerializer
)
class UserLoginAPIView(APIView):
	def post(self, request, *args, **kwargs):
		""" Handle http post request """
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user, token = serializer.save()
		data = {
			'user': UserModelSerializer(user).data,
			'token': token
		}
		return Response(data, status=201)

class UserSignUpAPIView(APIView):
	def post(self, request, *args, **kwargs):
		""" Handle http post request """
		serializer = UserSignUpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = UserModelSerializer(user).data
		return Response(data, status=status.HTTP_201_CREATED)
