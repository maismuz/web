# Generated by Django 5.2 on 2025-07-16 17:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True, verbose_name='Nome da Categoria')),
                ('descricao', models.TextField(blank=True, help_text='Descrição da categoria', verbose_name='Descrição')),
                ('ativa', models.BooleanField(default=True, help_text='Indica se a categoria está ativa', verbose_name='Ativa')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='BuscaDenuncia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termo', models.CharField(max_length=255, verbose_name='Termo de Busca')),
                ('categoria', models.CharField(blank=True, help_text='Categoria usada no filtro', max_length=20, verbose_name='Categoria Filtrada')),
                ('status', models.CharField(blank=True, help_text='Status usado no filtro', max_length=20, verbose_name='Status Filtrado')),
                ('tipo', models.CharField(blank=True, help_text='Tipo usado no filtro', max_length=20, verbose_name='Tipo Filtrado')),
                ('data_inicial', models.DateField(blank=True, help_text='Data inicial do período filtrado', null=True, verbose_name='Data Inicial')),
                ('data_final', models.DateField(blank=True, help_text='Data final do período filtrado', null=True, verbose_name='Data Final')),
                ('bairro', models.CharField(blank=True, max_length=100, verbose_name='Bairro Filtrado')),
                ('data_busca', models.DateTimeField(auto_now_add=True, verbose_name='Momento da Busca')),
                ('total_resultados', models.PositiveIntegerField(default=0, help_text='Número de resultados encontrados', verbose_name='Total de Resultados')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buscas_denuncias', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Busca de Denúncia',
                'verbose_name_plural': 'Buscas de Denúncias',
                'ordering': ['-data_busca'],
            },
        ),
        migrations.CreateModel(
            name='Denuncia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, verbose_name='Título da Denúncia')),
                ('descricao', models.TextField(help_text='Descreva detalhadamente o problema', verbose_name='Descrição Detalhada')),
                ('tipo', models.CharField(choices=[('infraestrutura', 'Buracos, calçamento, iluminação'), ('seguranca', 'Segurança e ordem pública'), ('meio_ambiente', 'Lixo, poluição, desmatamento'), ('servicos', 'Problemas com serviços públicos'), ('transporte', 'Transporte público'), ('saude', 'Saúde pública'), ('educacao', 'Educação'), ('outro', 'Outro')], default='outro', max_length=20, verbose_name='Tipo de Denúncia')),
                ('prioridade', models.CharField(choices=[('baixa', 'Baixa'), ('normal', 'Normal'), ('alta', 'Alta'), ('urgente', 'Urgente')], default='normal', max_length=10, verbose_name='Prioridade')),
                ('data_ocorrencia', models.DateTimeField(verbose_name='Data e Hora da Ocorrência')),
                ('logradouro_ocorrencia', models.CharField(max_length=255, verbose_name='Rua/Avenida da Ocorrência')),
                ('bairro_ocorrencia', models.CharField(default='Centro', max_length=100, verbose_name='Bairro da Ocorrência')),
                ('ponto_referencia', models.CharField(blank=True, help_text='Ponto de referência próximo (opcional)', max_length=255, verbose_name='Ponto de Referência')),
                ('anexo', models.FileField(blank=True, help_text='Arquivo de imagem ou vídeo (opcional)', null=True, upload_to='denuncias/', verbose_name='Anexar Foto ou Vídeo')),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('em_analise', 'Em Análise'), ('resolvido', 'Resolvido'), ('recusado', 'Recusado')], default='pendente', max_length=20, verbose_name='Status')),
                ('observacoes_internas', models.TextField(blank=True, help_text='Observações para uso interno da administração', verbose_name='Observações Internas')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='denuncias', to='reclamemuz.categoria', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Denúncia',
                'verbose_name_plural': 'Denúncias',
                'ordering': ['-data_criacao'],
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='Texto do Comentário')),
                ('data_hora', models.DateTimeField(auto_now_add=True, verbose_name='Data e Hora')),
                ('eh_publico', models.BooleanField(default=True, help_text='Se marcado, o comentário será visível publicamente', verbose_name='Comentário Público')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_denuncias', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('denuncia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='reclamemuz.denuncia', verbose_name='Denúncia')),
            ],
            options={
                'verbose_name': 'Comentário',
                'verbose_name_plural': 'Comentários',
                'ordering': ['-data_hora'],
            },
        ),
        migrations.CreateModel(
            name='Midia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('imagem', 'Imagem'), ('video', 'Vídeo'), ('documento', 'Documento')], max_length=10, verbose_name='Tipo de Mídia')),
                ('arquivo', models.FileField(help_text='Arquivo de mídia', upload_to='denuncias/midias/', verbose_name='Arquivo')),
                ('url_arquivo', models.URLField(blank=True, help_text='URL externa do arquivo (opcional)', max_length=500, verbose_name='URL do Arquivo')),
                ('descricao', models.CharField(blank=True, help_text='Descrição da mídia (opcional)', max_length=255, verbose_name='Descrição')),
                ('data_upload', models.DateTimeField(auto_now_add=True, verbose_name='Data de Upload')),
                ('denuncia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='midias', to='reclamemuz.denuncia', verbose_name='Denúncia')),
            ],
            options={
                'verbose_name': 'Mídia',
                'verbose_name_plural': 'Mídias',
                'ordering': ['-data_upload'],
            },
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('status_mudou', 'Status da Denúncia Alterado'), ('novo_comentario', 'Novo Comentário'), ('denuncia_resolvida', 'Denúncia Resolvida'), ('lembrete', 'Lembrete'), ('outro', 'Outro')], default='outro', max_length=20, verbose_name='Tipo de Notificação')),
                ('mensagem', models.TextField(verbose_name='Mensagem')),
                ('data_hora', models.DateTimeField(auto_now_add=True, verbose_name='Data e Hora')),
                ('lida', models.BooleanField(default=False, help_text='Indica se a notificação foi lida', verbose_name='Lida')),
                ('denuncia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes', to='reclamemuz.denuncia', verbose_name='Denúncia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Notificação',
                'verbose_name_plural': 'Notificações',
                'ordering': ['-data_hora'],
            },
        ),
    ]
