# Generated manually to fix telefone_contato field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratamuz', '0003_alter_servico_options_alter_usuario_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='telefone_contato',
            field=models.CharField(blank=True, max_length=20, verbose_name='Telefone de Contato'),
        ),
    ]
