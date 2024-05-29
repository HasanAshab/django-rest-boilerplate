from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveDestroyAPIView,
)
from .models import User
from .permissions import DeleteUserPermission
from .serializers import (
    ListUserSerializer,
    UserDetailsSerializer,
)
from .pagination import UserPagination


class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    pagination_class = UserPagination


class UserDetailsView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, DeleteUserPermission)
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserDetailsSerializer
