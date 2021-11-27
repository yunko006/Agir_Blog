from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import Http404

from .models import *
from .forms import *


@login_required
def index(request):

    blog_posts = BlogPost.objects.order_by('-created_on')
    categories = Category.objects.all()

    # donnée pour le coté droit de la page
    news = NewsPost.objects.all()

    paginator = Paginator(blog_posts, 5) # Show 5 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'categories':categories, 'news':news, 'page_obj': page_obj}

    return render(request, 'blog/index.html', context)


@login_required
def post(request, post_id):

    post = BlogPost.objects.get(id=post_id)
    news = NewsPost.objects.all()


    context = {'post': post, 'news': news}
    return render(request, 'blog/post.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new_post(request):
    if request.method != "POST":
        form = PostForm()

    else:
        form = PostForm(data=request.POST)
        if form.is_valid():

            form.save()
            return redirect('blog:index')

    context = {"form": form}

    return render(request, "blog/new_post.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser) #check if user is superuser
def edit_post(request, post_id):
    pass


@login_required
@user_passes_test(lambda u:u.is_superuser)
def edit_news(request, news_id):
    news = NewsPost.objects.get(id=news_id)
    content = news.content

    if request.method != 'POST':

        form = NewsForm(instance=news)

    else:
        form = NewsForm(instance=news, data=request.POST)

        if form.is_valid():

            form.save()
            return redirect('blog:index')

    context = {"news": news, "content": content, "form": form}

    return render(request, 'blog/edit_news.html', context)


def is_author(request, post):
    if post.author != request.user:
        raise Http404
