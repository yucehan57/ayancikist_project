from django.urls import path
from . import views
from .views import PostListView, CreatePostView, PostDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', PostListView.as_view(), name='blog-view'),
    path('blog/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('blog/addpost', CreatePostView.as_view(), name='add-post'),

]
