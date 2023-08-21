from django.urls import path
from . import views

urlpatterns = [
    path('catecismo/', views.catechism_index, name = 'index'),
    # path('catecismo/busca/<str:slug>/', views.catechism_search, name = 'catechism_search'),
    path('catecismo/busca/', views.catechism_search, name = 'catechism_search'),
    path('catecismo/<str:slug>/', views.catechism_read, name = 'catechism_read'),
]