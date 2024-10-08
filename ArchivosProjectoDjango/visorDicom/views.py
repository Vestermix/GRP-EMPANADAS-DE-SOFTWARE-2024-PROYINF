from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
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
                return HttpResponse('Login exitoso')
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
        } )
    else:
        if request.POST['password1'] == request.POST['password1']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                return HttpResponse('Usuario creado')
            except:
                return render(request, 'formulario.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario ya existe'	
                })
        return render(request, 'formulario.html', {
            'form': UserCreationForm(),
            'error': 'la contraseña no coincide'	
        })