from django.shortcuts import render, get_object_or_404

def index(request, slug):
    # navbar 'logged in as {{}}' should be modified.
    userprofile = get_object_or_404(UserProfile, slug=slug)
    # Query user's posts
    posts = userprofile.user.posts.all()
    context = {
        'posts': posts,
        'user': userprofile,
    }
    return render(request, 'userprofile/userprofile.html', context)
