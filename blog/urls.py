from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('criando_menu', views.criando_menu, name = 'criando_menu'),
    path('<path:url>', views.my_view, name='my_view'),
    path('<path:url>/', views.my_view, name='my_view'),
    # path('<str:slug_category>/<slug_post>', views.post, name = 'post'),
    # path('<str:slug>/<chapter>', views.livros, name = 'livros'),
    # path('insert/', views.insert, name = 'insert'),

]

