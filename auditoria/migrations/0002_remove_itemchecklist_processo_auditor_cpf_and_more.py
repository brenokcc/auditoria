# Generated by Django 4.1 on 2023-04-27 05:39

from django.db import migrations
import django.db.models.deletion
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('auditoria', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemchecklist',
            name='processo',
        ),
        migrations.AddField(
            model_name='auditor',
            name='cpf',
            field=sloth.db.models.BrCpfField(default=None, max_length=255, verbose_name='CPF'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auditor',
            name='nome',
            field=sloth.db.models.CharField(default=None, max_length=255, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklist',
            name='processo',
            field=sloth.db.models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auditoria.processo', verbose_name='Processo'),
            preserve_default=False,
        ),
    ]
