# Generated by Django 4.1 on 2023-04-27 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auditoria', '0002_remove_itemchecklist_processo_auditor_cpf_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='nome',
        ),
    ]
