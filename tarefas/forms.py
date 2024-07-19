from django import forms
from .models import Tarefa
from django.core.exceptions import ValidationError
from datetime import date

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_data_inicio(self):
        data_inicio = self.cleaned_data['data_inicio']
        if data_inicio < date.today():
            raise ValidationError('A data de início não pode ser anterior à data atual.')
        return data_inicio

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        if data_inicio and data_fim:
            if data_fim < data_inicio:
                self.add_error('data_fim', 'A data de término não pode ser anterior à data de início.')
