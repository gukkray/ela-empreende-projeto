from django import forms
from .models import Comentario, ItemVenda, Venda
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
        

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {'texto': 'Comentário'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_texto(self):
        texto = self.cleaned_data['texto']
        # Adicione suas validações personalizadas, se necessário
        return texto