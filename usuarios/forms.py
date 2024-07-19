from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Empresa  # Import your Empresa model
from localflavor.br.forms import BRStateSelect


class UsuarioForms(UserCreationForm):
    nome = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="E-mail")
    descricao = forms.CharField(max_length=255, label="Descrição", required=False)
    imagem = forms.ImageField(label="Imagem", required=False)
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirme a senha",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'nome', 'email', 'descricao', 'imagem', 'password1', 'password2']

        labels = {
            'username': 'Usuário:',
            'nome': 'Nome:',
            'email': 'E-mail:',
            'password1': 'Senha:',
            'password2': 'Confirme a senha:',
            'descricao': 'Descrição:',
            'imagem': 'Imagem:',
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError(_("A senha deve ter pelo menos 8 caracteres."))
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise ValidationError(_("As senhas não correspondem."))
        return password2


class EditProfileForm(forms.ModelForm):
    descricao = forms.CharField(max_length=255, label="Descrição", required=False)
    imagem = forms.ImageField(label="Imagem", required=False, widget=forms.FileInput)
    remover_imagem = forms.BooleanField(label="Remover imagem", required=False)

    class Meta:
        model = User
        fields = ['username', 'descricao', 'imagem']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagem'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['remover_imagem'].widget.attrs.update({'class': 'form-check-input'})


from .models import Endereco

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        
        fields = ['estado', 'cidade', 'endereco', 'numero', 'complemento']
    estado = forms.CharField(widget=BRStateSelect())

from .models import Contato

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['contato', 'contato2']
        labels = { 
             'contato': 'Adicione um contato:',
             'contato2': 'Adicione outro contato:',

             }



from django import forms
from .models import Contato

class ExcluirContatoForm(forms.Form):
    contato = forms.BooleanField(required=False)
    contato2 = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  
        super(ExcluirContatoForm, self).__init__(*args, **kwargs)

        if usuario:
            if not usuario.contato.contato:
                del self.fields['contato']  
            if not usuario.contato.contato2:
                del self.fields['contato2']  
    


from .models import Links

class LinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ['linksfacebook', 'linksinstagram', 'linkswhatsapp']
        labels = {
            'linksfacebook': 'Adicione o link do facebook',
            'linksinstagram': 'Adicione o link do instagram',
            'linkswhatsapp': 'Adicione o link do whatsapp',
            }





from django import forms
from .models import Links

class ExcluirLinksForm(forms.Form):
    linksfacebook = forms.BooleanField(required=False)
    linksinstagram = forms.BooleanField(required=False)
    linkswhatsapp = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Obtém o usuário passado como argumento
        super(ExcluirLinksForm, self).__init__(*args, **kwargs)

        if usuario:
            if not usuario.links.linksfacebook:
                del self.fields['linksfacebook']  # Remove o campo linksfacebook
            if not usuario.links.linksinstagram:
                del self.fields['linksinstagram']  # Remove o campo linksinstagram
            if not usuario.links.linkswhatsapp:
                del self.fields['linkswhatsapp']  # Remove o campo linkswhatsapp
