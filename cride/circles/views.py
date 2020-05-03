""" Circle views."""

# Django REST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


# Serializers
from cride.circles.serializers import CircleSerializer

# Models
from cride.circles.models import Circle

@api_view(['GET', 'POST'])
def list_circles(request):
	""" 
		List all public circles
		or crete a new circle	
	"""
	if request.method == 'GET':
		circles = Circle.objects.all().filter(is_public=True)
		circles_serializer = CircleSerializer(circles, many=True)
		return Response(circles_serializer.data, status=200)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		circle_serializer = CircleSerializer(data=data)
		if circle_serializer.is_valid():
			circle_serializer.save()
			return Response(circle_serializer.data, status=201)
		return Response(circle_serializer.errors, status=400)
