from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import Http404

from .models import *
from .forms import *


@login_required
def index(request):

    blog_posts = BlogPost.postobjects.order_by('-created_on')

    # donnée pour le coté droit de la page
    news = NewsPost.objects.all()
    rappel = Rappel.objects.all()

    # # categories
    # categories = Category.objects.filter(title=category.replace('-', " "))

    # get featured post
    featured_posts = BlogPost.featured_objects.all()
    # first_featured_posts = featured_posts[0]

    # prends que les 2 et 3 featured post pour les mettres sous forme de card dans l'index.html
    # second_third_featured_posts = featured_posts[1:3]
    # uniquement trois post mis en avant.
    trois_featured = featured_posts[:3]
    # print(second_third_featured_posts)
    # pagination
    paginator = Paginator(blog_posts, 5)  # Show X posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'news': news, 'rappel': rappel, 'page_obj': page_obj,
               'trois_featured': trois_featured}

    return render(request, 'blog/index.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index_draft_post(request):

    draft_post = BlogPost.draftobjects.order_by('-created_on')

    context = {'draft_post': draft_post}

    return render(request, 'blog/draft.html', context)


@login_required
def post(request, post_id):

    post = BlogPost.objects.get(id=post_id)

    # coté droit du site
    news = NewsPost.objects.all()
    rappel = Rappel.objects.all()

    context = {'post': post, 'news': news, 'rappel': rappel}
    return render(request, 'blog/post.html', context)


@login_required
def new_post(request):
    if request.method != "POST":
        form = PostForm()

    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.save()
            return redirect('blog:index')

    context = {"form": form}

    return render(request, "blog/new_post.html", context)


@login_required
# @user_passes_test(lambda u: u.is_superuser) #check if user is superuser
def edit_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    content = post.content
    is_author(request, post)

    if request.method != 'POST':

        form = EditPostForm(instance=post)

    else:
        form = EditPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("blog:index")

    context = {"post": post, 'content': content, 'form': form}

    return render(request, "blog/edit_post.html", context)


@user_passes_test(lambda u: u.is_superuser)
def delete_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')

    context = {
        "post": post
    }

    return render(request, 'blog/delete_post.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def edit_rappel(request, rappel_id):
    rappel = Rappel.objects.get(id=rappel_id)
    content = rappel.content

    if request.method != 'POST':
        form = EditRappelForm(instance=rappel)

    else:
        form = EditRappelForm(instance=rappel, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('blog:index')

    context = {
        "rappel": rappel,
        "content": content,
        "form": form
    }

    return render(request, 'blog/edit_rappel.html', context)


@login_required
def caterogy_views(request, cat):
    categories = BlogPost.postobjects.filter(
        categories__title=cat.replace('-', " "))

    # featured articles
    featured_posts = BlogPost.featured_objects.all()
    # uniquement trois post mis en avant.
    trois_featured = featured_posts[:3]

    # donnée pour le coté droit de la page
    news = NewsPost.objects.all()
    rappel = Rappel.objects.all()

    # pagination a faire plus tard

    context = {
        'cat': cat.replace('-', " "),
        'categories': categories,
        'trois_featured': trois_featured,
        'news': news,
        'rappel': rappel
    }

    return render(request, 'blog/category.html', context)


@login_required
def rubrique_views(request, rub, sub_id):

    une_rubrique = BlogPost.postobjects.filter(rubrique__title=rub)

    news = NewsPost.objects.all()

    context = {
        'sub_id': sub_id,
        'categories': categories,
        'news': news,
    }

    return render(request, 'blog/rubrique.html', context)


def is_author(request, post):
    if post.author != request.user:
        raise Http404
