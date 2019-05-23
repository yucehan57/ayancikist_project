from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post
from django.utils import timezone
from django.views.generic import ListView, DetailView

def index(request):
    # List published posts on home page
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'

    def get_queryset(self):
        # Filter by 'published_date' field of Post model
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

class PostDetailView(DetailView):
    model = Post
