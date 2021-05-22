from django.urls import path
from . import views as blog_views


urlpatterns = [
    path('', blog_views.PostListView.as_view(), name='blog-home'),
    path('posts_by_likes', blog_views.PostListViewByLikes.as_view(), name='blog-home2'),
    path('user/<str:username>', blog_views.UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', blog_views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', blog_views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', blog_views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', blog_views.PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>', blog_views.like_detail_view, name='like_detail_view'),
    path('likes/<int:pk>', blog_views.like_list_view, name='like_list_view'),
]
