from django.urls import path
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', PostListView.as_view(), name='blog-view'),

]
