from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Tarefa  # Substitua 'Tarefa' pelo nome do seu modelo de tarefa
from .forms import TarefaForm  # Substitua 'TarefaForm' pelo nome do seu formulário de tarefa
from django.db.models import Count
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Tarefa
from .forms import TarefaForm
from django.db.models import Count
from django.http import JsonResponse
from django.core.exceptions import ValidationError

class TarefaCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Tarefa
    template_name = "agendando/cadastrar_tarefa.html"
    form_class = TarefaForm
    success_url = reverse_lazy('listar-tarefas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Associa o usuário à tarefa

        # Verifica se uma tarefa com o mesmo nome e usuário já existe
        tarefa_existente = Tarefa.objects.filter(usuario=self.request.user, nome=form.cleaned_data['nome']).exclude(id=form.instance.id).exists()

        if tarefa_existente:
            # Adiciona uma mensagem de erro ao formulário
            form.add_error('nome', 'Já existe uma tarefa cadastrada com esse nome para esse usuário.')
            return super().form_invalid(form)

        return super().form_valid(form)


class TarefaUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Tarefa
    template_name = "agendando/cadastrar_tarefa_edit.html"
    form_class = TarefaForm
    success_url = reverse_lazy('listar-tarefas')

class TarefaDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Tarefa
    template_name = "agendando/excluir_tarefa.html"  # Substitua pelo seu template de exclusão de tarefa
    success_url = reverse_lazy('listar-tarefas')  # Substitua 'listar-tarefas' pelo nome da sua URL de listar tarefas


from datetime import date

from django.db.models import Q

from django.db.models import Q

class TarefaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Tarefa
    template_name = "agendando/listar/listar_tarefas.html"
    context_object_name = 'tarefas'
    paginate_by = 10

    def get_queryset(self):
        queryset = Tarefa.objects.filter(usuario=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) | 
                Q(descricao__icontains=query) | 
                Q(data_inicio__icontains=query) | 
                Q(data_fim__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tarefas'] = Tarefa.objects.filter(usuario=self.request.user).count()
        context['pagina'] = 'tarefas'  # Adiciona a informação da página atual
        return context


def concluir_tarefa(request):
    # Obter o ID da tarefa a ser concluída
    tarefa_id = request.POST.get('tarefa_id')
    
    try:
        # Buscar a tarefa no banco de dados
        tarefa = Tarefa.objects.get(pk=tarefa_id)
        
        # Marcar a tarefa como concluída
        tarefa.concluida = True
        tarefa.save()
        
        # Retornar uma resposta JSON indicando sucesso
        return JsonResponse({'success': True})
    except Tarefa.DoesNotExist:
        # Se a tarefa não for encontrada, retornar uma resposta JSON indicando erro
        return JsonResponse({'success': False, 'error': 'Tarefa não encontrada'})