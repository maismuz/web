

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doamuz', '0002_remove_solicitacao_nome_solicitacao_contato_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacao',
            name='descricao',
            field=models.TextField(help_text='Descrição completa'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='prazo',
            field=models.DateField(blank=True, help_text='Prazo', null=True),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='titulo',
            field=models.TextField(help_text='Título'),
        ),
    ]
