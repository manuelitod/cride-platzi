""" User model"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CrideModel

class User(CrideModel, AbstractUser):
	""" User model.

	Custom user model from Django Abstract User,
	override username field to email.
	"""

	email = models.EmailField(
		'email address',
		unique=True,
		error_messages={
			'unique': 'An user with this email already exists.'
		}
	)
	phone_validator = RegexValidator(
		regex='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$',
		message='Phone number must be match format: +9999999'
	)
	phone_number = models.CharField(max_length=17, blank=True, validators=[phone_validator])
	is_client = models.BooleanField(
		'client',
		default=True,
		help_text=(
			'Helper for distinguish users'
			'Clients are the main type of users.'
		)
	)
	is_verified = models.BooleanField(
		'verified',
		default=True,
		help_text='True if the user has a verified email.'
	)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	def __str__(self):
		return self.username
	
	def get_short_name(self):
		return self.username
