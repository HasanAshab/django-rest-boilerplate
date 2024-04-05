from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .pagination import UserCursorPagination
from .serializers import ListUserSerializer, ProfileSerializer


class UserViewSet(ViewSet):
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]
    pagination_class = UserCursorPagination

    def list(self, request):
        queryset = User.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        data = ListUserSerializer(result_page, many=True).data
        return paginator.get_paginated_response(data)
    
    def retrieve(self, request, username):
        user = get_object_or_404(User, username=username)
        data = ProfileSerializer(user, context={'request': request}).data
        return Response({ 'data': data })
    
    def destroy(self, request, username):
        User.objects.filter(username=username).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, url_path='me')
    def profile(self, request):
        profile = ProfileSerializer(request.user, context={'request': request}).data
        return Response({ 'data': profile })
    
    @action(detail=False, methods=['patch'], url_path='me')
    def updateProfile(self, request):
        return Response('')

    @action(detail=True, methods=['patch'], url_path='admin')
    def makeAdmin(self, request, username):
        User.objects.filter(username=username).update(is_superuser=True)
        return Response({
            'message': 'Admin role granted to the user.'
        })