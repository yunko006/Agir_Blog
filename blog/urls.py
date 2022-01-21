from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # home page
    path('', views.index, name='index'),
    # post functions
    path('post/<int:post_id>', views.post, name='post'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    # news
    path('edit_news/<int:news_id>', views.edit_news, name='edit_news'),
    # rappel
    path('edit_rappel/<int:rappel_id>', views.edit_rappel, name='edit_rappel'),
    # coté droit du site
    path('category/<str:cat>', views.caterogy_views, name='category'),
    # # acceder a une sous categorie
    # path('category/<str:cat>/<str:sub_id>', views.rubrique_views, name='rubrique'),
    # draft
    path('draft/', views.index_draft_post, name='draft'),
]
