from django.urls import path
from campeonatos.views import index, menu_campeonatos
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', menu_campeonatos),
    path('index/', index,name='index')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)