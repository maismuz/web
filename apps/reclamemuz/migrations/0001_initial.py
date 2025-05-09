# Generated by Django 5.2 on 2025-05-07 17:35

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
            name='Denuncia',
            fields=[
                ('id_denuncia', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('categoria', models.CharField(choices=[('buraco', 'Buraco no Asfalto'), ('lixo', 'Lixo'), ('iluminacao', 'Iluminação')], max_length=20)),
                ('endereco', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('data_ocorrencia', models.DateField()),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('resolvido', 'Resolvido'), ('ignorado', 'Ignorado')], default='pendente', max_length=10)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
