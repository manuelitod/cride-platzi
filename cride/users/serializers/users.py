""" User Serializer """

# Django REST
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Django
from django.contrib.auth import authenticate

# Models
from cride.users.models import User

class UserModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'phone_number'
		)

class UserLoginSerializer(serializers.Serializer):
	""" 
		Handle login on request data
	"""
	email = serializers.EmailField()
	password = serializers.CharField(min_length=8, max_length=64)

	def validate(self, data):
		""" Check user credentials """
		user = authenticate(username=data['email'], password=data['password'])
		if not user:
			raise serializers.ValidationError('Invalid credentials')
		self.context['user'] = user
		return data
	
	def create(self, data):
		""" Generate or retrieve user token """
		token, created = Token.objects.get_or_create(user=self.context['user'])
		return self.context['user'], token.key
