from django.urls import path
from . import views

urlpatterns = [
    path('', views.bible_index, name = 'bible_index'),
    path('<str:slug>/<chapter>', views.bible_read, name = 'bible_read'),
    path('update/', views.bible_update, name = 'bible_update'),
    path('busca/', views.bible_search, name = 'bible_search'),
    # path('catecismo/busca/<str:slug>/', views.catechism_search, name = 'catechism_search'),
]