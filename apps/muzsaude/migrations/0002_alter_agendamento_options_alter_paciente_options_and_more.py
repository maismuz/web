
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion



class Migration(migrations.Migration):

    dependencies = [
        ('muzsaude', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agendamento',
            options={'ordering': ['data_hora_agendada'], 'verbose_name': 'Agendamento', 'verbose_name_plural': 'Agendamentos'},
        ),
        migrations.AlterModelOptions(
            name='paciente',
            options={'ordering': ['nome_completo'], 'verbose_name': 'Paciente', 'verbose_name_plural': 'Pacientes'},
        ),
        migrations.AlterModelOptions(
            name='solicitacao',
            options={'ordering': ['-criado_em'], 'verbose_name': 'Solicitação', 'verbose_name_plural': 'Solicitações'},
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='data_hora_agendada',
            field=models.DateTimeField(verbose_name='Data e Hora Agendada'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='local',
            field=models.CharField(max_length=150, verbose_name='Local'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='observacoes',
            field=models.TextField(blank=True, null=True, verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='solicitacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='muzsaude.solicitacao', verbose_name='Solicitação'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='status_agendamento',
            field=models.CharField(choices=[('agendado', 'Agendado'), ('realizado', 'Realizado'), ('cancelado', 'Cancelado')], default='agendado', max_length=20, verbose_name='Status do Agendamento'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='consentimento_lgpd',
            field=models.BooleanField(default=False, verbose_name='Consentimento LGPD'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='cpf',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('^\\d{11}$', 'O CPF deve conter 11 dígitos.')], verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='data_nascimento',
            field=models.DateField(verbose_name='Data de Nascimento'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='endereco',
            field=models.TextField(verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='historico',
            field=models.TextField(blank=True, null=True, verbose_name='Histórico Médico'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nome_completo',
            field=models.CharField(max_length=150, verbose_name='Nome Completo'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefone',
            field=models.CharField(max_length=20, verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='arquivos',
            field=models.FileField(blank=True, null=True, upload_to='documentos/', verbose_name='Arquivos'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='descricao',
            field=models.TextField(verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='especialidade',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Especialidade'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes', to='muzsaude.paciente', verbose_name='Paciente'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('analise', 'Em Análise'), ('agendado', 'Agendado'), ('concluido', 'Concluído')], default='pendente', max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='tipo',
            field=models.CharField(choices=[('consulta', 'Consulta'), ('cirurgia', 'Cirurgia'), ('transporte', 'Transporte')], max_length=20, verbose_name='Tipo de Solicitação'),
        ),
    ]
