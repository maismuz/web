from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Usuario, Servico, VagaEmprego, Candidatura, Avaliacao


class UsuarioModelTest(TestCase):
    """Testes para o modelo Usuario"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.usuario = Usuario.objects.create(
            user=self.user,
            nome='Usuário Teste',
            cidade='São Paulo',
            telefone='(11) 99999-9999',
            biografia='Biografia de teste',
            eh_empresa=False,
            eh_prestador=True
        )
    
    def test_usuario_creation(self):
        """Testa a criação de um usuário"""
        self.assertEqual(self.usuario.nome, 'Usuário Teste')
        self.assertEqual(self.usuario.cidade, 'São Paulo')
        self.assertEqual(self.usuario.telefone, '(11) 99999-9999')
        self.assertFalse(self.usuario.eh_empresa)
        self.assertTrue(self.usuario.eh_prestador)
    
    def test_usuario_str(self):
        """Testa a representação string do usuário"""
        self.assertEqual(str(self.usuario), 'Usuário Teste')
    
    def test_imagem_url_property(self):
        """Testa a propriedade imagem_url"""
        self.assertEqual(self.usuario.imagem_url, '/static/img/default-user.svg')


class ServicoModelTest(TestCase):
    """Testes para o modelo Servico"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.usuario = Usuario.objects.create(
            user=self.user,
            nome='Prestador Teste',
            cidade='Rio de Janeiro',
            telefone='(21) 88888-8888',
            eh_prestador=True
        )
        self.servico = Servico.objects.create(
            titulo='Aulas de Violão',
            descricao='Aulas particulares de violão para iniciantes e intermediários',
            categoria='musica',
            telefone_contato='(21) 88888-8888',
            usuario=self.usuario
        )
    
    def test_servico_creation(self):
        """Testa a criação de um serviço"""
        self.assertEqual(self.servico.titulo, 'Aulas de Violão')
        self.assertEqual(self.servico.categoria, 'musica')
        self.assertEqual(self.servico.usuario, self.usuario)
    
    def test_servico_str(self):
        """Testa a representação string do serviço"""
        self.assertEqual(str(self.servico), 'Aulas de Violão')
    
    def test_descricao_curta_property(self):
        """Testa a propriedade descricao_curta"""
        # Descrição curta
        self.assertEqual(self.servico.descricao_curta, self.servico.descricao)
        
        # Descrição longa
        descricao_longa = 'A' * 150
        self.servico.descricao = descricao_longa
        self.assertEqual(len(self.servico.descricao_curta), 103)  # 100 + '...'
    
    def test_get_categoria_display_icon(self):
        """Testa o método get_categoria_display_icon"""
        self.assertEqual(self.servico.get_categoria_display_icon(), 'music')


class AuthViewsTest(TestCase):
    """Testes para as views de autenticação"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='João',
            last_name='Silva'
        )
        self.usuario = Usuario.objects.create(
            user=self.user,
            nome='João Silva',
            cidade='São Paulo',
            telefone='(11) 99999-9999'
        )
    
    def test_login_view_get(self):
        """Testa o acesso à página de login"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_login_view_post_success(self):
        """Testa login com credenciais válidas"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('index'))
    
    def test_login_view_post_invalid(self):
        """Testa login com credenciais inválidas"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário ou senha incorretos')
    
    def test_register_view_get(self):
        """Testa o acesso à página de registro"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cadastro')
    
    def test_register_view_post_success(self):
        """Testa registro com dados válidos"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'nome': 'Maria Santos',
            'cidade': 'Rio de Janeiro',
            'telefone': '(21) 88888-8888',
            'biografia': 'Nova usuária',
            'eh_prestador': 'on'
        })
        self.assertRedirects(response, reverse('index'))
        
        # Verifica se o usuário foi criado
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Usuario.objects.filter(nome='Maria Santos').exists())
    
    def test_register_view_post_password_mismatch(self):
        """Testa registro com senhas diferentes"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'differentpass',
            'nome': 'Maria Santos',
            'cidade': 'Rio de Janeiro',
            'telefone': '(21) 88888-8888'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'As senhas não coincidem')
    
    def test_logout_view(self):
        """Testa logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
    
    def test_perfil_view_authenticated(self):
        """Testa acesso ao perfil com usuário autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')
    
    def test_perfil_view_unauthenticated(self):
        """Testa acesso ao perfil sem autenticação"""
        response = self.client.get(reverse('perfil'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('perfil')}")
    
    def test_meus_servicos_view_authenticated(self):
        """Testa acesso aos serviços do usuário autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('meus_servicos'))
        self.assertEqual(response.status_code, 200)


class MainViewsTest(TestCase):
    """Testes para as views principais"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.usuario = Usuario.objects.create(
            user=self.user,
            nome='Prestador Teste',
            cidade='São Paulo',
            telefone='(11) 99999-9999',
            eh_prestador=True
        )
        self.servico = Servico.objects.create(
            titulo='Serviço Teste',
            descricao='Descrição do serviço teste',
            categoria='tecnologia',
            telefone_contato='(11) 99999-9999',
            usuario=self.usuario
        )
    
    def test_inicial_view(self):
        """Testa a página inicial"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ContrataMuz')
    
    def test_listar_servicos_view(self):
        """Testa a listagem de serviços"""
        response = self.client.get(reverse('listar_servicos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Serviço Teste')
    
    def test_listar_servicos_with_filter(self):
        """Testa a listagem de serviços com filtro"""
        response = self.client.get(reverse('listar_servicos'), {'categoria': 'tecnologia'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Serviço Teste')
    
    def test_listar_servicos_with_search(self):
        """Testa a listagem de serviços com busca"""
        response = self.client.get(reverse('listar_servicos'), {'busca': 'Teste'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Serviço Teste')
    
    def test_detalhe_servico_view(self):
        """Testa a view de detalhes do serviço"""
        response = self.client.get(reverse('detalhe_servico', args=[self.servico.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Verifica se o JSON contém os dados esperados
        data = response.json()
        self.assertEqual(data['titulo'], 'Serviço Teste')
        self.assertEqual(data['categoria'], 'Tecnologia')
    
    def test_publicar_servico_auth_unauthenticated(self):
        """Testa publicação de serviço sem autenticação"""
        response = self.client.get(reverse('publicar_servico_auth'))
        self.assertRedirects(response, reverse('login'))
    
    def test_publicar_servico_auth_authenticated(self):
        """Testa publicação de serviço com autenticação"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('publicar_servico_auth'))
        self.assertEqual(response.status_code, 200)


class VagaEmpregoModelTest(TestCase):
    """Testes para o modelo VagaEmprego"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='empresa',
            email='empresa@example.com',
            password='testpass123'
        )
        self.usuario = Usuario.objects.create(
            user=self.user,
            nome='Empresa Teste',
            cidade='São Paulo',
            telefone='(11) 99999-9999',
            eh_empresa=True
        )
        self.vaga = VagaEmprego.objects.create(
            titulo='Desenvolvedor Python',
            descricao='Vaga para desenvolvedor Python júnior',
            salario=5000.00,
            localizacao='São Paulo',
            categoria='tecnologia',
            usuario=self.usuario
        )
    
    def test_vaga_creation(self):
        """Testa a criação de uma vaga"""
        self.assertEqual(self.vaga.titulo, 'Desenvolvedor Python')
        self.assertEqual(self.vaga.salario, 5000.00)
        self.assertTrue(self.vaga.ativa)
    
    def test_vaga_str(self):
        """Testa a representação string da vaga"""
        self.assertEqual(str(self.vaga), 'Desenvolvedor Python')


class CandidaturaModelTest(TestCase):
    """Testes para o modelo Candidatura"""
    
    def setUp(self):
        # Criar empresa
        self.user_empresa = User.objects.create_user(
            username='empresa',
            email='empresa@example.com',
            password='testpass123'
        )
        self.empresa = Usuario.objects.create(
            user=self.user_empresa,
            nome='Empresa Teste',
            cidade='São Paulo',
            telefone='(11) 99999-9999',
            eh_empresa=True
        )
        
        # Criar candidato
        self.user_candidato = User.objects.create_user(
            username='candidato',
            email='candidato@example.com',
            password='testpass123'
        )
        self.candidato = Usuario.objects.create(
            user=self.user_candidato,
            nome='Candidato Teste',
            cidade='São Paulo',
            telefone='(11) 88888-8888'
        )
        
        # Criar vaga
        self.vaga = VagaEmprego.objects.create(
            titulo='Desenvolvedor Python',
            descricao='Vaga para desenvolvedor Python júnior',
            salario=5000.00,
            localizacao='São Paulo',
            categoria='tecnologia',
            usuario=self.empresa
        )
        
        # Criar candidatura
        self.candidatura = Candidatura.objects.create(
            candidato=self.candidato,
            vaga=self.vaga,
            mensagem='Tenho interesse na vaga'
        )
    
    def test_candidatura_creation(self):
        """Testa a criação de uma candidatura"""
        self.assertEqual(self.candidatura.candidato, self.candidato)
        self.assertEqual(self.candidatura.vaga, self.vaga)
        self.assertEqual(self.candidatura.status, 'pendente')
    
    def test_candidatura_str(self):
        """Testa a representação string da candidatura"""
        expected = f"{self.candidato.nome} -> {self.vaga.titulo}"
        self.assertEqual(str(self.candidatura), expected)


class AvaliacaoModelTest(TestCase):
    """Testes para o modelo Avaliacao"""
    
    def setUp(self):
        # Criar prestador
        self.user_prestador = User.objects.create_user(
            username='prestador',
            email='prestador@example.com',
            password='testpass123'
        )
        self.prestador = Usuario.objects.create(
            user=self.user_prestador,
            nome='Prestador Teste',
            cidade='São Paulo',
            telefone='(11) 99999-9999',
            eh_prestador=True
        )
        
        # Criar avaliador
        self.user_avaliador = User.objects.create_user(
            username='avaliador',
            email='avaliador@example.com',
            password='testpass123'
        )
        self.avaliador = Usuario.objects.create(
            user=self.user_avaliador,
            nome='Avaliador Teste',
            cidade='São Paulo',
            telefone='(11) 88888-8888'
        )
        
        # Criar serviço
        self.servico = Servico.objects.create(
            titulo='Aulas de Violão',
            descricao='Aulas particulares de violão',
            categoria='musica',
            telefone_contato='(11) 99999-9999',
            usuario=self.prestador
        )
        
        # Criar avaliação
        self.avaliacao = Avaliacao.objects.create(
            serviço=self.servico,
            avaliador=self.avaliador,
            nota=5,
            comentario='Excelente professor!'
        )
    
    def test_avaliacao_creation(self):
        """Testa a criação de uma avaliação"""
        self.assertEqual(self.avaliacao.serviço, self.servico)
        self.assertEqual(self.avaliacao.avaliador, self.avaliador)
        self.assertEqual(self.avaliacao.nota, 5)
    
    def test_avaliacao_str(self):
        """Testa a representação string da avaliação"""
        expected = f"Avaliação de {self.avaliador.nome} para {self.servico.titulo}"
        self.assertEqual(str(self.avaliacao), expected)

