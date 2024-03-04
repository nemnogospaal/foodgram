from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPagePagination
from recipes.serializers import FollowSerializer
from users.models import Follow
from users.serializers import CustomUserSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitPagePagination
    search_fields = ('username', 'email')

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        return super().me(request)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(follow__user=request.user)
        paginate = self.paginate_queryset(queryset)
        serializer = FollowSerializer(paginate,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)
        if request.method == 'POST':

            serializer = FollowSerializer(author,
                                          data=request.data,
                                          context={'request': request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        subscribe = request.user.follower.filter(
            user=request.user, author=author)
        if not subscribe.exists():
            return Response('Вы не подписаны на этого пользователя',
                            status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response('Вы успешно отписались',
                        status=status.HTTP_204_NO_CONTENT)
