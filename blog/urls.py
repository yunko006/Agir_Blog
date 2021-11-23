from django.urls import path
from . import views

app_name = 'blog'

urlpatterns= [
    # home page
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('post/<int:post_id>', views.post, name='post'),
]
