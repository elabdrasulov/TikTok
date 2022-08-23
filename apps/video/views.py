from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .permissions import *
from .serializers import *


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter, 
        filters.SearchFilter, 
        DjangoFilterBackend,
    ]
    filterset_fields = ['title', 'user', 'videos_tags', ]
    search_fields = ['title', 'user', 'videos_tags','category__title',]
    ordering_fields = ['title', 'user', ]

    @action(methods=['GET'], detail=True)
    def view(self, request, pk):
        video = get_object_or_404(Post, id=pk)
        video.views += 1
        video.save()
        return Response("View added")

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("title", 
                          openapi.IN_QUERY, 
                          "search products by title", 
                          type=openapi.TYPE_STRING)])
    @action(methods=['GET'], detail=False)
    def search(self, request):
        title = request.query_params.get("title")
        queryset = self.get_queryset()
        if title:
            queryset = queryset.filter(title__icontains=title)

        serializer = PostSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data, 200)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class FavoriteView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset

@api_view(['GET'])
def add_to_favorite(request, v_id):
    user = request.user
    video = get_object_or_404(Post, id=v_id)

    if Favorite.objects.filter(user=user, video=video).exists():
        Favorite.objects.filter(user=user, video=video).delete()
        return Response('Deleted from favorite')
    else:
        Favorite.objects.create(user=user, video=video, favorited=True)
        return Response('Added to favorites')

# @api_view (['GET'])
# def view(request, v_id):
#     video = get_object_or_404(Post, id=v_id)
#     video.views += 1
#     video.save()
#     return Response("View added")


@api_view(['GET'])
def toggle_post_like(request, v_id):
    user = request.user
    video = get_object_or_404(Post, id=v_id)

    if LikePost.objects.filter(user=user, video=video).exists():
        LikePost.objects.filter(user=user, video=video).delete()
    else:
        LikePost.objects.create(user=user, video=video)
    return Response("Like toggled", 200)