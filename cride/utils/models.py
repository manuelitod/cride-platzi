"""Django models utilities"""

# Django
from django.db import models

class CrideModel(models.Model):
	""" Abstract class for all other class
	in the project. This class provide
	every table with the following attributes:
		+ created (DateTime): Store the datetime the object was created.
		+ modified (DateTime): Store the last datetime the object was modified.
	"""

	created = models.DateTimeField(
		'created at',
		auto_now_add=True,
		help_text='Date time on which the object was created.'
	)
	modified = models.DateTimeField(
		'modified at',
		auto_now=True,
		help_text='Date time on which the object was last modified.'
	)

	class Meta:
		"""Meta option."""

		abstract = True

		get_latest_by = 'created'
		ordering = ['-created', '-modified']
