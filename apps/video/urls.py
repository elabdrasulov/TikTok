from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
# router.register("videos", PostViewSet)
router.register("categories", CategoryViewSet)
router.register('comment', CommentViewSet)
# router.register("favorites", FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('toggle_like/<int:m_id>/', toggle_like),
    # path('add_rating/<int:m_id>/', add_rating),
    path('videos/create/', PostCreateView.as_view()),
    path('videos/<int:pk>/', PostDetailView.as_view()),
    path('videos/', PostListView.as_view()),
    path('videos/update/<int:pk>/', PostUpdateView.as_view()),
    path('videos/delete/<int:pk>/', PostDeleteView.as_view()),
    path('comments/', CommentListDetailView.as_view()),
    path('comments/<int:pk>/', CommentListDetailView.as_view()),
    path('add_to_favorite/<int:v_id>/', add_to_favorite),
    path('favorites/', FavoriteView.as_view()),
    path('like_post/<int:v_id>/', toggle_post_like),
    path('liked_videos/', LikePostView.as_view()),
    path('like_comment/<int:c_id>/', toggle_comment_like),
    path('show_similar_videos/<int:pk>/', show_similar_videos),
    path('videos/views/<int:pk>/', get_views),
]