from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Post, Comment
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    # List published posts on home page
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)


def blog_list(request):
    # filter by published date of the model
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'posts': paged_listings,
    }
    return render(request, 'blog/posts.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(request)
            post.save()
        else:
            print(post_form.errors)
    else:
            post_form = PostForm()

    context = {
        'post_form': post_form,
    }

    return render(request, 'blog/addpost.html', context )

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=pk)

    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form,
                                                             })
