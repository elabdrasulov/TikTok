from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .permissions import *
from .serializers import *


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [
        filters.OrderingFilter, 
        filters.SearchFilter, 
        DjangoFilterBackend,
    ]
    filterset_fields = ['title', 'video_tags', ]
    search_fields = ['title', 'video_tags', 'user__username', 'categories__title']
    ordering_fields = ['title', ]

    # def get_permissions(self):
    #     return super().get_permissions()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "title", 
                openapi.IN_QUERY, 
                "search videos by title", 
                type=openapi.TYPE_STRING
            )
        ]
    )
    @action(methods=['GET'], detail=False)
    def search(self, request):
        title = request.query_params.get("title")
        queryset = self.get_queryset()
        if title:
            queryset = queryset.filter(title__icontains=title)

        serializer = PostSerializer(
            queryset, many=True, context={"request":request}
        )
        return Response(serializer.data, 200)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "categories", 
                openapi.IN_QUERY, 
                "search videos by categories", 
                type=openapi.TYPE_STRING
            )
        ]
        # query_serializer=PostSerializer
    )
    @action(methods=['GET'], detail=False)
    def recommendations(self, request):
        categories_title = request.query_params.get("categories")
        categories = Category.objects.get(title__icontains=categories_title)
        
        queryset = self.get_queryset()
        queryset = queryset.filter(categories=categories)

        queryset = sorted(
            queryset, key=lambda post: post.post_likes.all().count(), reverse=True
        )

        serializer = PostSerializer(
            queryset, many=True, context={"request":request}
        )
        return Response(serializer.data, 200)

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny,]

    def get(self, request,  pk, *args, **kwargs):
        video = get_object_or_404(Post, pk=pk)
        video.views += 1
        video.save()
        serializer =PostSerializer(video)
        return Response(serializer.data)

class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrAuthor, ]

class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrAuthor, ]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CommentListDetailView(
    ListAPIView, RetrieveAPIView
):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

class FavoriteView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset

class LikePostView(ListAPIView):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset

@api_view(['GET'])
def add_to_favorite(request, v_id):
    user = request.user
    post = get_object_or_404(Post, id=v_id)

    if Favorite.objects.filter(user=user, post=post).exists():
        Favorite.objects.filter(user=user, post=post).delete()
        return Response('Deleted from favorite')
    else:
        Favorite.objects.create(user=user, post=post)
        return Response('Added to favorites')


@api_view(['GET'])
def toggle_post_like(request, v_id):
    user = request.user
    post = get_object_or_404(Post, id=v_id)

    if LikePost.objects.filter(user=user, post=post).exists():
        LikePost.objects.filter(user=user, post=post).delete()
        return Response("Like untoggled")
    else:
        LikePost.objects.create(user=user, post=post)
    return Response("Like toggled")

@api_view(['GET'])
def toggle_comment_like(request, c_id):
    user = request.user
    comment = get_object_or_404(Comment, id=c_id)

    if LikeComment.objects.filter(user=user, comment=comment).exists():
        LikeComment.objects.filter(user=user, comment=comment).delete()
        return Response("Like untoggled")
    else:
        LikeComment.objects.create(user=user, comment=comment)
    return Response("Like toggled")

@api_view(["GET"])
def show_similar_videos(request, pk):

    post = get_object_or_404(Post, id=pk)
    relative_posts = Post.objects.filter(categories__id__in=post.categories.all())
    serializer = PostSerializer(relative_posts, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def get_views(request, pk):

    user = request.user
    post = get_object_or_404(Post, id=pk)
    request_views = request.data.get('views')

    if user.is_staff == True and user.is_superuser == True:
        post.views += request_views
        return Response("Views added")
    else:
        return Response("Access denied!", 400)
