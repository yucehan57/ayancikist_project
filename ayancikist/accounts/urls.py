from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    # 'profile/<str:slug> to go users profile'
    # slug to be username that is unique.
    path('profile/<int:user_id>', views.profile, name='profile'),

]
