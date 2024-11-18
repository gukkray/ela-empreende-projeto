from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Q, Count
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Comentario, Venda, ItemVenda, Categoria, Produto
from .forms import ComentarioForm, AdicionarProdutoForm, CategoriaForm




@login_required
def excluir_item_venda(request, venda_id, item_id):
    venda = get_object_or_404(Venda, id=venda_id, usuario=request.user, finalizado=False)
    item_venda = get_object_or_404(ItemVenda, id=item_id, venda=venda)

    produto = item_venda.produto
    quantidade = item_venda.quantidade

    # Atualiza o estoque do produto
    produto.aumentar_estoque(quantidade)
    
    # Remove o item de venda
    item_venda.delete()
    
    # Atualiza o total da venda
    venda.total -= item_venda.preco_unitario * quantidade
    venda.save()
    
    messages.success(request, f"Produto {produto.nome} removido da venda.")
    return redirect('adicionar_produto', venda_id=venda.id)


@login_required
def buscar_produto(request):
    termo_busca = request.GET.get('termo')
    query = request.GET.get('q')
    if query:
        produtos = Produto.objects.filter(
            Q(nome__icontains=query) 
        )
    return render(request, 'adicionar_produto.html', {
       'produtos': list(produtos.values('id', 'nome', 'preco'))
    })


from django.http import JsonResponse
from .models import Produto

def buscar_produtos_por_loja(request):
    if request.is_ajax() and request.method == 'GET':
        
        produtos = Produto.objects.filter().values('nome')  # ajuste conforme a estrutura do seu modelo Produto
        return JsonResponse({'produtos': list(produtos)})
    else:
        return JsonResponse({'error': 'Requisição inválida'})


from django.shortcuts import render, redirect
from django.urls import reverse

@login_required
def iniciar_venda(request):
    # Verifica se já existe uma venda em aberto para o usuário
    venda_aberta = Venda.objects.filter(usuario=request.user, finalizado=False).first()
    if venda_aberta:
        # Remove todos os itens da venda em aberto
        ItemVenda.objects.filter(venda=venda_aberta).delete()
        # Deleta a venda em aberto
        venda_aberta.delete()
    
    if request.method == 'POST':
        # Cria uma nova venda
        venda = Venda.objects.create(usuario=request.user)
        # Redireciona para a view 'adicionar_produto' com o venda_id
        return redirect('adicionar_produto', venda_id=venda.id)
    else:
        # Renderiza o template para iniciar a venda
        return render(request, 'iniciar_venda.html')

@login_required
def adicionar_produto(request, venda_id):
    # Busca a venda em aberto para o usuário
    venda = get_object_or_404(Venda, id=venda_id, usuario=request.user, finalizado=False)
    
    if request.method == 'POST':
        if 'produto_id' in request.POST:
            produto_id = request.POST.get('produto_id')
            quantidade = int(request.POST.get('quantidade'))

            try:
                produto = Produto.objects.get(id=produto_id, usuario=request.user)
                
                # Verifica se há estoque suficiente para a venda
                if quantidade > produto.quantidade_estoque:
                    messages.error(request, f"Quantidade insuficiente em estoque para o produto {produto.nome}. Venda não pode ser concluída.")
                else:
                    # Adiciona o item à venda e atualiza o estoque
                    item_venda = ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=quantidade,
                        preco_unitario=produto.preco
                    )
                    venda.total += produto.preco * quantidade
                    venda.save()
                    
            except Produto.DoesNotExist:
                messages.error(request, "Produto não encontrado ou você não tem permissão para adicioná-lo.")

    produtos = Produto.objects.filter(usuario=request.user)
    
    return render(request, 'adicionar_produto.html', {
        'venda': venda,
        'produtos': produtos,
    })


@login_required
def finalizar_venda(request, venda_id):
    # Busca a venda em aberto para o usuário
    venda = Venda.objects.filter(id=venda_id, usuario=request.user, finalizado=False).first()  # Aqui corrigimos para 'finalizado'
    if not venda:
        # Se não houver uma venda em aberto com o ID fornecido, redireciona para iniciar a venda
        return redirect('iniciar_venda')
    
    # Verifica se há itens na venda
    if venda.itens.exists():
        # Obtém todos os itens da venda
        itens_venda = ItemVenda.objects.filter(venda=venda)

        try:
            # Inicia uma transação para garantir consistência nos dados
            with transaction.atomic():
                for item in itens_venda:
                    # Obtém o produto associado ao item da venda
                    produto = item.produto

                    # Verifica se há estoque suficiente para a venda
                    if item.quantidade <= produto.quantidade_estoque:
                        # Atualiza a quantidade em estoque do produto
                        produto.diminuir_estoque(item.quantidade)
                    else:
                        # Se não houver estoque suficiente, cancela a venda
                        messages.error(request, f"Quantidade insuficiente em estoque para o produto {produto.nome}. Venda cancelada.")
                        return redirect('iniciar_venda')

                # Atualiza o status da venda
                venda.finalizado = True  # Aqui corrigimos para 'finalizado'
                venda.save()
            
            return redirect(reverse('listar_vendas') + '?success=true')
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao finalizar a venda: {str(e)}")
            return redirect('listar_vendas')
    else:
        # Se nenhum produto foi adicionado à venda, redireciona de volta à página de adicionar produtos
        messages.error(request, "Nenhum produto foi adicionado à venda. Por favor, adicione pelo menos um produto antes de finalizar a venda.")
        return redirect('adicionar_produto', venda_id=venda_id)

@login_required
def listar_vendas(request):
    success_message = None
    if 'success' in request.GET:
        success_message = "Venda concluída com sucesso!"
        request.GET = request.GET.copy()
        request.GET.pop('success', None)

    query = request.GET.get('q')
    vendas = Venda.objects.filter(usuario=request.user, finalizado=True).order_by('-data_criacao')

    if query:
        vendas = vendas.filter(
            Q(itens__quantidade__icontains=query) |
            Q(itens__produto__nome__icontains=query) |  # Filtra pelo nome do produto associado ao item da venda
            Q(total__icontains=query) |
            Q(data_criacao__icontains=query)  # Filtra pela data de criação da venda
        ).distinct()

    vendas = vendas.annotate(total_produtos=Count('itens'))

    total_produtos = sum(venda.total_produtos for venda in vendas)

    return render(request, 'gerenciarLoja/listas/venda.html', {
        'vendas': vendas,
        'total_produtos': total_produtos,
        'success_message': success_message,
        'query': query,
    })



class VendaDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'  # Substitua pela sua URL de login
    model = Venda
    template_name = "gerenciarLoja/excluir_venda.html"  # Caminho correto para o template
    success_url = reverse_lazy('listar_vendas')  # Substitua 'listar_vendas' pelo nome da sua URL de lista de vendas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venda = self.get_object()
        context['produtos'] = venda.itens.all()
        return context


@login_required
def get_total_venda(request, venda_id):
    venda = Venda.objects.get(id=venda_id)
    total = sum(item.produto.preco * item.quantidade for item in venda.itens.all())
    return JsonResponse({'total': total})


from django.db.models import Q

class VendaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Venda
    template_name = "venda.html"
    context_object_name = 'vendas'

    def get_queryset(self):
        queryset = Venda.objects.filter(usuario=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(data_criacao__icontains=query) |  # Filtra pela data de criação da venda
                Q(itens_produto_nome__icontains=query) |  # Filtra pelo nome do produto nos itens da venda
                Q(total__icontains=query)  # Filtra pelo código de barras do produto nos itens da venda
            ).distinct()  # Utiliza distinct para evitar duplicatas
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_vendas'] = Venda.objects.filter(usuario=self.request.user).count()
        context['pagina'] = 'vendas'  # Adiciona a informação da página atual
        return context

class CategoriaCreateView(CreateView):
    model = Categoria
    fields = ['nome']  # Ajuste os campos de acordo com o modelo Categoria
    template_name = 'forum/cadastrar_categoria.html'  # Altere para o nome correto do template
    success_url = reverse_lazy('exibir_comentarios', kwargs={'categoria_id': 1})  # Defina o ID padrão aqui
def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()  # Salva a nova categoria
            return redirect('exibir_comentarios', kwargs={'categoria_id': 1})  # Redireciona para a página de comentários
    else:
        form = CategoriaForm()
    return render(request, 'forum/cadastrar_categoria.html', {'form': form}, kwargs={'categoria_id': 1})

class ComentarioCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'  # Substitua pela sua URL de login
    model = Comentario
    template_name = "forum/comentarios.html"  # Substitua pelo seu template
    form_class = ComentarioForm
    success_url = reverse_lazy('cadastrar-comentario')  # Substitua 'listar-comentario' pelo nome da sua URL de lista de comentários

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = Comentario.objects.order_by('-data_publicacao')  # Adiciona os comentários ao contexto
        return context
    
class ComentarioUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'  # Substitua pela sua URL de login
    model = Comentario
    template_name = "forum/editar_comentario.html"  # Substitua pelo seu template
    form_class = ComentarioForm
    success_url = reverse_lazy('listar-comentario')  # Substitua 'listar-comentario' pelo nome da sua URL de lista de comentários

class ComentarioDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'  # Substitua pela sua URL de login
    model = Comentario
    template_name = "forum/excluir_comentario.html"  # Substitua pelo seu template
    success_url = reverse_lazy('listar-comentario')  # Substitua 'listar-comentario' pelo nome da sua URL de lista de comentários

from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Comentario
from .forms import ComentarioForm

def exibir_comentarios(request, categoria_id=None):
        # Verifica se existem categorias no banco de dados
    if not Categoria.objects.exists():
        # Cria a categoria "Geral" se nenhuma categoria existir
        Categoria.objects.create(nome="Geral")
    # Se categoria_id for None, pega a primeira categoria ou redireciona para a primeira disponível
    if categoria_id is None:
        categoria = Categoria.objects.first()
        if not categoria:
            return redirect('alguma_categoria_padrão')  # Redireciona para uma categoria padrão
        return redirect('exibir_comentarios', categoria_id=categoria.id)
        # Filtrar por categoria, se selecionada
        categorias = Categoria.objects.all()
    categorias = Categoria.objects.all()
    comentarios = Comentario.objects.all()
    if categoria_id:
        comentarios = comentarios.filter(categoria_id=categoria_id)
    # Obtém a categoria ou retorna 404 se não encontrada
    categoria = get_object_or_404(Categoria, id=categoria_id)

    # Obtém os comentários da categoria ordenados pela data de publicação
    comentarios = Comentario.objects.filter(categoria=categoria).order_by('data_publicacao')

    # Processa o envio do formulário de comentário
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)  # Cria o comentário mas não salva ainda
            # Aqui, pegamos o valor da categoria selecionada
            categoria_id_post = request.POST.get('categoria')
            if categoria_id_post:
                comentario.categoria = Categoria.objects.get(id=categoria_id_post)  # Ajuste aqui
            comentario.autor = request.user  # Associa o autor ao comentário
            comentario.save()  # Salva o comentário no banco
            return redirect('exibir_comentarios', categoria_id=categoria.id)  # Redireciona para a mesma categoria

    else:
        form = ComentarioForm()

    # Retorna a renderização da página com os dados necessários
    return render(request, 'forum/comentarios.html', {
        'categoria': categoria,
        'comentarios': comentarios,
        'form': form,
        'categorias': Categoria.objects.all(),  # Para preencher o seletor de categorias
        'categoria_selecionada': categoria_id,

    })

