from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView

#ALTERAR SEMPRE O OUTRO URLS QUANDO NECESSARIO ACRESCENTAR ALGUM URLS


urlpatterns = [
    path("", RedirectView.as_view(url='/caderneta/', permanent=True)),
    path('caderneta/', include('caderneta.urls')),
    path('admin/', admin.site.urls),

]