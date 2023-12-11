from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('biblia/', include('bible.urls')),
    path('search/', include('search.urls')),
    path('docs/', include('documents.urls')),
    path('', include('blog.urls')),

    #  path('', include('plataforma.urls')),
]