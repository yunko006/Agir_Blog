from django.urls import path
from . import views

app_name = 'blog'

urlpatterns= [
    # home page
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post, name='post'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_news/<int:news_id>', views.edit_news, name='edit_news'),
]
