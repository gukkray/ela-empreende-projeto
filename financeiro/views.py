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
from django.db.models import Sum

class MovimentacaoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Movimentacao
    template_name = "cadastrar_movimentacao.html"
    form_class = MovimentacaoForm
    success_url = reverse_lazy('listar-movimentacoes')  # Lista todas as movimentações.

    def form_valid(self, form):
        form.instance.usuario_id = self.request.user.id
        if form.cleaned_data['tipo'] == 'saida':
            form.instance.valor *= -1  # Ajusta o valor para saídas.
        return super().form_valid(form)

class MovimentacaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Movimentacao
    template_name = "listas/movimentacoes.html"
    context_object_name = 'movimentacoes'
    ordering = ['-id']

    def get_queryset(self):
        return Movimentacao.objects.filter(usuario=self.request.user)
    
class MovimentacaoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Movimentacao
    template_name = "excluir_movimentacao.html"
    success_url = reverse_lazy('listar-movimentacoes')


@login_required
def exibir_grafico(request):
    return render(request, 'grafico.html')

@login_required
def listar_Movimentacoes(request):
    movimentacoes = Movimentacao.objects.filter(usuario=request.user)
    return render(request, 'movimentacoes.html', {'movimentacoes': movimentacoes})



def obter_dados_entrada(request):
    dados_entrada = (
        Movimentacao.objects.filter(valor__gte=0, usuario=request.user)
        .values('data')
        .annotate(total=Sum('valor'))
        .order_by('data')
    )
    dados_json = [{'data': item['data'], 'valor': float(item['total'])} for item in dados_entrada]
    return JsonResponse(dados_json, safe=False)

def obter_dados_saida(request):
    dados_saida = (
        Movimentacao.objects.filter(valor__lt=0, usuario=request.user)
        .values('data')
        .annotate(total=Sum('valor'))
        .order_by('data')
    )
    dados_json = [{'data': item['data'], 'valor': float(item['total'])} for item in dados_saida]
    return JsonResponse(dados_json, safe=False)

def tipo_movimentacao(request):
    return render(request, 'p1.html')