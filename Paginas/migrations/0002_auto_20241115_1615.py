# Generated by Django 3.0 on 2024-11-15 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paginas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
