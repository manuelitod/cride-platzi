""" Users view"""

# Django REST
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from cride.users.serializers.users import (
	UserLoginSerializer,
	UserModelSerializer
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
