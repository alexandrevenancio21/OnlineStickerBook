import os
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .utils import processar_compra_pacote
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *


def homepage(request):
    return render(request, 'caderneta/homepage.html')
@login_required(login_url='/caderneta/login_user')
def forum(request):
    mensagem_list = Mensagem.objects.all().order_by('-pub_data')
    if request.user.is_superuser:
        return render(request, 'caderneta/forum.html', {'mensagem_list': mensagem_list})

    utilizador = request.user.utilizador
    mensagem_like = []
    for mensagem in mensagem_list:
        if Like.objects.filter(mensagem=mensagem, user=utilizador).exists():
            mensagem_like.append(mensagem)


    return render(request, 'caderneta/forum.html', {'mensagem_list': mensagem_list, 'mensagem_like': mensagem_like})

@login_required(login_url='/caderneta/login_user')
def caderneta(request):
    utilizador = request.user.utilizador
    caderneta = Caderneta.objects.filter(utilizador=utilizador).order_by('cromo_id')
    n_cromos = caderneta.count()
    return render(request, 'caderneta/caderneta.html', {'caderneta': caderneta, 'n_cromos': n_cromos})

@login_required(login_url='/caderneta/login_user')
def loja(request):
    pacote_list = Pacote.objects.all()
    if request.user.is_superuser:
        return render(request, 'caderneta/loja.html', {'pacote_list': pacote_list})

    utilizador = Utilizador.objects.get(user=request.user)
    return render(request, 'caderneta/loja.html', {'pacote_list': pacote_list, 'utilizador': utilizador})

def cromos_pacote(request, pacote_id):
    cromos = list(Cromo.objects.all())

    pacote = Pacote.objects.get(id=pacote_id)

    quantidade_cromos = pacote.qnt_cromos

    cromos_aleatorios = random.sample(cromos, k=quantidade_cromos)

    utilizador_id = request.user.utilizador.id
    cromos_utilizador = [caderneta.cromo for caderneta in Caderneta.objects.filter(utilizador_id=utilizador_id)]


    processar_compra_pacote(utilizador_id, pacote_id, cromos_aleatorios)

    return render(request, 'caderneta/cromos_pacote.html', {'cromos_aleatorios': cromos_aleatorios, 'cromos_utilizador': cromos_utilizador})

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dt_of_birth = request.POST.get('data_nascimento')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já está em uso. Por favor, faça Login.')
            return render(request, 'caderneta/login.html')

        if User.objects.filter(username=username).values().exists():
            messages.error(request, 'Username ocupado. Por favor, escolha outro.')
            return render(request, 'caderneta/sign-up.html')

        user = User.objects.create_user(username, email, password)
        u = Utilizador(user=user, data_nascimento=dt_of_birth)

        u.save()

        login(request, user)
        return HttpResponseRedirect(reverse('caderneta:homepage'))

    return render(request, 'caderneta/sign-up.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('caderneta:homepage'))
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
            return render(request, 'caderneta/login.html')

    return render(request, 'caderneta/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Você saiu com sucesso. Obrigado por usar nosso sistema!')
    return HttpResponseRedirect(reverse('caderneta:homepage'))

def info_user(request):
    utilizador = Utilizador.objects.get(user=request.user)
    caderneta = Caderneta.objects.filter(utilizador=utilizador).order_by('cromo_id')
    n_cromos = caderneta.count()
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        name, extension = os.path.splitext((myfile.name))
        filename = f'{request.user.username}_profile{extension}'

        if fs.exists(filename):
            fs.delete(filename)

        fs.save(filename, myfile)

        request.user.utilizador.imagem = filename
        request.user.utilizador.save()

        messages.success(request, 'Imagem adicionada com sucesso')
        return HttpResponseRedirect(reverse('caderneta:info_user'))

    return render(request,'caderneta/info.html', {'utilizador': utilizador, 'n_cromos': n_cromos})

def load_image(request):
    fs = FileSystemStorage()
    avatar = '/static/media/default_image.jpg'
    if request.user.utilizador.imagem != '/media/default_image.jpg' and fs.exists(request.user.utilizador.imagem):
        avatar = '/static/media/' + request.user.utilizador.imagem
    return redirect(avatar)

def add_saldo(request):
    if request.method == 'POST':
        saldo_adicionar = request.POST.get('add_saldo')
        saldo_adicionar = float(saldo_adicionar)

        utilizador = Utilizador.objects.get(user=request.user)
        utilizador.saldo += saldo_adicionar
        utilizador.save()
        messages.success(request, f' {saldo_adicionar} € adicionados com sucesso.')
        return HttpResponseRedirect(reverse('caderneta:info_user'))
    return render(request, 'caderneta/add_saldo.html')

def criar_mensagem(request):
        texto_mensagem = request.POST['mensagem_texto']
        user = request.user.utilizador
        mensagem = Mensagem(user=user, mensagem_texto=texto_mensagem, pub_data=timezone.now())
        mensagem.save()
        return HttpResponseRedirect(reverse('caderneta:forum'))

def like_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)

    if request.user.is_superuser:
        return redirect('caderneta:forum')
    utilizador = Utilizador.objects.get(user=request.user)
    try:
        # Tenta obter o like do usuário para esta mensagem
        like = Like.objects.get(mensagem=mensagem, user=utilizador)
        # Se o like existir, isso significa que o usuário já deu like
        # Portanto, remove o like da mensagem e subtrai 1 ao contador de likes
        like.delete()
        mensagem.n_likes -= 1
    except Like.DoesNotExist:
        # Se o like não existir, isso significa que o usuário ainda não deu like
        # Portanto, crie um novo like para a mensagem e soma 1 no contador de likes
        Like.objects.create(mensagem=mensagem, user=utilizador)
        mensagem.n_likes += 1
    # Dá save à mensagem para atualizar as alterações feitas
    mensagem.save()
    return redirect('caderneta:forum')

def delete_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    mensagem.delete()
    return redirect('caderneta:forum')

def foto_msg(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    user = mensagem.user
    avatar = '/static/media/default_image.jpg'
    if mensagem.user.imagem != '/media/default_image.jpg':
        avatar = '/static/media/' + user.imagem
    return redirect(avatar)

def colar_caderneta(request):
    return redirect('caderneta:caderneta')

@api_view(['GET', 'POST'])
def criar_pacote(request):
    if request.method == 'POST':
        print("teste" + str(request.data))
        serializer = PacoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def apagar_pacote_2(request):
    if request.method == 'POST':
        pacote_id = request.POST.get('pacote_id')
        if pacote_id:
            try:
                pacote = Pacote.objects.get(id=pacote_id)
                pacote.delete()
            except Pacote.DoesNotExist:
                messages.success(request, f'O pacote com o id {pacote_id} não existe')
                return redirect('caderneta:loja')
    return redirect('caderneta:loja')