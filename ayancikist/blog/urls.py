from django.urls import path
from . import views
from .views import PostListView
urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', PostListView.as_view(), name='blog-view'),
    path('blog/<int:pk>', views.post_detail, name='post-detail'),
    path('blog/addpost', views.create_post, name='add-post'),
    path('blog/<int:pk>/comment/', views.add_comment_to_post, name='add-comment'),

]
