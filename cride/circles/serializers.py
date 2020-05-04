""" Circle serializers"""

# Django REST
from rest_framework import serializers

# Models
from cride.circles.models import Circle

class CircleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Circle
		fields = ['name', 'slug_name', 'description', 'rides_taken', 'rides_offered', 'members_limit']
