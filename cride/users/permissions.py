""" User permissions """

# Django Rest
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
	""" Allow acces only to objects owned by
		the requesting user. """

	def has_object_permission(self, request, view, obj):
		return request.user == obj
