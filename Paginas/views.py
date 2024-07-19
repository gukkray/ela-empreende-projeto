from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Paginas.models import Tarefa as PaginasTarefa, Produto as PaginasProduto
from tarefas.models import Tarefa as TarefasTarefa
from gerenciar.models import Produto as GerenciarProduto
from lojas.models import Venda
from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout

class IndexView(TemplateView):
    template_name = 'index.html'


def minha_view_de_logout(request):
    logout(request)
    return redirect('index')


class ModeloView(TemplateView):
    template_name = 'modelo.html'

class InicioView(TemplateView):
    template_name = 'inicio.html'

@login_required(login_url='/login/')  # Apenas usuários autenticados podem acessar esta view
def minha_view(request):
    # Consulta ao modelo PaginasTarefa
    total_tarefas_paginas = PaginasTarefa.objects.filter(usuario=request.user).count()
    
    # Consulta ao modelo PaginasProduto
    total_produtos_paginas = PaginasProduto.objects.filter(usuario=request.user).count()
    
    # Consulta ao modelo TarefasTarefa
    total_tarefas_tarefas = TarefasTarefa.objects.filter(usuario=request.user).count()
    
    # Consulta ao modelo GerenciarProduto
    total_produtos_gerenciar = GerenciarProduto.objects.filter(usuario=request.user).count()
    
    # Consulta ao modelo Venda
    total_vendas = Venda.objects.filter(usuario=request.user, finalizado=True).count()
    
    
    total_tarefas = total_tarefas_paginas + total_tarefas_tarefas
    total_produtos = total_produtos_paginas + total_produtos_gerenciar
    
    return render(request, 'inicio.html', {'total_tarefas': total_tarefas, 'total_produtos': total_produtos, 'total_vendas': total_vendas})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def tarefas_json(request):
    tarefas = Tarefa.objects.filter(usuario=request.user)
    tarefas_list = list(tarefas.values('nome', 'descricao', 'data_inicio', 'data_fim', 'concluida'))
    return JsonResponse(tarefas_list, safe=False)
