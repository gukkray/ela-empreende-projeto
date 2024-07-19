from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Movimentacao

class MovimentacaoForm(forms.ModelForm):

    class Meta:
        model = Movimentacao
        fields = ['descricao', 'valor', 'data']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor'].widget.attrs.update({'step': '0.01'})

