from django import forms
from .models import Post, Comment

# when to use forms.Form and forms.ModelForm?
# forms.Form -> when DB is not to be directly impacted (Contact Form)
# forms.ModelForm -> when DB is directly impacted (User Registration )

class PostForm(forms.ModelForm):
    # A form to have users add posts using post.user, post.title, and post.text
    # fields of the Post model
    # How would I be able to use the signed in user to add posts without
    # having to ask on front-end what user will be the author of the post
    # How do I by default assign the user(author) as authenticated user?
    class Meta:
        model = Post
        exclude = ('user', 'slug', 'image')

class CommentForm(forms.ModelForm):
    # A form to leave comments for posts.
    # Same question as above, how do I bypass the need to pass 'user' field
    # and comment as either anonymous when not authenticated, and logged in
    # user when authenticated rather than giving end user the right to choose.
    class Meta:
        model = Comment
        fields = ('text',)


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'slug', 'image')

# class AnanymousCommentForm(forms.ModelForm):
#     # Commenting when not logged in will ask for a nickname
#     class Meta:
#         model = Comment
#         fields = ('user', 'text',)
