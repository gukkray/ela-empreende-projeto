# Generated by Django 5.1.3 on 2024-11-14 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lojas', '0006_alter_comentario_categoria'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={},
        ),
        migrations.AlterModelOptions(
            name='comentario',
            options={},
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='comentario_resposta',
        ),
        migrations.AlterField(
            model_name='comentario',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='lojas.categoria'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='texto',
            field=models.TextField(),
        ),
    ]
