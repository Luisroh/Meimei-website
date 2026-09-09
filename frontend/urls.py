# frontend/urls.py
from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('masajes/', views.masajes, name='masajes'),
    path('peluqueria/', views.peluqueria, name='peluqueria'),
    path('galeria/', views.galeria, name='galeria'),
    path('contacto/', views.contacto, name='contacto'),
    path('mei-contesta-mei/', views.panel_mensajes, name='panel_mensajes'),
    path('mei-contesta-mei/marcar/<int:mensaje_id>/', views.marcar_leido, name='marcar_leido'),
    path('mei-contesta-mei/responder/<int:mensaje_id>/', views.enviar_respuesta, name='enviar_respuesta'),
]