# Generated by Django 3.0 on 2024-11-15 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_alter_cliente_data_criacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]