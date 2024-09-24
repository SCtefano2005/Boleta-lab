from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import Cliente
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                cliente = Cliente.objects.get(email=email)
                if cliente.check_password(password):  # Verifica la contraseña
                    # Iniciar sesión (puedes utilizar sesiones de Django o un token)
                    request.session['cliente_id'] = cliente.id
                    messages.success(request, "Inicio de sesión exitoso.")
                    return redirect('home')  # Redirige a una vista después de iniciar sesión
                else:
                    messages.error(request, "Contraseña incorrecta.")
            except Cliente.DoesNotExist:
                messages.error(request, "El cliente no existe.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def login_requerido(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('cliente_id'):
            return redirect('login')  # Redirige a login si no está autenticado
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_requerido
def home(request):
    cliente = Cliente.objects.get(id=request.session['cliente_id'])
    return render(request, 'home.html', {'cliente': cliente})

