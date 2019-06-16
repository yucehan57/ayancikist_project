# Ayancikist

Ayancikist is a blog oriented project that aims to offer users ability
to share blog posts, comment on blog posts, register, and login. Superuser has
ability to both delete and verify comments. Name 'Ayancikist' refers to the town 
I am originally from, Ayancik.

v1 of the project aimed to finish bulk work of the blog app, which is still not
entirely complete, and needs a bit of tweaking.
v2's aim was to be able to offer internet users to register and login with no bugs,
and offer a profile page for every user. A new model (UserProfile) was created to 
be able to have users access profile pages using a slug field which is derived from unique
username of every respective user.

Main goal in v3 is to finish userprofile view and offer authenticated users to post images for
blog posts and comments as well as have users be able to respond to other users' comments

### Requirements

* Python 3.6+
* Django 2.1+

### Installation

Clone the repo, create virtual environment:

    $ git clone https://github.com/yucehan57/ayancikist_project.git
    $ virtualenv env
    $ source/env/bin/activate
    
Environment is set up. To proceed, you begin by making necessary migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate
    
And, run the server:

    $ python manage.py runserver
