from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Produto

class ProdutoForm(forms.ModelForm):
    imagem = forms.ImageField(label='Imagem do Produto', required=False) 

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'quantidade_estoque', 'imagem', 'na_loja', 'oferta']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preco'].widget.attrs.update({'step': '0.01'})
        self.fields['quantidade_estoque'].widget.attrs.update({'min': '0'})

    def clean_preco(self):
        preco = self.cleaned_data['preco']
        if preco < 0:
            raise forms.ValidationError("O preço não pode ser negativo.")
        return preco

    def clean_quantidade_estoque(self):
        quantidade_estoque = self.cleaned_data['quantidade_estoque']
        if quantidade_estoque < 0:
            raise forms.ValidationError("A quantidade em estoque não pode ser negativa.")
        return quantidade_estoque


