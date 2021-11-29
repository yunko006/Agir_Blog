from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title



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
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    content = tinymce_models.HTMLField()
    created_on = models.DateTimeField(auto_now_add=True)
    # updated_on
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=10, choices=options, default=created_on)
    featured = models.BooleanField(default=False) # rename en main_featured ?

    # manager
    objects = models.Manager() # The default manager.
    # Main featured post
    featured_objects = FeaturedPostManager() # The FeaturedPost manager.
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

