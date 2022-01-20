from django import forms
from tinymce.widgets import TinyMCE

from .models import BlogPost, NewsPost, Rappel


class PostForm(forms.ModelForm):
    # content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = BlogPost
        fields = ['redacteur', 'qualite', 'title',
                  'content', 'categories', 'rubrique', 'stockage']
        labels = {
            "redacteur": "Nom et Prénom",
            "qualite": "Qualité",
            "title": "Titre de l'article",
            "description": "Description de l'article",
            "content": "Ecrire votre article"
        }


class EditPostForm(forms.ModelForm):
    # content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = BlogPost
        fields = ['redacteur', 'qualite', 'title',
                  'content', 'categories', 'rubrique', 'status', 'featured', 'stockage']
        labels = {
            "redacteur": "Nom et Prénom",
            "qualite": "Qualité",
            "title": "Titre de l'article",
            "description": "Description de l'article",
            "content": "Ecrire votre article"
        }


class NewsForm(forms.ModelForm):

    class Meta:
        model = NewsPost
        fields = ['content']
        # labels = {"content": "Texte"}


class EditRappelForm(forms.ModelForm):

    class Meta:
        model = Rappel
        fields = ['title', 'content']
