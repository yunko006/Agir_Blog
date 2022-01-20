from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models


class Category(models.Model):
    title = models.CharField(max_length=20)
    # foreign key avec rubrique ou inversement pour pouvoir choisir les sous catégories
    # parent = models.ForeignKey(
    #     'self', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title


class Rubrique(models.Model):
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.title


class Rappel(models.Model):
    title = models.CharField(max_length=20)
    content = tinymce_models.HTMLField()

class BlogPost(models.Model):

    class FeaturedPostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(featured=True)

    class StatusPostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    class DraftPostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    redacteur = models.CharField(max_length=50, default="")
    qualite = models.CharField(max_length=50, default="")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    content = tinymce_models.HTMLField()
    created_on = models.DateTimeField(auto_now_add=True)
    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE, default="")
    rubrique = models.ForeignKey(
        Rubrique, on_delete=models.CASCADE, default="")
    status = models.CharField(
        max_length=10, choices=options, default='draft')
    featured = models.BooleanField(default=False)  # rename en main_featured ?
    # savoir si on veux stocker dans db agir.
    stockage = models.BooleanField(default=False)

    # manager
    objects = models.Manager()  # The default manager.
    # Main featured post
    featured_objects = FeaturedPostManager()  # The FeaturedPost manager.
    # custom manager
    postobjects = StatusPostManager()
    # draft post manager
    draftobjects = DraftPostManager()

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.title


class NewsPost(models.Model):

    content = tinymce_models.HTMLField()
