from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Usuario, Servico, VagaEmprego, Candidatura, Avaliacao
from .forms import UsuarioForm, ServicoForm


def inicial(request):
    """Página inicial da aplicação"""
    # Busca os últimos serviços para exibir na home
    servicos_recentes = Servico.objects.all()[:6]
    total_servicos = Servico.objects.count()
    total_prestadores = Usuario.objects.filter(eh_prestador=True).count()
    
    context = {
        'servicos_recentes': servicos_recentes,
        'total_servicos': total_servicos,
        'total_prestadores': total_prestadores,
    }
    return render(request, 'contratamuz/index.html', context)


def listar_vagas(request):
    """Página de listagem de vagas de emprego"""
    vagas = VagaEmprego.objects.filter(ativa=True).order_by('-criado_em')
    
    # Filtro por categoria
    categoria = request.GET.get('categoria')
    if categoria and categoria != 'todos':
        vagas = vagas.filter(categoria=categoria)
    
    # Filtro por busca
    busca = request.GET.get('busca')
    if busca:
        vagas = vagas.filter(
            Q(titulo__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(localizacao__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(vagas, 12)  # 12 vagas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categoria_selecionada': categoria,
        'busca': busca,
        'total_vagas': vagas.count(),
    }
    return render(request, 'contratamuz/listar_vagas.html', context)


def listar_servicos(request):
    """Página de listagem de serviços com filtros"""
    servicos = Servico.objects.all()
    
    # Filtro por categoria
    categoria = request.GET.get('categoria')
    if categoria and categoria != 'todos':
        servicos = servicos.filter(categoria=categoria)
    
    # Filtro por busca
    busca = request.GET.get('busca')
    if busca:
        servicos = servicos.filter(
            Q(titulo__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(usuario__nome__icontains=busca) |
            Q(usuario__cidade__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(servicos, 12)  # 12 serviços por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Categorias para o filtro
    categorias = Servico.CATEGORIAS_CHOICES
    
    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'categoria_selecionada': categoria,
        'busca': busca,
        'total_servicos': servicos.count(),
    }
    return render(request, 'contratamuz/servicos.html', context)


def detalhe_servico(request, servico_id):
    """Retorna detalhes do serviço em JSON para o modal"""
    servico = get_object_or_404(Servico, id=servico_id)
    
    data = {
        'id': servico.id,
        'titulo': servico.titulo,
        'descricao': servico.descricao,
        'categoria': servico.get_categoria_display(),
        'categoria_icon': servico.get_categoria_display_icon(),
        'telefone_contato': servico.telefone_contato or servico.contato,
        'imagem_url': servico.imagem_url,
        'prestador': {
            'nome': servico.usuario.nome,
            'cidade': servico.usuario.cidade,
            'telefone': servico.usuario.telefone,
            'biografia': servico.usuario.biografia,
            'imagem_url': servico.usuario.imagem_url,
            'eh_empresa': servico.usuario.eh_empresa,
        },
        'created_at': (servico.created_at or servico.criado_em).strftime('%d/%m/%Y') if (servico.created_at or servico.criado_em) else '',
    }
    
    return JsonResponse(data)


def publicar_servico(request):
    """Página para publicar um novo serviço"""
    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            # Por enquanto, vamos criar um usuário padrão se não existir
            # Em uma implementação real, isso seria baseado no usuário logado
            usuario, created = Usuario.objects.get_or_create(
                nome='Usuário Padrão',
                defaults={
                    'cidade': 'São Paulo',
                    'telefone': '(11) 99999-9999',
                    'biografia': 'Prestador de serviços',
                }
            )
            
            servico = form.save(commit=False)
            servico.usuario = usuario
            servico.save()
            
            messages.success(request, 'Serviço publicado com sucesso!')
            return redirect('listar_servicos')
    else:
        form = ServicoForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contratamuz/publicar_servico.html', context)


def sobre(request):
    """Página sobre a plataforma"""
    return render(request, 'contratamuz/sobre.html')


def contato(request):
    """Página de contato"""
    return render(request, 'contratamuz/contato.html')


# Views de Autenticação

def login_view(request):
    """View para login de usuários"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {user.first_name or user.username}!')
                
                # Redirecionar para a página solicitada ou home
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return render(request, 'contratamuz/auth/login.html')


def register_view(request):
    """View para registro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        # Dados do usuário Django
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Dados do perfil
        nome = request.POST.get('nome')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        biografia = request.POST.get('biografia')
        eh_empresa = request.POST.get('eh_empresa') == 'on'
        eh_prestador = request.POST.get('eh_prestador') == 'on'
        
        # Validações
        if not all([username, email, password, password_confirm, nome]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
        elif password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
        elif len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
        else:
            try:
                # Criar usuário Django
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Criar perfil do usuário
                usuario = Usuario.objects.create(
                    user=user,
                    nome=nome,
                    cidade=cidade or '',
                    telefone=telefone or '',
                    biografia=biografia or '',
                    eh_empresa=eh_empresa,
                    eh_prestador=eh_prestador
                )
                
                # Fazer login automático
                login(request, user)
                messages.success(request, f'Conta criada com sucesso! Bem-vindo, {nome}!')
                return redirect('index')
                
            except Exception as e:
                messages.error(request, 'Erro ao criar conta. Tente novamente.')
    
    return render(request, 'contratamuz/auth/register.html')


def logout_view(request):
    """View para logout de usuários"""
    if request.user.is_authenticated:
        nome = request.user.first_name or request.user.username
        logout(request)
        messages.success(request, f'Até logo, {nome}! Você foi desconectado com sucesso.')
    
    return redirect('index')


@login_required
def perfil_view(request):
    """View para visualizar e editar perfil do usuário"""
    try:
        usuario = request.user.usuario
    except Usuario.DoesNotExist:
        # Criar perfil se não existir
        usuario = Usuario.objects.create(
            user=request.user,
            nome=request.user.get_full_name() or request.user.username,
            cidade='',
            telefone='',
            biografia=''
        )
    
    if request.method == 'POST':
        # Atualizar dados do User
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Atualizar dados do Usuario
        usuario.nome = request.POST.get('nome', '')
        usuario.cidade = request.POST.get('cidade', '')
        usuario.telefone = request.POST.get('telefone', '')
        usuario.biografia = request.POST.get('biografia', '')
        usuario.eh_empresa = request.POST.get('eh_empresa') == 'on'
        usuario.eh_prestador = request.POST.get('eh_prestador') == 'on'
        
        # Upload de imagem
        if 'imagem' in request.FILES:
            usuario.imagem = request.FILES['imagem']
        
        usuario.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    
    context = {
        'usuario': usuario,
    }
    return render(request, 'contratamuz/auth/perfil.html', context)


@login_required
def meus_servicos_view(request):
    """View para listar serviços do usuário logado"""
    try:
        usuario = request.user.usuario
        servicos = Servico.objects.filter(usuario=usuario).order_by('-id')
    except Usuario.DoesNotExist:
        servicos = []
    
    context = {
        'servicos': servicos,
    }
    return render(request, 'contratamuz/auth/meus_servicos.html', context)


def publicar_servico_auth(request):
    """Página para publicar um novo serviço (versão com autenticação)"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Você precisa estar logado para publicar um serviço.')
        return redirect('login')
    
    try:
        usuario = request.user.usuario
    except Usuario.DoesNotExist:
        messages.error(request, 'Você precisa completar seu perfil antes de publicar serviços.')
        return redirect('perfil')
    
    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.usuario = usuario
            servico.save()
            
            messages.success(request, 'Serviço publicado com sucesso!')
            return redirect('meus_servicos')
    else:
        form = ServicoForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contratamuz/publicar_servico.html', context)

