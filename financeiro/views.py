from django.views.generic.edit import CreateView, DeleteView
from .models import Movimentacao
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import MovimentacaoForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Movimentacao

class SaidaCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login') 
    model = Movimentacao
    template_name = "cadastrar_movimentacao.html"
    form_class = MovimentacaoForm
    success_url = reverse_lazy('listar-saida')  
    def form_valid(self, form):
        form.instance.usuario_id = self.request.user.id
        form.instance.valor *= -1  
        return super().form_valid(form)

class SaidaDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Movimentacao
    template_name = "excluir_movimentacao.html"
    success_url = reverse_lazy('listar-saida')  
    fields = '__all__'  

class SaidaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')  
    model = Movimentacao
    template_name = "listas/saidas.html"
    context_object_name = 'saidas'  
    ordering = ['-id'] 

    def get_queryset(self):
        return Movimentacao.objects.filter(usuario=self.request.user)

class EntradaCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login') 
    model = Movimentacao
    template_name = "cadastrar_movimentacao.html"
    form_class = MovimentacaoForm
    success_url = reverse_lazy('listar-entrada')  

    def form_valid(self, form):
        form.instance.usuario_id = self.request.user.id
        return super().form_valid(form)


class EntradaDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Movimentacao
    template_name = "excluir_movimentacao.html"
    success_url = reverse_lazy('listar-entrada')  
    fields = '__all__'  

class EntradaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')  
    model = Movimentacao
    template_name = "listas/entradas.html"
    context_object_name = 'entradas'  
    ordering = ['-id'] 

    def get_queryset(self):
        return Movimentacao.objects.filter(usuario=self.request.user)


@login_required
def listar_Movimentacoes(request):
    movimentacoes = Movimentacao.objects.filter(usuario=request.user)
    return render(request, 'movimentacoes.html', {'movimentacoes': movimentacoes})



def obter_dados_entrada(request):
    dados_entrada = Movimentacao.objects.filter(valor__gte=0, usuario=request.user)
    dados_json = [{'data': movimentacao.data, 'valor': movimentacao.valor} for movimentacao in dados_entrada]
   
    return JsonResponse(dados_json, safe=False)

def obter_dados_saida(request):
    dados_saida = Movimentacao.objects.filter(valor__lt=0, usuario=request.user)
    
    dados_json = [{'data': movimentacao.data, 'valor': movimentacao.valor} for movimentacao in dados_saida]
    
    return JsonResponse(dados_json, safe=False)

def tipo_movimentacao(request):
    return render(request, 'p1.html')