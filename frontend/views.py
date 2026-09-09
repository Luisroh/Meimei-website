# frontend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.utils import timezone as tz
from datetime import timedelta
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from .forms import ContactoForm
from .models import MensajeContacto, Servicio, ImagenGaleria
import datetime
import requests

def validar_captcha(token):
    """Valida el token de reCAPTCHA v3 con Google"""
    secret = settings.RECAPTCHA_SECRET_KEY
    
    if not secret:
        # Si no hay clave secreta, no validamos (solo en desarrollo)
        return True
    
    payload = {
        'secret': secret,
        'response': token,
    }
    
    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = response.json()
        
        # V3 devuelve un score entre 0.0 y 1.0
        # 0.5 o más = probable humano
        score = result.get('score', 0)
        return score >= 0.5 and result.get('success', False)
        
    except Exception as e:
        print(f"Error al verificar CAPTCHA: {e}")
        # En caso de error, permitimos el envío (para no bloquear a usuarios reales)
        return True

def contacto(request):
    
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        
        # ✅ VALIDAR CAPTCHA
        captcha_token = request.POST.get('g-recaptcha-response', '')
        captcha_valido = validar_captcha(captcha_token)
        
        if not captcha_valido:
            messages.error(request, 'No pudimos verificar que eres humano. Por favor, intenta de nuevo.')
            return render(request, 'frontend/contacto.html', {'form': form})
        
        # ✅ RATE LIMITING MANUAL
        if 'last_submit_time' in request.session:
            last_submit_str = request.session['last_submit_time']
            last_submit = datetime.datetime.fromisoformat(last_submit_str)
            now = tz.now()
            time_diff = now - last_submit
            
            if time_diff < datetime.timedelta(minutes=1):
                submit_count = request.session.get('submit_count', 0)
                if submit_count >= 3:
                    messages.error(request, 'Has enviado demasiados mensajes. Espera un momento.')
                    return render(request, 'frontend/contacto.html', {'form': form})
                
                request.session['submit_count'] = submit_count + 1
            else:
                request.session['submit_count'] = 1
        else:
            request.session['submit_count'] = 1
        
        # Guardar timestamp como string ISO
        request.session['last_submit_time'] = tz.now().isoformat()
        
        # ✅ PROCESAR FORMULARIO
        if form.is_valid():
            # Verificar duplicado
            nombre = form.cleaned_data.get('nombre')
            email = form.cleaned_data.get('email')
            mensaje_texto = form.cleaned_data.get('mensaje')
            
            tiempo_limite = tz.now() - datetime.timedelta(minutes=5)
            duplicado = MensajeContacto.objects.filter(
                nombre=nombre,
                email=email,
                mensaje=mensaje_texto,
                fecha_envio__gte=tiempo_limite
            ).exists()
            
            if duplicado:
                messages.warning(request, 'Ya hemos recibido tu mensaje. Te responderemos pronto. 💖')
                return redirect('frontend:contacto')
            
            # Guardar mensaje
            mensaje = form.save()
            
            # Enviar email
            try:
                enviar_email_contacto(mensaje)
                messages.success(request, '¡Mensaje enviado con éxito! Te contactaremos pronto. 💖')
            except Exception as e:
                messages.error(request, 'Hubo un error al enviar el mensaje. Por favor, intenta de nuevo.')
                print(f"Error al enviar email: {e}")
            
            return redirect('frontend:contacto')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ContactoForm()
    
    return render(request, 'frontend/contacto.html', {'form': form})

def home(request):
    servicios_destacados = Servicio.objects.filter(activo=True).order_by('orden')[:4]
    context = {
        'servicios_destacados': servicios_destacados,
    }
    return render(request, 'frontend/home.html', context)

def quienes_somos(request):
    return render(request, 'frontend/quienes_somos.html')

def masajes(request):
    return render(request, 'frontend/masajes.html')

def peluqueria(request):
    return render(request, 'frontend/peluqueria.html')

def galeria(request):
    return render(request, 'frontend/galeria.html')

def contacto(request):
    
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        
        # ✅ RATE LIMITING MANUAL
        if 'last_submit_time' in request.session:
            last_submit_str = request.session['last_submit_time']
            last_submit = datetime.fromisoformat(last_submit_str)
            now = tz.now()
            time_diff = now - last_submit
            
            if time_diff < timedelta(minutes=1):
                submit_count = request.session.get('submit_count', 0)
                if submit_count >= 3:
                    messages.error(request, 'Has enviado demasiados mensajes. Espera un momento.')
                    return render(request, 'frontend/contacto.html', {'form': form})
                
                request.session['submit_count'] = submit_count + 1
            else:
                request.session['submit_count'] = 1
        else:
            request.session['submit_count'] = 1
        
        # Guardar timestamp como string ISO
        request.session['last_submit_time'] = tz.now().isoformat()
        
        # ✅ PROCESAR FORMULARIO
        if form.is_valid():
            # Verificar duplicado
            nombre = form.cleaned_data.get('nombre')
            email = form.cleaned_data.get('email')
            mensaje_texto = form.cleaned_data.get('mensaje')
            
            tiempo_limite = tz.now() - timedelta(minutes=5)
            duplicado = MensajeContacto.objects.filter(
                nombre=nombre,
                email=email,
                mensaje=mensaje_texto,
                fecha_envio__gte=tiempo_limite
            ).exists()
            
            if duplicado:
                messages.warning(request, 'Ya hemos recibido tu mensaje. Te responderemos pronto. 💖')
                return redirect('frontend:contacto')
            
            # Guardar mensaje
            mensaje = form.save()
            
            # Enviar email
            try:
                enviar_email_contacto(mensaje)
                messages.success(request, '¡Mensaje enviado con éxito! Te contactaremos pronto. 💖')
            except Exception as e:
                messages.error(request, 'Hubo un error al enviar el mensaje. Por favor, intenta de nuevo.')
                print(f"Error al enviar email: {e}")
            
            return redirect('frontend:contacto')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ContactoForm()
    
    return render(request, 'frontend/contacto.html', {'form': form})

def enviar_email_contacto(mensaje):

    """Envía un email con los datos del formulario de contacto"""
    
    # Asunto del email
    subject = f"Nuevo mensaje de contacto - Meimei Estética - {mensaje.nombre}"
    
    # Mensaje para el administrador (email)
    admin_message = render_to_string('frontend/emails/contacto_admin.html', {
        'nombre': mensaje.nombre,
        'email': mensaje.email,
        'telefono': mensaje.telefono or 'No especificado',
        'servicio': mensaje.get_servicio_display() or 'No especificado',
        'mensaje': mensaje.mensaje,
        'fecha': mensaje.fecha_envio.strftime('%d/%m/%Y %H:%M'),
    })
    
    # Mensaje para el cliente (confirmación)
    client_message = render_to_string('frontend/emails/contacto_cliente.html', {
        'nombre': mensaje.nombre,
    })
    
    # Email para el administrador
    email_admin = EmailMessage(
        subject=subject,
        body=admin_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_EMAIL] if hasattr(settings, 'CONTACT_EMAIL') else [settings.DEFAULT_FROM_EMAIL],
        reply_to=[mensaje.email],
    )
    email_admin.content_subtype = 'html'
    email_admin.send(fail_silently=False)
    
    # Email de confirmación para el cliente
    email_cliente = EmailMessage(
        subject="¡Gracias por contactar con Meimei Estética!",
        body=client_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[mensaje.email],
    )
    email_cliente.content_subtype = 'html'
    email_cliente.send(fail_silently=False)

@staff_member_required
def panel_mensajes(request):
    """Panel para que tu madre vea los mensajes de contacto"""
    
    # Obtener todos los mensajes
    mensajes = MensajeContacto.objects.all().order_by('-fecha_envio')
    
    # Contadores
    total = mensajes.count()
    no_leidos = mensajes.filter(leido=False).count()
    no_respondidos = mensajes.filter(respondido=False).count()
    
    # Paginación
    paginator = Paginator(mensajes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total': total,
        'no_leidos': no_leidos,
        'no_respondidos': no_respondidos,
    }
    
    return render(request, 'frontend/panel_mensajes.html', context)

@staff_member_required
def enviar_respuesta(request, mensaje_id):
    """Envía una respuesta al cliente y la guarda en la base de datos"""
    mensaje = get_object_or_404(MensajeContacto, id=mensaje_id)
    
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta', '').strip()
        
        if respuesta:
            # Guardar respuesta en la base de datos
            mensaje.respuesta = respuesta
            mensaje.fecha_respuesta = tz.now()
            mensaje.respondido = True
            mensaje.leido = True
            mensaje.save()
            
            # Enviar email al cliente
            try:
                # Email en HTML
                from django.template.loader import render_to_string
                from django.core.mail import EmailMessage
                
                html_message = render_to_string('frontend/emails/respuesta_cliente.html', {
                    'nombre': mensaje.nombre,
                    'respuesta': respuesta,
                    'mensaje_original': mensaje.mensaje,
                })
                
                email = EmailMessage(
                    subject=f'Respuesta a tu mensaje - Meimei Estética',
                    body=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[mensaje.email],
                )
                email.content_subtype = 'html'
                email.send(fail_silently=False)
                
                messages.success(request, f'✅ Respuesta enviada a {mensaje.nombre}')
            except Exception as e:
                messages.error(request, f'❌ Error al enviar el email: {e}')
        else:
            messages.error(request, 'Por favor, escribe un mensaje antes de enviar.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/panel/mensajes/'))

@staff_member_required
def marcar_leido(request, mensaje_id):
    """Marca un mensaje como leído o no leído"""
    mensaje = get_object_or_404(MensajeContacto, id=mensaje_id)
    mensaje.leido = not mensaje.leido
    mensaje.save()
    return redirect('frontend:panel_mensajes')

def masajes(request):
    servicios = Servicio.objects.filter(categoria='masaje', activo=True).order_by('orden')
    context = {
        'servicios': servicios,
    }
    return render(request, 'frontend/masajes.html', context)

def peluqueria(request):
    servicios = Servicio.objects.filter(categoria='peluqueria', activo=True).order_by('orden')
    context = {
        'servicios': servicios,
    }
    return render(request, 'frontend/peluqueria.html', context)

def galeria(request):
    # Obtener todas las imágenes activas agrupadas por categoría
    imagenes = ImagenGaleria.objects.filter(activo=True).order_by('orden')
    
    # Separar por categoría para los filtros
    categorias = ImagenGaleria.CATEGORIAS
    imagenes_por_categoria = {}
    for cat_value, cat_label in categorias:
        imagenes_por_categoria[cat_value] = imagenes.filter(categoria=cat_value)
    
    context = {
        'imagenes': imagenes,
        'imagenes_por_categoria': imagenes_por_categoria,
        'categorias': categorias,
    }
    return render(request, 'frontend/galeria.html', context)
