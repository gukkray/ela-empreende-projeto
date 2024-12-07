from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from localflavor.br.forms import BRStateSelect
from localflavor.br.br_states import STATE_CHOICES
from .models import Empresa, Endereco, Contato, Links
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
    email = forms.EmailField(label="E-mail", required=True)
    descricao = forms.CharField(max_length=255, label="Descrição", required=False)
    imagem = forms.ImageField(label="Imagem", required=False, widget=forms.FileInput)
    remover_imagem = forms.BooleanField(label="Remover imagem", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'descricao', 'imagem']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['remover_imagem'].widget.attrs.update({'class': 'form-check-input'})


class EnderecoForm(forms.ModelForm):
    estado = forms.ChoiceField(choices=STATE_CHOICES, label="Estado")

    class Meta:
        model = Endereco
        fields = ['estado', 'cidade', 'endereco', 'numero', 'complemento']




from django import forms
from .models import Contato

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['contato', 'contato2']
        labels = {
            'contato': 'Adicione um contato:',
            'contato2': 'Adicione outro contato (opcional):',
        }

    def validate_phone_number(self, phone_number):
        """Valida se o número de telefone contém apenas dígitos."""
        if not phone_number:
            raise forms.ValidationError("O campo de contato não pode estar vazio.")
        if not phone_number.isdigit():
            raise forms.ValidationError("O número de contato deve conter apenas dígitos.")
        if len(phone_number) < 8 or len(phone_number) > 15:
            raise forms.ValidationError("O número de contato deve ter entre 8 e 15 dígitos.")
        return phone_number

    def clean_contato(self):
        """Valida o campo 'contato', que é obrigatório."""
        contato = self.cleaned_data.get('contato')
        return self.validate_phone_number(contato)

    def clean_contato2(self):
        """Valida o campo 'contato2', que é opcional."""
        contato2 = self.cleaned_data.get('contato2')
        if contato2:  # Apenas valida se houver algum valor no campo.
            return self.validate_phone_number(contato2)
        return contato2  # Retorna o valor vazio ou None, sem erro.

    def activate_phone_number(self):
        """Processa os números de telefone, removendo caracteres não numéricos."""
        phone_number_digits = ""  # Inicializa a variável para o primeiro número
        second_phone_number_digits = ""  # Inicializa a variável para o segundo número

        # Processa o primeiro número de contato
        phone_number = self.cleaned_data.get('contato')
        if phone_number:
            phone_number_digits = "".join(filter(str.isdigit, phone_number))

        # Processa o segundo número de contato, se disponível
        phone_number2 = self.cleaned_data.get('contato2')
        if phone_number2:
            second_phone_number_digits = "".join(filter(str.isdigit, phone_number2))

        # Apenas para depuração (remova ou substitua em produção)
        print("Contato 1:", phone_number_digits)
        print("Contato 2 (opcional):", second_phone_number_digits)



class ExcluirContatoForm(forms.Form):
    contato = forms.BooleanField(required=False)
    contato2 = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super(ExcluirContatoForm, self).__init__(*args, **kwargs)

        if usuario:
            if not getattr(usuario.contato, 'contato', None):
                del self.fields['contato']
            if not getattr(usuario.contato, 'contato2', None):
                del self.fields['contato2']


class LinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ['linksfacebook', 'linksinstagram', 'linkswhatsapp']
        labels = {
            'linksfacebook': 'Adicione o link do Facebook:',
            'linksinstagram': 'Adicione o link do Instagram:',
            'linkswhatsapp': 'Adicione o link do WhatsApp:',
        }


class ExcluirLinksForm(forms.Form):
    linksfacebook = forms.BooleanField(required=False)
    linksinstagram = forms.BooleanField(required=False)
    linkswhatsapp = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super(ExcluirLinksForm, self).__init__(*args, **kwargs)

        if usuario:
            if not getattr(usuario.links, 'linksfacebook', None):
                del self.fields['linksfacebook']
            if not getattr(usuario.links, 'linksinstagram', None):
                del self.fields['linksinstagram']
            if not getattr(usuario.links, 'linkswhatsapp', None):
                del self.fields['linkswhatsapp']
