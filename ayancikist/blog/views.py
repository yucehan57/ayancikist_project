from django.shortcuts import render, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm, PostUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    return render(request, 'blog/index.html')

def blog_list(request):
    # filter by published date of the model and paginate list of posts by 3 p/ea
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)
    context = {
        'posts': paged_posts,
    }
    return render(request, 'blog/posts.html', context)


def post_detail(request, slug):
    # Get request for the Post object is sent using the slug field of the
    # object. '/blog/"what-is-slug"' is an example. Then entered slug for the
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
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            # Why do I exactly pass 'request' method here?
            # Is it to save post that is created by the request.POST form above?
            # P.S. next line used to read post = post_form.save(request)
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            slug = post.slug
            return redirect('post-detail', slug=slug)
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
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', slug=slug)

    else:
        form = CommentForm()
    template_name = 'blog/add_comment_to_post.html'
    context = {
        'form': form,
    }
    return render(request, template_name , context)


def delete_post(request, slug):
    # Maybe have template for: "Sure you want to delete?"
    # 'blog/delete_post_confirm.html'
    post = get_object_or_404(Post, slug=slug)
    # Should this logic stay here?
    if request.user == post.user:
        post.delete()
        return redirect('blog-view')
        template_name = 'blog/delete_post.html'
        return HttpResponseRedirect('Deleted')
    else:
        return HttpResponse('You must be authorized to delete this post')

@login_required
def edit_post(request, slug):
    # How to tell front end that an edit took place
    # and record the time of edit. So that I could have a field
    # on the front end stating, i.e., edited: May 31, 2019 - 6:48pm

    # get the original post
    original_post = get_object_or_404(Post, slug=slug)
    # if user requesting the edit is the post author:
    if request.user == original_post.user:
        # if user filled out the form and pressed submit:
        if request.method == 'POST':
            edit_form = PostUpdateForm(request.POST)
            # request.POST returns a Query Dictionary
            # so that we can grab the values using the key
            # and assign values to variables
            edited_title = request.POST['title']
            edited_text  = request.POST['text']
            print(request.POST)
            if edit_form.is_valid():
                # original_post = edit_form.save(commit=False)
                original_post.user  = request.user
                original_post.title = edited_title
                original_post.text  = edited_text
                original_post.save()
                # original_post.delete()
                # redirect to edited post detail
                # when title is updated, will slug change automatically?
                # or do I need to handle it at save?
                # Answered: Yes, it is automatically handled on the back end.
                slug = original_post.slug
                print(slug)
                print(original_post._meta.get_fields())
                return redirect('post-detail', slug=slug)

        else:
            edit_form = PostUpdateForm()
    else:
        return HttpResponse('You are not authorized to perform this action')
    template_name = 'blog/edit_post.html'
    context = {
        'edit_form': edit_form,
        'original_post': original_post,
    }
    return render(request, template_name, context)


def edit_post_comment(request, slug):
    # grab the post the comment belongs to
    post = get_object_or_404(Post, slug=slug)
    # comment time will change, affecting the order of the
    # comments. Have superuser be able to approve, delete
    # all the comments. when deleted by superuser, maybe say:
    # "deleted because of <edit reason>"
    # since there has to be a user for every comment and post,
    # just like we did above functions, we need to specify:
    # post.user = request.user and/or comment.user = request.user
    # this we do, because we don't pass 'user' field in forms (Comment or Post)
    pass

def add_comment_to_comment(request, slug):
    # comment.user = request.user
    # comment.post = post
    pass

@login_required
def approve_comment(self, pk):
    # grab the comment object by its pk field
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve_comment()
    return redirect('post-detail', slug=comment.post.slug)


def delete_comment(self, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', slug=comment.post.slug)
