from .models import Assignment
from rest_framework.viewsets import ModelViewSet
from .serializers import AssignmentSerailizer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import permissions


class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerailizer

    # ! Permission for assignment
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]
