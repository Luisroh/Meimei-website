from django.contrib import admin
from .models import MensajeContacto, Servicio, ImagenGaleria

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'servicio', 'fecha_envio', 'leido', 'respondido']
    list_filter = ['leido', 'respondido', 'servicio', 'fecha_envio']
    search_fields = ['nombre', 'email', 'mensaje', 'respuesta']
    readonly_fields = ['fecha_envio', 'fecha_respuesta']
    actions = ['marcar_como_leido', 'marcar_como_no_leido']
    
    def marcar_como_leido(self, request, queryset):
        queryset.update(leido=True)
    marcar_como_leido.short_description = 'Marcar como leídos'
    
    def marcar_como_no_leido(self, request, queryset):
        queryset.update(leido=False)
    marcar_como_no_leido.short_description = 'Marcar como no leídos'

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'orden', 'activo']
    list_filter = ['categoria', 'activo']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['orden', 'activo', 'precio']
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'imagen', 'categoria')
        }),
        ('Detalles', {
            'fields': ('precio', 'duracion', 'tecnica', 'beneficio')
        }),
        ('Configuración', {
            'fields': ('orden', 'activo')
        }),
    )


@admin.register(ImagenGaleria)
class ImagenGaleriaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'orden', 'activo']
    list_filter = ['categoria', 'activo']
    search_fields = ['titulo']
    list_editable = ['orden', 'activo']