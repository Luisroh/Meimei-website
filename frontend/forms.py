from django import forms
from .models import MensajeContacto

class ContactoForm(forms.ModelForm):

    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'telefono', 'servicio', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu nombre',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'tu@email.com',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '600 12 34 56'
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-input'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 5,
                'placeholder': 'Cuéntanos qué necesitas...',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clases CSS adicionales
        self.fields['servicio'].widget.choices = [('', 'Selecciona un servicio...')] + list(MensajeContacto.SERVICIO_CHOICES)[1:]
        self.fields['nombre'].label = 'Nombre completo *'
        self.fields['email'].label = 'Correo electrónico *'
        self.fields['mensaje'].label = 'Mensaje *'