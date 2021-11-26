from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def index(request):

    blog_posts = BlogPost.objects.order_by('-created_on')
    categories = Category.objects.all()

    # donnée pour le coté droit de la page
    news = NewsPost.objects.all()

    context = {'blog_posts': blog_posts, 'categories':categories, 'news':news}

    return render(request, 'blog/index.html', context)



@login_required
def post(request, post_id):

    post = BlogPost.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'blog/post.html', context)
