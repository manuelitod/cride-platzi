""" User Serializer """

# Django REST
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Django
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

# PyJWT
import jwt

# Utilities
from datetime import timedelta

# Models
from cride.users.models import User, Profile

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer

class UserModelSerializer(serializers.ModelSerializer):
	profile = ProfileModelSerializer(read_only=True)

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'phone_number',
			'profile'
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
		if not user.is_verified:
			raise serializers.ValidationError('Email account is not verified')
		self.context['user'] = user
		return data
	
	def create(self, data):
		""" Generate or retrieve user token """
		token, created = Token.objects.get_or_create(user=self.context['user'])
		return self.context['user'], token.key

class UserSignUpSerializer(UserModelSerializer):
	""" Handle sign up data validation and
		profile creation.
	"""
	password_confirmation = serializers.CharField(min_length=8, max_length=64)

	class Meta(UserModelSerializer.Meta):
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'phone_number',
			'password',
			'password_confirmation',
		)
		extra_kwargs = {
			'first_name': { 'required': True },
			'last_name': { 'required': True },
			'phone_number': { 'required': True }
		}

	def validate(self, data):
		if data['password'] != data['password_confirmation']:
			raise serializers.ValidationError("Passwords don't match")
		return data
	
	def create(self, validated_data):
		validated_data.pop('password_confirmation')
		user = User.objects.create_user(**validated_data, is_verified=False, is_client=True)
		profile = Profile.objects.create(user=user)
		self.send_confirmation_email(user)
		return user
	
	def send_confirmation_email(self, user):
		""" Send account verification link to given user """
		verification_token = self.gen_verification_token(user)
		subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
		from_email = 'Comparte Ride <noreply@comparteride.com>'
		content = render_to_string(
			'emails/users/account_verification.html', 
			{'token': verification_token, 'user': user}
		)
		msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
		msg.attach_alternative(content, "text/html")
		msg.send()

	def gen_verification_token(self, user):
		""" Create JWT token to verify a new account """
		expiration_date = timezone.now() + timedelta(days=3)
		payload = {
			'user': user.username,
			'exp': int(expiration_date.timestamp()),
			'type': 'email_confirmation'
		}
		token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
		return token.decode()

class UserVerificationSerializer(serializers.Serializer):
	""" Account verification serializer """

	token = serializers.CharField()

	def validate_token(self, data):
		""" Check if token is valid """
		try:
			payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			raise serializers.ValidationError('Verification link has expired')
		except jwt.PyJWTError:
			raise serializers.ValidationError('Invalid token')
		if payload.get('type', '') != 'email_confirmation':
			raise serializers.ValidationError('Invalid token')
		self.context['payload'] = payload
		return data
	
	def save(self):
		""" Update verify status for a specific user """
		payload = self.context['payload']
		users = User.objects.get(username=payload['user'])
		users.is_verified = True
		users.save()
