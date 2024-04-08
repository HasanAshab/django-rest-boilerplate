from http import HTTPMethod
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import User
from .pagination import UserCursorPagination
from .serializers import ListUserSerializer, ProfileSerializer

#from .factories import UserFactory
#UserFactory.create_batch(10)



class UserViewSet(ViewSet):
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)
    pagination_class = UserCursorPagination

    def list(self, request):
        queryset = User.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        data = ListUserSerializer(result_page, many=True).data
        return paginator.get_paginated_response(data)
    
    def retrieve(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = ProfileSerializer(user, context={'user': request.user}).data
        return Response({'data': profile})
    
    def destroy(self, request, username):
        user = get_object_or_404(User, username=username)
        request.user.assert_can('delete', user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, url_path='me')
    def profile(self, request):
        profile = ProfileSerializer(request.user, context={'user': request.user}).data
        return Response({'data': profile})
    
    @profile.mapping.patch
    def updateProfile(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Profile updated!'
        })

    @action(detail=True, methods=[HTTPMethod.PATCH], url_path='admin')
    def makeAdmin(self, request, username):
        User.objects.filter(username=username).update(is_superuser=True)
        return Response({
            'message': 'Admin role granted to the user.'
        })