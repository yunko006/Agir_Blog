from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class BlogPost(models.Model):

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

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.title
