""" Circle model """

# Django
from django.db import models

# Utilities
from cride.utils.models import CrideModel

class Circle(CrideModel):
	"""
		Private group where rides are offered and taken
	by its members. To join a circle user must receive
	an unique invitation code from an existing circle member.
	"""

	name = models.CharField('circle name', max_length=140)
	slug_name = models.SlugField(unique=True, max_length=40)
	description = models.CharField('circle description', max_length=255, blank=True)
	picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)
	verified = models.BooleanField(
		'verified circle',
		default=False,
		help_text='Verified circles are also known as oficcial communitties.'
	)
	is_public = models.BooleanField(
		default=True,
		help_text='Public circles are listed in the main page so everyone know about them.'
	)
	is_limited = models.BooleanField(
		'limited',
		default=False,
		help_text='Limited circles can grow up to a fixed number of members.'
	)
	members_limit = models.PositiveIntegerField(
		default=0,
		help_text='Member limit for limited circles.'
	)

	# Stats
	rides_offered = models.PositiveIntegerField(default=0)
	rides_taken = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.name
	
	class Meta(CrideModel.Meta):
		ordering = ['-rides_taken', '-rides_offered']
