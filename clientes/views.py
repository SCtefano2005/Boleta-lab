from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from .models import Cliente
from ventas.models import Factura
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                cliente = Cliente.objects.get(email=email)
                if cliente.check_password(password):
                    request.session['cliente_id'] = cliente.id
                    messages.success(request, "Inicio de sesión exitoso.")
                    
                    # Redirigir a la vista de la factura más reciente del cliente
                    factura = Factura.objects.filter(cliente=cliente).order_by('-id').first()
                    if factura:
                        return redirect('factura_view', factura_id=factura.id)
                    else:
                        messages.warning(request, "No tienes facturas disponibles.")
                        return redirect('home')
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
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def logout(request):
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
        messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')

@login_requerido
def factura_view(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    context = {
        'factura': factura,
        'detalles': factura.detalles.all(),
    }
    
    # Comprobar si se ha solicitado generar PDF
    if request.GET.get('pdf'):
        return render_to_pdf('factura.html', context)
    
    return render(request, 'factura.html', context)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF.')
    return response
