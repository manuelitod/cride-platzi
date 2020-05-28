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
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.circles.serializers.circles import CircleModelSerializer

# Permissions
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated
)
from cride.users.permissions import IsAccountOwner

# Models
from cride.users.models import User
from cride.circles.models.circles import Circle

class UserViewSet(mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
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
		elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
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
	
	@action(detail=True, methods=['put', 'patch'])
	def profile(self, request, *args, **kwargs):
		""" Update profile data """
		user = self.get_object()
		profile = user.profile
		partial = request.method == 'PATCH'
		serializer = ProfileModelSerializer(
			profile,
			data=request.data,
			partial=partial
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		data = UserModelSerializer(user).data
		return Response(data,  status=status.HTTP_200_OK)
	
	def retrieve(self, request, *args, **kwargs):
		""" Add extra data to response """
		response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
		circles = Circle.objects.filter(
			members=request.user,
			membership__is_active=True
		)
		data = {
			'users': response.data,
			'circles': CircleModelSerializer(circles, many=True).data
		}
		response.data = data
		return response
