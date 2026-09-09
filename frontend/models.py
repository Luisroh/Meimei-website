from django.db import models
from django.utils import timezone

class Servicio(models.Model):
    CATEGORIAS = [
        ('masaje', 'Masaje'),
        ('peluqueria', 'Peluquería'),
    ]
    
    nombre = models.CharField('Nombre del servicio', max_length=100)
    descripcion = models.TextField('Descripción')
    imagen = models.ImageField('Imagen', upload_to='servicios/', blank=True, null=True)
    precio = models.DecimalField('Precio', max_digits=6, decimal_places=2, blank=True, null=True)
    categoria = models.CharField('Categoría', max_length=20, choices=CATEGORIAS)
    duracion = models.CharField('Duración', max_length=50, blank=True, help_text='Ej: 60-90 min')
    tecnica = models.CharField('Técnica', max_length=100, blank=True, help_text='Ej: Presión profunda')
    beneficio = models.CharField('Beneficio', max_length=100, blank=True, help_text='Ej: Alivio del dolor muscular')
    orden = models.IntegerField('Orden', default=0, help_text='Menor número = aparece antes')
    activo = models.BooleanField('Activo', default=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', default=timezone.now)
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

class ImagenGaleria(models.Model):
    """Modelo para imágenes de la galería"""
    
    CATEGORIAS = [
        ('espacio', 'Nuestro Espacio'),
        ('masajes', 'Masajes'),
        ('peluqueria', 'Peluquería'),
    ]
    
    imagen = models.ImageField('Imagen', upload_to='galeria/')
    titulo = models.CharField('Título', max_length=100, blank=True)
    categoria = models.CharField('Categoría', max_length=20, choices=CATEGORIAS)
    orden = models.IntegerField('Orden', default=0, help_text='Menor número = aparece antes')
    activo = models.BooleanField('Activo', default=True)
    fecha_subida = models.DateTimeField('Fecha de subida', default=timezone.now)
    
    class Meta:
        verbose_name = 'Imagen de galería'
        verbose_name_plural = 'Imágenes de galería'
        ordering = ['orden', 'fecha_subida']
    
    def __str__(self):
        return self.titulo or f"Imagen {self.id} - {self.get_categoria_display()}"

class MensajeContacto(models.Model):
    """Modelo para almacenar mensajes del formulario de contacto"""
    
    SERVICIO_CHOICES = [
        ('', 'Selecciona un servicio...'),
        ('masaje-descontracturante', 'Masaje Descontracturante'),
        ('masaje-relajante', 'Masaje Relajante'),
        ('masaje-terapeutico', 'Masaje Terapéutico'),
        ('masaje-piedras', 'Masaje con Piedras Calientes'),
        ('corte', 'Corte y Peinado'),
        ('coloracion', 'Coloración'),
        ('tratamiento', 'Tratamientos Capilares'),
        ('alisado', 'Alisados'),
        ('recogido', 'Recogidos y Bodas'),
        ('infantil', 'Peluquería Infantil'),
        ('otros', 'Otros'),
    ]
    
    nombre = models.CharField('Nombre completo', max_length=100)
    email = models.EmailField('Correo electrónico')
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    servicio = models.CharField('Servicio de interés', max_length=50, choices=SERVICIO_CHOICES, blank=True)
    mensaje = models.TextField('Mensaje')
    fecha_envio = models.DateTimeField('Fecha de envío', default=timezone.now)
    leido = models.BooleanField('Leído', default=False)
    
    # ✅ NUEVOS CAMPOS PARA RESPUESTAS
    respuesta = models.TextField('Respuesta', blank=True, null=True)
    fecha_respuesta = models.DateTimeField('Fecha de respuesta', blank=True, null=True)
    respondido = models.BooleanField('Respondido', default=False)
    
    class Meta:
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
        ordering = ['-fecha_envio']
    
    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"