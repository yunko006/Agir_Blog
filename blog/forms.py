from django import forms
from .models import BlogPost


class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = {'author', 'title', 'description', 'content', 'categories', 'status'}
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80})
        }
