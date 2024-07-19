from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from .models import Cliente

class ClienteForm(forms.ModelForm):
    # Seu código existente para o formulário

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data['data_nascimento']
        if data_nascimento:
            if data_nascimento > date.today():
                raise ValidationError("A data de nascimento não pode ser maior que a data atual.")
        return data_nascimento

    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco', 'data_nascimento']

        labels = {
            'nome': 'Nome:',
            'email': 'E-mail:',
            'telefone': 'Telefone:',
            'endereco': 'Endereço:',
            'data_nascimento': 'Data de Nascimento:',
        }

        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
