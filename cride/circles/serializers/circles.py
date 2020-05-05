""" Circle serializers"""

# Django REST
from rest_framework import serializers

# Models
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Circle
		fields = (
			'name', 'slug_name', 'description',
			'picture', 'rides_offered', 'rides_taken',
			'verified', 'is_public', 'is_limited', 'members_limit'
		)
