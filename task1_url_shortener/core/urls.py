from django.contrib import admin
from django.urls import path

from shortener.views import go_to_url, shorten_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shorten/', shorten_url),
    path('<str:code>/', go_to_url),
]