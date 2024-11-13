from django import forms
from .models import Comentario, ItemVenda, Venda, Comentario, Categoria
from gerenciar.models import Produto


class AdicionarProdutoForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona um campo para armazenar o preço unitário do produto
        self.fields['preco_unitario'] = forms.DecimalField(disabled=True, decimal_places=2, required=False)  # Campo desabilitado para evitar edição

        if 'data' in kwargs and kwargs['data']:
            # Se estivermos recebendo dados do formulário (ou seja, o formulário foi enviado), preencha o preço unitário com o valor do produto selecionado
            produto_id = kwargs['data'].get('produto')
            if produto_id:
                produto = Produto.objects.get(pk=produto_id)
                self.fields['preco_unitario'].initial = produto.preco

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['total']  # Defina os campos do formulário

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtém o usuário passado para o formulário
        super().__init__(*args, **kwargs)
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', ]

def get_comentario_model():
    from .models import Comentario 
    return Comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'categoria']  # Inclui 'categoria' se estiver usando o seletor no formulário
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
