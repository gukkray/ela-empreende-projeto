from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Cliente
from .forms import ClienteForm
from datetime import date
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class ClienteCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_form.html'
    
    success_url = reverse_lazy('cliente_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Associa o usuário ao cliente

        cliente_existente = Cliente.objects.filter(usuario=self.request.user, nome=form.cleaned_data['nome']).exclude(id=form.instance.id).exists()

        if cliente_existente:
            form.add_error('nome', 'Já existe um cliente cadastrado com esse nome para esse usuário.')
            return super().form_invalid(form)

        return super().form_valid(form)


class ClienteUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_form_edit.html'
    success_url = reverse_lazy('cliente_list')

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Cliente
    template_name = 'cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


from django.db.models import Q

class ClienteListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Cliente
    template_name = 'clientes_list.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        queryset = Cliente.objects.filter(usuario=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) | 
                Q(email__icontains=query) | 
                Q(telefone__icontains=query) | 
                Q(endereco__icontains=query) | 
                Q(data_nascimento__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = date.today()
        aniversariantes = self.get_queryset().filter(data_nascimento__month=hoje.month, data_nascimento__day=hoje.day)
        context['aniversariantes'] = aniversariantes
        context['pagina'] = 'clientes'  # Adiciona a informação da página atual
        return context
