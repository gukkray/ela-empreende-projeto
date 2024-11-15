from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AlterarSenhaView, listar_perfis, cadastrar_links, LinksUpdate, UsuarioCreate, EnderecoDelete, excluir_contato, ContatoUpdate, cadastrar_contato, perfil_usuario, cadastrar_endereco, EnderecoUpdate, excluir_endereco
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name="login"),
    
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar_senha'),
    path('registrar/', UsuarioCreate.as_view(), name='registrar'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    
    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    
    path('cadastrar-endereco/', cadastrar_endereco, name='cadastrar_endereco'),
    path('excluir/endereco/<int:pk>/', EnderecoDelete.as_view(), name='excluir_endereco'),
    path('editar/endereco/<int:pk>/', EnderecoUpdate.as_view(), name='editar_endereco'),
    
    path('cadastrar/contato/', cadastrar_contato, name='cadastrar_contato'),
    path('editar/contato/<int:pk>/', ContatoUpdate.as_view(), name='editar_contato'),
    path('excluir/contato/<int:contato_id>/', views.excluir_contato, name='excluir_contato'),
    
    path('cadastrar/link/', cadastrar_links, name='cadastrar_links'),
    path('editar/link/<int:pk>/', LinksUpdate.as_view(), name='editar_links'),
    path('excluir-links/<int:links_id>/', views.excluir_links, name='excluir_links'),
    
    path('listar-perfis/', listar_perfis, name='listar_perfis'),
] 
