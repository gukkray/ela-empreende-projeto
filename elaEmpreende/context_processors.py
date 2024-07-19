from datetime import date
from clientes.models import Cliente

def global_message(request):
    # Inicialmente, define context_message como None
    context_message = None

    if request.user.is_authenticated:
        # Verifica aniversariantes apenas para o usuário logado
        hoje = date.today()
        aniversariantes = Cliente.objects.filter(usuario=request.user, data_nascimento__month=hoje.month, data_nascimento__day=hoje.day)

        if aniversariantes.exists():
            # Se houver aniversariantes, define a mensagem para exibir no template
            context_message = " "

    return {
        'global_message': context_message
    }
