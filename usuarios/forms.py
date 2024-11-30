from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from localflavor.br.forms import BRStateSelect
from .models import Empresa, Endereco, Contato, Links
from localflavor.br.forms import BRStateSelect
from localflavor.br.br_states import STATE_CHOICES
import re

class UsuarioForms(UserCreationForm):
    nome = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="E-mail")
    descricao = forms.CharField(max_length=255, label="Descrição", required=False)
    imagem = forms.ImageField(label="Imagem", required=False)
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme a senha", widget=forms.PasswordInput)

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
    email = forms.EmailField(label="E-mail", required=True)  # Add this field
    descricao = forms.CharField(max_length=255, label="Descrição", required=False)
    imagem = forms.ImageField(label="Imagem", required=False, widget=forms.FileInput)
    remover_imagem = forms.BooleanField(label="Remover imagem", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'descricao', 'imagem']  # Include email here

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})  # Add class for styling
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagem'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['remover_imagem'].widget.attrs.update({'class': 'form-check-input'})



class EnderecoForm(forms.ModelForm):
    estado = forms.ChoiceField(choices=STATE_CHOICES, label="Estado")  # Define choices here

    class Meta:
        model = Endereco
        fields = ['estado', 'cidade', 'endereco', 'numero', 'complemento']


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['contato', 'contato2']
        labels = {
            'contato': 'Adicione um contato:',
            'contato2': 'Adicione outro contato:',
        }

    def clean_contato(self):
        contato = self.cleaned_data.get('contato')
        return self.validate_phone_number(contato)

    def clean_contato2(self):
        contato2 = self.cleaned_data.get('contato2')
        return self.validate_phone_number(contato2)

    def validate_phone_number(self, phone_number):
        phone_number_digits = re.sub(r'\D', '', phone_number)  # Remove caracteres não numéricos
            if len(phone_number_digits) < 9:  # Alterado para aceitar pelo menos 9 dígitos
                raise ValidationError("O contato deve conter no mínimo 9 números.")
            return phone_number_digits
        return phone_number


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


class LinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ['linksfacebook', 'linksinstagram', 'linkswhatsapp']
        labels = {
            'linksfacebook': 'Adicione o link do facebook',
            'linksinstagram': 'Adicione o link do instagram',
            'linkswhatsapp': 'Adicione o link do whatsapp',
        }


class ExcluirLinksForm(forms.Form):
    linksfacebook = forms.BooleanField(required=False)
    linksinstagram = forms.BooleanField(required=False)
    linkswhatsapp = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super(ExcluirLinksForm, self).__init__(*args, **kwargs)

        if usuario:
            if not usuario.links.linksfacebook:
                del self.fields['linksfacebook']
            if not usuario.links.linksinstagram:
                del self.fields['linksinstagram']
            if not usuario.links.linkswhatsapp:
                del self.fields['linkswhatsapp']