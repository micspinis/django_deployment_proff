from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm


# New imports to use in login page
from django.contrib.auth import  authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('You are Logged in, Nice!!')

## Funcion para salir de sesion
##Usamo el decorador para saber que solo se usara esta funcion si estamos logeados
## esto es que primero debe correrse esa funcion para que esta actue.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))    

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                print('Found it')
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', 
                    {'user_form':user_form, 
                    'profile_form':profile_form,
                    'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # Obtenemos de la db el nombre de usuario y contraseña
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Validamos el usuario y contraseña con uno de los modulos que importamos
        user = authenticate(username=username, password=password)


        #Si pasa la validacion
        if user:
            #Nos logeamos
            if user.is_active:
                #Para terminar el login usamos el modulo que importamos
                login(request, user)

                ## Una vez que nos logeamos, no redirigimos a otra pagina
                ## para eso usamos HttpResponseRedirect
                return HttpResponseRedirect(reverse('index')) #Nos redirigimos al index page
            else:
                return HttpResponse('Account Not Active')
        else:
            return HttpResponse('Invalid Login Details supplied!')
    else:
        return render(request, 'basic_app/login.html', {})
