""" Circle views """

# Django REST
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Serializers
from cride.circles.serializers.circles import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership

# Permissions
from cride.circles.permissions import IsCircleAdmin

class CircleViewSet(mixins.CreateModelMixin,
					mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin,
					mixins.ListModelMixin,
					viewsets.GenericViewSet):
	serializer_class = CircleModelSerializer

	def get_permissions(self):
		""" Assign permissions based on circle action """
		permissions = [IsAuthenticated]
		if self.action in ['update', 'partial_update']:
			permissions.append(IsCircleAdmin)
		return [permission() for permission in permissions]

	def get_queryset(self):
		""" Restrict list method to public circles """
		queryset = Circle.objects.all()
		if self.action == 'list':
			return queryset.filter(is_public=True)
		return queryset
	
	def perform_create(self, serializer):
		""" Assign circle admin """
		circle = serializer.save()
		user = self.request.user
		profile = user.profile
		Membership.objects.create(
			user=user,
			profile=profile,
			circle=circle,
			is_admin=True,
			remaining_invitations=10
		)
