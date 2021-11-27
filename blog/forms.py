from django import forms
# from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

from .models import BlogPost, NewsPost


class PostForm(forms.ModelForm):
    # content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = BlogPost
        fields = ['author', 'title', 'description', 'content', 'categories', 'status', 'featured']
        labels = {"author":"Auteur","title": "Titre de l'article", "description":"Description de l'article", "content":"Ecrire votre article"}


class NewsForm(forms.ModelForm):

    class Meta:
        model = NewsPost
        fields = ['content']
        labels = {"content": "Texte"}
