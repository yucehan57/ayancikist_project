from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog_list, name='blog-view'),
    path('blog/<str:slug>', views.post_detail, name='post-detail'),
    path('blog/addpost/', views.create_post, name='add-post'),
    path('blog/<str:slug>/comment/', views.add_comment_to_post, name='add-comment'),

]
