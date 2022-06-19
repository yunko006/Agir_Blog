from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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
            return super().get_queryset().filter(published=True, featured=False)

    class DraftPostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft', published=False)

    class EditPostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='edit', published=False)

    class SuspenduPostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='suspendu', published=False)

    options = (
        ('draft', 'Brouillon'),
        ('edit', 'A publier'),
        ('suspendu', 'Parution Suspendu'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    redacteur = models.CharField(max_length=50, default="")
    qualite = models.CharField(max_length=50, default="")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    content = tinymce_models.HTMLField()
    created_on = models.DateTimeField(default=timezone.now)
    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE, default="")
    rubrique = models.ForeignKey(
        Rubrique, on_delete=models.CASCADE, default="")
    status = models.CharField(
        max_length=10, choices=options, default='draft')
    published = models.BooleanField(default=False)
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
    # a publier manager
    a_publier_objects = EditPostManager()

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.title


class NewsPost(models.Model):
    title = models.CharField(max_length=20, default="")
    content = tinymce_models.HTMLField()


class AvisDeRecherche(models.Model):

    class NotArchivedIntervenantManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(archiver=False, status='intervenant')

    class NotArchivedPorteurManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(archiver=False, status='porteur')

    class ArchivedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(archiver=True)

    options = (
        ('intervenant', 'Intervenant'),
        ('porteur', 'Porteur Projet'),
    )

    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()
    created_on = models.DateTimeField(default=timezone.now)
    archiver = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=options, default='intervenant')

    # default manager
    objects = models.Manager()
    # manager if not archiver and status = intervenant
    pas_archiver_object = NotArchivedIntervenantManager()
    # manager if pas archiver and status = porteur
    pas_archiver_porteur = NotArchivedPorteurManager()
    # manager if archiver
    archiver_object = ArchivedManager()

    def __str__(self):
        return self.title
