from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.
def menuPrincipal(request):
    return render(request, 'home.html', {

    } )

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                user.last_login = timezone.now()
                return redirect('sesion')
            else:
                return HttpResponse('Contraseña incorrecta')
        except User.DoesNotExist:
            return HttpResponse('Usuario no existe')
    else:
        return render(request, 'login.html', {})

def cabecera(request):
    return render(request, 'cabecera.html', {

    })

def formulario(request):
    if request.method == 'GET':
        return render(request, 'formulario.html', {
            'form': UserCreationForm()
        })
    else:
        # Verificamos si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crear el usuario con nombre de usuario, correo y contraseña
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                user.last_login = timezone.now()
                user.save()
                return redirect('sesion')
            except Exception as e:
                # Si ocurre un error (por ejemplo, el usuario ya existe)
                return render(request, 'formulario.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario o correo ya existe'
                })
        else:
            # Si las contraseñas no coinciden
            return render(request, 'formulario.html', {
                'form': UserCreationForm(),
                'error': 'Las contraseñas no coinciden'
            })
    
def sesion(request):
    return render(request, 'sesion.html')