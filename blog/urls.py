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
    path('category/<str:cat>/<str:rub_title>',
         views.rubrique_views, name='rubrique'),
    # draft
    path('draft/', views.index_draft_post, name='draft'),
    path('publication/', views.index_a_publier_post, name='publication'),
    # avis de recherche
    path('new_avis/', views.new_avis_recherche, name='new_avis'),
    path('index_avis/', views.index_avis_recherche, name='index_avis'),
    path('index_porteur/', views.index_porteur_recherche, name='index_porteur'),
    path('index_avis_archivés/', views.index_avis_recherche_archiver, name='index_avis_archiver'),
    path('edit_avis/<int:avis_id>', views.edit_avis_recherche, name='edit_avis'),
    path('delete_avis/<int:avis_id>',
         views.delete_avis_recherche, name='delete_avis'),
]
