from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import Http404

from .models import *
from .forms import *


def must_be_redacteur(user):
    return user.groups.filter(name='redacteur').count() or user.is_superuser


def must_be_correcteur(user):
    return user.groups.filter(name='correcteur').count() or user.is_superuser


def more_than_lecteur(user):
    # check if the user's group is not lecteur
    return not user.groups.filter(name='lecteur').count()


@login_required
def index(request):

    blog_posts = BlogPost.postobjects.order_by('-created_on')

    # donnée pour le coté droit de la page
    news = NewsPost.objects.all()
    rappel_first = Rappel.objects.first()
    rappel_last = Rappel.objects.last()

    # # categories
    # categories = Category.objects.filter(title=category.replace('-', " "))

    # get featured post
    featured_posts = BlogPost.featured_objects.all()
    # first_featured_posts = featured_posts[0]

    # prends que les 2 et 3 featured post pour les mettres sous forme de card dans l'index.html
    # second_third_featured_posts = featured_posts[1:3]
    # uniquement trois post mis en avant.
    trois_featured = featured_posts[:3]

    # pagination
    paginator = Paginator(blog_posts, 5)  # Show X posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # avis count
    avis = AvisDeRecherche.objects.all()

    context = {'news': news, 'rappel_first': rappel_first, 'rappel_last': rappel_last, 'page_obj': page_obj,
               'trois_featured': trois_featured, 'avis': avis}

    return render(request, 'blog/index.html', context)


@login_required
@user_passes_test(more_than_lecteur)
def index_draft_post(request):
    avis = AvisDeRecherche.objects.all()

    if request.user.is_superuser:
        draft_post = BlogPost.draftobjects.order_by('-created_on')

    elif request.user.groups.filter(name='redacteur'):
        draft_post = BlogPost.draftobjects.filter(
            author=request.user).order_by('-created_on')

    elif request.user.groups.filter(name='correcteur'):
        draft_post = BlogPost.draftobjects.order_by('-created_on')

    else:
        raise Http404

    context = {
        'draft_post': draft_post,
        'avis': avis
    }

    return render(request, 'blog/draft.html', context)


@login_required
@user_passes_test(must_be_correcteur)
def index_a_publier_post(request):
    avis = AvisDeRecherche.objects.all()

    if request.user.is_superuser:
        a_publier_post = BlogPost.a_publier_objects.order_by('-created_on')

    elif request.user.groups.filter(name='correcteur'):
        a_publier_post = BlogPost.a_publier_objects.order_by('-created_on')

    else:
        raise Http404

    context = {
        'a_publier_post': a_publier_post,
        "avis": avis
    }

    return render(request, 'blog/a_publier.html', context)


@login_required
def post(request, post_id):

    post = BlogPost.objects.get(id=post_id)
    avis = AvisDeRecherche.objects.all()

    context = {
        'post': post,
        'avis': avis
    }

    return render(request, 'blog/post.html', context)


@login_required
@user_passes_test(more_than_lecteur)
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
@user_passes_test(more_than_lecteur)  # check if user is superuser
def edit_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    content = post.content
    # if superuse can edit all post
    if request.user.is_superuser:
        if request.method != 'POST':

            form = EditPostForm(instance=post)
            # le truc c'est ca check pas en temps réel trouver une autre idée ?
            # form.fields["published"].widget = forms.HiddenInput()
            # print(form.fields["categories"].widget)
            # if form.fields["categories"].widget == 'Missions':

            #     form.fields["rubrique"].widget = forms.ShowInput()

        else:
            form = EditPostForm(instance=post, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect("blog:index")

    # if not usersuper user can only edit their posts
    if is_author(request, post):
        if request.method != 'POST':

            form = EditPostForm(instance=post)
            # hide published field and featured field if not superuser
            form.fields["created_on"].widget = forms.HiddenInput()
            form.fields["published"].widget = forms.HiddenInput()
            form.fields["featured"].widget = forms.HiddenInput()

        else:
            form = EditPostForm(instance=post, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect("blog:index")

    context = {"post": post, 'content': content, 'form': form}

    return render(request, "blog/edit_post.html", context)


@login_required
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


@login_required
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
    # avis
    avis = AvisDeRecherche.objects.all()
    # donnée pour le coté droit de la page
    news = NewsPost.objects.all()
    rappel_first = Rappel.objects.first()
    rappel_last = Rappel.objects.last()

    # pagination a faire plus tard

    context = {
        'cat': cat.replace('-', " "),
        'categories': categories,
        'trois_featured': trois_featured,
        'news': news,
        'rappel_first': rappel_first,
        "rappel_last": rappel_last,
        'avis': avis,
    }

    return render(request, 'blog/category.html', context)


@login_required
def rubrique_views(request, cat, rub_title):

    rubrique_title = BlogPost.postobjects.filter(rubrique__title=rub_title)
    # rubrique_parent = BlogPost.postobjects.filter(rubrique__category=cat)
    # avis
    avis = AvisDeRecherche.objects.all()
    # featured articles
    featured_posts = BlogPost.featured_objects.all()
    # uniquement trois post mis en avant.
    trois_featured = featured_posts[:3]

    # donnée pour le coté droit de la page
    # pas de donnée

    # pagination a faire plus tard

    context = {
        'cat': cat.replace('-', " "),
        'rub_title': rub_title,
        'rubrique_title': rubrique_title,
        'trois_featured': trois_featured,
        'avis': avis
    }

    return render(request, 'blog/rubrique.html', context)


def is_author(request, post):
    if post.author != request.user:
        raise Http404


def index_avis_recherche(request):
    avis = AvisDeRecherche.objects.order_by('-created_on')

    context = {
        "avis": avis
    }

    return render(request, 'blog/index_avis_recherche.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new_avis_recherche(request):
    if request.method != "POST":
        form = AvisDeRechercheForm()

    else:
        form = AvisDeRechercheForm(data=request.POST)
        if form.is_valid():
            new_avis = form.save(commit=False)
            new_avis.save()
            return redirect('blog:index')

    context = {"form": form}

    return render(request, "blog/create_avis_recherche.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_avis_recherche(request, avis_id):
    avis = AvisDeRecherche.objects.get(id=avis_id)
    content = avis.content

    if request.method != 'POST':

        form = AvisDeRechercheForm(instance=avis)

    else:
        form = AvisDeRechercheForm(instance=avis, data=request.POST)

        if form.is_valid():

            form.save()
            return redirect('blog:index_avis')

    context = {"avis": avis, "content": content, "form": form}

    return render(request, 'blog/edit_avis_recherche.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_avis_recherche(request, avis_id):
    avis = AvisDeRecherche.objects.get(id=avis_id)
    content = avis.content

    if request.method == 'POST':
        avis.delete()
        return redirect('blog:index_avis')

    context = {
        "avis": avis
    }

    return render(request, 'blog/delete_avis.html', context)
