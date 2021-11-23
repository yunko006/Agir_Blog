from django.shortcuts import render
from .models import BlogPost, Category

def index(request):

    blog_posts = BlogPost.objects.order_by('-created_on')
    categories = Category.objects.all()
    context = {'blog_posts': blog_posts, 'categories':categories}

    return render(request, 'blog/index.html', context)

def post(request, post_id):

    post = BlogPost.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'blog/post.html', context)

def home(request):

    blog_posts = BlogPost.objects.order_by('created_on')
    context = {'blog_posts': blog_posts}

    return render(request, 'blog/home.html', context)
