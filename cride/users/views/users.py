""" Users view"""

# Django REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action

# Serializers
from cride.users.serializers.users import (
	UserLoginSerializer,
	UserModelSerializer,
	UserSignUpSerializer,
	UserVerificationSerializer
)

# Permissions
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated
)
from cride.users.permissions import IsAccountOwner
# Models
from cride.users.models import User

class UserViewSet(mixins.RetrieveModelMixin,
	viewsets.GenericViewSet):
	""" User view set.
		Handle signup, login and account verification methods
	"""
	queryset = User.objects.filter(is_active=True, is_client=True)
	serializer_class = UserModelSerializer
	lookup_field = 'username'

	def get_permissions(self):
		""" Get permissions based on actions """
		if self.action in ['login', 'signup', 'verify']:
			permissions = [AllowAny]
		elif self.action == 'retrieve':
			permissions = [IsAuthenticated, IsAccountOwner]
		else:
			permissions = [IsAuthenticated]
		return [p() for p in permissions]
	
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
