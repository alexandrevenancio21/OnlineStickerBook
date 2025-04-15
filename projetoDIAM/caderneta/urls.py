from django.urls import include, path
from . import views
from django.conf import settings  

app_name = 'caderneta'

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('create_user', views.create_user, name='create_user'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('info_user', views.info_user, name='info_user'),
    path('add_saldo', views.add_saldo, name='add_saldo'),
    path('loja', views.loja, name='loja'),
    path('caderneta', views.caderneta, name='caderneta'),
    path('forum', views.forum, name='forum'),
    path('cromos_pacote/<int:pacote_id>', views.cromos_pacote, name='cromos_pacote'),
    path('load_image', views.load_image, name='load_image'),
    path('criar_mensagem', views.criar_mensagem, name='criar_mensagem'),
    path('like_mensagem/<int:mensagem_id>', views.like_mensagem, name='like_mensagem'),
    path('delete_mensagem/<int:mensagem_id>', views.delete_mensagem, name='delete_mensagem'),
    path('foto_msg/<int:mensagem_id>', views.foto_msg, name='foto_msg'),
    path('colar_caderneta', views.colar_caderneta, name='colar_caderneta'),
    path('apagar_pacote_2', views.apagar_pacote_2, name='apagar_pacote_2'),

    path('api/criar_pacote/', views.criar_pacote),#react
]