from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Produto
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProdutoForm
# views.py em sua aplicação de produtos
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.db.models import Q
class ProdutoCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'  # substitua por sua URL de login
    model = Produto
    template_name = "gerenciar/cadastrar_produto.html"
    form_class = ProdutoForm
    success_url = reverse_lazy('listar-produto')  

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Associa o usuário ao produto

        # Verifica se um produto com o mesmo nome e usuário já existe
        produto_existente = Produto.objects.filter(usuario=self.request.user, nome=form.cleaned_data['nome']).exclude(id=form.instance.id).exists()

        if produto_existente:
            # Adiciona uma mensagem de erro ao formulário
            form.add_error('nome', 'Já existe um produto cadastrado com esse nome para esse usuário.')
            return super().form_invalid(form)

        return super().form_valid(form)
    

class ProdutoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Produto
    template_name = "gerenciar/editar-produto.html"
    form_class = ProdutoForm
    success_url = reverse_lazy('listar-produto')


class ProdutoDelete(DeleteView):
    login_url = reverse_lazy('login')
    model = Produto
    template_name = "gerenciar/excluir-produto.html"
    success_url = reverse_lazy('listar-produto')  # Substitua 'inicio' pelo nome da sua URL de sucesso
    fields = '__all__'  # Adicione esta linha para corrigir o erro

class ProdutosGeraisList(LoginRequiredMixin, ListView):
    login_url = '/login/'  # substitute with your login URL
    model = Produto
    template_name = "gerenciar/listas/produtos_gerais.html"
    context_object_name = 'produtos'  # specify the context object name
    ordering = ['-id']  # optional: order by the product ID or another field

    def get_queryset(self):
        queryset = Produto.objects.filter(usuario=self.request.user, na_loja=True)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) | 
                Q(preco__icontains=query) | 
                Q(descricao__icontains=query)
            )
        return queryset



class ProdutoList(LoginRequiredMixin, ListView):
    login_url = '/login/'  # substitua com sua URL de login
    model = Produto
    template_name = "gerenciar/listas/produtos_gerais.html"
    context_object_name = 'produtos'  # especifica o nome do contexto
    ordering = ['-id']  # opcional: ordena pelo ID do produto ou outro campo

    def get_queryset(self):
        queryset = Produto.objects.filter(usuario=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) | 
                Q(descricao__icontains=query) | 
                Q(preco__icontains=query) | 
                Q(quantidade_estoque__icontains=query) | 
                Q(na_loja__icontains=query) | 
                Q(oferta__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagina'] = 'produtos'  # Adiciona a informação da página atual
        return context


@login_required
def perfil_usuario(request):
    usuario = request.user
    produtos_em_oferta = Produto.objects.filter(usuario=usuario, oferta=True)
    return render(request, 'usuarios/perfil.html', {'usuario': usuario, 'produtos': produtos_em_oferta})