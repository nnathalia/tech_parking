# Generated by Django 4.2.11 on 2025-02-03 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0008_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoramento',
            name='status_vaga',
            field=models.CharField(default='Disponível', max_length=20),
        ),
    ]
