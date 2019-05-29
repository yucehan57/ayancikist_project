from django.shortcuts import render, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    return render(request, 'blog/index.html')

def blog_list(request):
    # filter by published date of the model and paginate list of posts by 3 p/ea
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'posts': paged_listings,
    }
    return render(request, 'blog/posts.html', context)


def post_detail(request, slug):
    # Get request for the Post object is sent using the slug field of the
    # object. '/blog/"what-is-slug"'. Is an example. Then entered slug for the
    # requested object is passed as an argument to the post_detail view so
    # that we can fetch the requested object from the database.
    # get_object_or_404 takes two arguments. One is what object model we need
    # to work with, and the second is the slug of the field.
    # (Rather than post_id field of the Post. In that case following urlpattern
    # would take place:
    #   urlpatterns = ['blog/<int:post_id>', views.post_detail, name='post-detail',]
    #   def post_detail(request, post_id):
    #       post = get_object_or_404(Post, id=post_id)
    # In either case, we would also have to pass the key used in our templates
    # where we have a redirection to a post_detail view. i.e. blog-view (posts.html)
    # <a href="{% url 'post-detail' post.slug %}">{{ post.title }}</a>    OR
    # <a href="{% url 'post-detail' post.id %}">{{ post.title }}</a> if id is used
    # to access the object. Notice post is the object name fetched, and
    # id and slug are fields of the very same object.
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
    }
    template_name = 'blog/post_detail.html'
    return render(request, template_name, context)

@login_required
def create_post(request):
    # How to redirect back to the post created?
    # Isn't it supposed to be done by get_absolute_url?
    # Or, Should I add success_url = reverse_lazy('post-detail')?
    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            # Why do I exactly pass 'request' method here?
            # Is it to save post that is created by the request.POST form above?
            print(post_form.cleaned_data)
            title = post_form.cleaned_data['title'] 
            post = post_form.save(request)
            post.save()
        else:
            print(post_form.errors)
    else:
            # when not POST request, display the empty form
            # meaning -> if request.method=='GET':
            post_form = PostForm()

    context = {
        'post_form': post_form,
    }

    return render(request, 'blog/addpost.html', context)

def add_comment_to_post(request, slug):
    # urlpatterns = ['/blog/<str:slug>/comment', views.add_comment_to_post, name='add-comment',]
    # when there is a get request for, say, '/blog/what-is-slug/comment/',
    # we need to pass the slug as an argument to our view as well so we can
    # fetch the object from our database.
    # def add_comment_to_post(request, slug): --> slug = 'what-is-slug'
    # post = get_object_or_404(Post, slug=slug) --> post.slug = 'what-is-slug'
    # so post variable ends up mapping the Post object where field slug
    # equals argument that is passed over by urlpatterns.
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        # assign filled-out form, which is a POST request the moment end user
        # hits 'add comment' button, to variable name 'form'
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            # comment.post --> post field of comment model.
            # is the purpose of doing the following to create a relation
            # between the comment and the post it is attached to?
            comment.post = post
            comment.save()
            return redirect('post-detail', slug=slug)

    else:
        form = CommentForm()
    template_name = 'blog/add_comment_to_post.html'
    return render(request, template_name , {'form': form })
