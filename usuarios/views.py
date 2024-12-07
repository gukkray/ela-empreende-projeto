from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from .forms import UsuarioForms
from .models import Empresa
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gerenciar.models import Produto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.views import PasswordResetView
from django.core.paginator import Paginator


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_subject.txt'
    
class UsuarioCreate(CreateView):
    template_name = "usuarios/form.html"
    form_class = UsuarioForms
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Salvar a descrição e a imagem no modelo Empresa
        descricao = form.cleaned_data.get('descricao', "")
        imagem = form.cleaned_data.get('imagem', None)
        empresa = Empresa.objects.create(user=self.object, descricao=descricao, imagem=imagem)
        
        # Verifica e adiciona o grupo "empresa" ao usuário
        grupo, created = Group.objects.get_or_create(name='empresa')
        self.object.groups.add(grupo)
        
        # Log in the user after successful registration
        login(self.request, self.object)

        return response



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EditProfileForm
from .models import Empresa



def minha_view_de_logout(request):
    logout(request)
    return redirect('inicio')

class AlterarSenhaView(PasswordChangeView):
    template_name = 'usuarios/alterar_senha.html'
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        messages.success(self.request, 'Senha alterada com sucesso.')
        return super().form_valid(form)
    
from django.db.models import Q

@login_required
def perfil_usuario(request, username):
    usuario = get_object_or_404(User, username=username)
    empresa = get_object_or_404(Empresa, user=usuario)
    
    query = request.GET.get('q')
    
    if query:
        produtos_gerais = Produto.objects.filter(
            Q(usuario=usuario, na_loja=True) & 
            (Q(nome__icontains=query) | Q(descricao__icontains=query))
        )
        produtos_em_oferta = Produto.objects.filter(
            Q(usuario=usuario, na_loja=True, oferta=True) & 
            (Q(nome__icontains=query) | Q(descricao__icontains=query))
        )
    else:
        produtos_gerais = Produto.objects.filter(usuario=usuario, na_loja=True)
        produtos_em_oferta = Produto.objects.filter(usuario=usuario, na_loja=True, oferta=True)
    
    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario,
        'empresa': empresa,
        'produtos_gerais': produtos_gerais,
        'produtos_em_oferta': produtos_em_oferta
    })


@login_required
def editar_perfil(request):
    user = request.user
    empresa = get_object_or_404(Empresa, user=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Remover imagem se o checkbox estiver marcado
            if form.cleaned_data['remover_imagem']:
                empresa.imagem.delete(save=False)
                empresa.imagem = None
            
            form.save()

            # Atualiza os campos adicionais no modelo Empresa
            empresa.descricao = form.cleaned_data['descricao']
            if form.cleaned_data['imagem']:
                empresa.imagem = form.cleaned_data['imagem']
            empresa.save()

            return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))
    else:
        initial_data = {
            'descricao': empresa.descricao,
            'imagem': empresa.imagem,
        }
        form = EditProfileForm(instance=user, initial=initial_data)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})





from django.shortcuts import render, redirect
from .forms import EnderecoForm
from .models import Endereco

@login_required
def cadastrar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.user = request.user  # Atribui o usuário atual ao endereço
            endereco.save()
            return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))
    else:
        form = EnderecoForm()
    return render(request, 'usuarios/cadastrar_endereco.html', {'form': form})
            
# views.py
from django.shortcuts import render, redirect, get_object_or_404


class EnderecoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Endereco
    template_name = "usuarios/cadastrar_endereco_edit.html"
    form_class = EnderecoForm
    success_url = reverse_lazy('perfil_usuario')
    def get_success_url(self):
        # Obtém o username do usuário associado ao contato atualizado
        username = self.request.user.username
        return reverse_lazy('perfil_usuario', kwargs={'username': username})



def excluir_endereco(request, endereco_id):
    endereco = get_object_or_404(Endereco, pk=endereco_id)
    endereco.delete()
    return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))

class EnderecoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Endereco
    template_name = "excluir_endereco.html"
    success_url = reverse_lazy('perfil_usuario')
    fields = '__all__'  # Adicione esta linha para corrigir o er

    def get_success_url(self):
        # Obtém o username do usuário associado ao endereço excluído
        username = self.object.user.username
        return reverse_lazy('perfil_usuario', kwargs={'username': username})

    
   


from .models import Contato
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ExcluirContatoForm
from django.views.generic.edit import DeleteView



from .forms import ContatoForm
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def cadastrar_contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            contato = form.save(commit=False)
            contato.user = request.user
            contato.save()
            return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))
    else:
        form = ContatoForm()
    return render(request, 'usuarios/cadastrar_contato.html', {'form': form})

    
class ContatoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Contato
    template_name = "usuarios/cadastrar_contato_edit.html"  # Nome do template de edição
    form_class = ContatoForm

    def get_success_url(self):
        # Obtém o username do usuário associado ao contato atualizado
        username = self.request.user.username
        return reverse_lazy('perfil_usuario', kwargs={'username': username})



class ContatoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Contato
    template_name = "excluir_contato.html"
    success_url = reverse_lazy('perfil_usuario')
    fields = '__all__'
    def get_success_url(self):
        # Obtém o username do usuário associado ao endereço excluído
        username = self.object.user.username
        return reverse_lazy('perfil_usuario', kwargs={'username': username})


def excluir_total_contato(request, contato_id):
    contato = get_object_or_404(Contato, pk=contato_id)
    contato.delete()
    return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))

@login_required
def excluir_contato(request, contato_id):
    contato = get_object_or_404(Contato, pk=contato_id)
    form = ExcluirContatoForm(request.POST or None, usuario=request.user)

    if request.method == 'POST' and form.is_valid():
        # Verifica se os campos estão presentes no formulário antes de acessá-los
        if 'contato' in form.cleaned_data and form.cleaned_data['contato']:
            contato.contato = None

        if 'contato2' in form.cleaned_data and form.cleaned_data['contato2']:
            contato.contato2 = None

        
        if not contato.contato and not contato.contato2:
            return excluir_total_contato(request, contato_id)

        contato.save()
        
        # Redireciona para o perfil do usuário após excluir o contato
        return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))

    return render(request, 'excluir_contato.html', {'form': form, 'contato': contato})



#novooooooooooooo


from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def listar_perfis(request):
    query = request.GET.get('q')
    empresas = Empresa.objects.exclude(user=request.user)  # Exclui o próprio usuário da lista

    if query:
        empresas = empresas.filter(
            Q(user__username__icontains=query) |  # Filtra pelo nome de usuário
            Q(descricao__icontains=query)  # Filtra pela descrição da empresa
        )
    
    # Paginação: define quantos itens por página (ajustado para 9)
    paginator = Paginator(empresas, 6)  # 9 itens por página
    page_number = request.GET.get('page')  # Pega o número da página atual
    page_obj = paginator.get_page(page_number)  # Obtém os objetos da página solicitada

    return render(request, 'usuarios/perfiluser.html', {
        'empresas': page_obj,  # Passa a página de empresas para o template
        'pagina': 'perfis'
    })


from .forms import LinksForm
from .models import Links

def cadastrar_links(request):
    if request.method == 'POST':
        form = LinksForm(request.POST)
        if form.is_valid():
            Links = form.save(commit=False)
            Links.user = request.user
            Links.save()
            return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))
    else:
        form = LinksForm()
    return render(request, 'usuarios/cadastrar_links.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404




class LinksUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Links
    template_name = "usuarios/cadastrar_links_edit.html"  # Nome do template de edição
    form_class = LinksForm

    def get_success_url(self):
        # Obtém o username do usuário associado aos links atualizados
        username = self.request.user.username
        return reverse_lazy('perfil_usuario', kwargs={'username': username})


from django.views.generic.edit import DeleteView


class LinksDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Links
    template_name = "excluir_links.html"
    success_url = reverse_lazy('perfil_usuario')
    fields = '__all__'
    def get_success_url(self):
        # Obtém o username do usuário associado ao endereço excluído
        username = self.object.user.username
        return reverse_lazy('perfil_usuario', kwargs={'username': username})

from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ExcluirLinksForm


def excluit_total_links(request, links_id):
    links = get_object_or_404(Links, pk=links_id)
    links.delete()
    return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))

def excluir_links(request, links_id):
    links = get_object_or_404(Links, pk=links_id)
    form = ExcluirLinksForm(request.POST or None, usuario=request.user)

    if request.method == 'POST' and form.is_valid():
        # Verifica se os campos estão presentes no formulário antes de acessá-los
        if 'linksfacebook' in form.cleaned_data and form.cleaned_data['linksfacebook']:
            links.linksfacebook = None

        if 'linksinstagram' in form.cleaned_data and form.cleaned_data['linksinstagram']:
            links.linksinstagram = None

        if 'linkswhatsapp' in form.cleaned_data and form.cleaned_data['linkswhatsapp']:
            links.linkswhatsapp = None
        
        if not links.linksfacebook and not links.linksinstagram and not links.linkswhatsapp:
            return excluit_total_links(request, links_id)

        links.save()
        return redirect(reverse('perfil_usuario', kwargs={'username': request.user.username}))

    return render(request, 'excluir_links.html', {'form': form, 'links': links})
 