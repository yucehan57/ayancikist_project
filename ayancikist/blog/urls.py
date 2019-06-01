from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog_list, name='blog-view'),
    path('blog/<str:slug>', views.post_detail, name='post-detail'),
    path('blog/<str:slug>/delete', views.delete_post, name='delete-post'),
    path('blog/<str:slug>/edit', views.edit_post, name='edit-post'),
    path('blog/addpost/', views.create_post, name='add-post'),
    path('blog/<str:slug>/comment/', views.add_comment_to_post, name='add-comment'),
    path('comment/<int:pk>/approve/', views.approve_comment, name='approve-comment'),
    # path('comment<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    path('blog/<str:slug>/comment/edit/', views.edit_post_comment, name='edit-comment'),

]
