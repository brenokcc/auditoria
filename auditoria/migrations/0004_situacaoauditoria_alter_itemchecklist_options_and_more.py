# Generated by Django 4.1 on 2023-04-27 06:09

from django.db import migrations, models
import django.db.models.deletion
import sloth.core.base
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('auditoria', '0003_remove_checklist_nome'),
    ]

    operations = [
        migrations.CreateModel(
            name='SituacaoAuditoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', sloth.db.models.CharField(max_length=255, verbose_name='Nome')),
                ('cor', sloth.db.models.ColorField(max_length=7, verbose_name='Cor')),
                ('auditavel', models.BooleanField(verbose_name='Auditável')),
            ],
            options={
                'verbose_name': 'Situação de Auditoria',
                'verbose_name_plural': 'Situações de Auditoria',
            },
            bases=(models.Model, sloth.core.base.ModelMixin),
        ),
        migrations.AlterModelOptions(
            name='itemchecklist',
            options={'verbose_name': 'Item', 'verbose_name_plural': 'Itens'},
        ),
        migrations.CreateModel(
            name='Auditoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_prevista_inicio', models.DateField(verbose_name='Data Prevista para Início')),
                ('data_prevista_fim', models.DateField(verbose_name='Data Prevista para Fim')),
                ('data_inicio', models.DateField(null=True, verbose_name='Data de Início')),
                ('data_fim', models.DateField(null=True, verbose_name='Data de Fim')),
                ('lider', sloth.db.models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auditoria.auditor', verbose_name='Líder')),
                ('situacao', sloth.db.models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auditoria.situacaoauditoria', verbose_name='Situação')),
                ('tipo', sloth.db.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auditoria.tipoauditoria', verbose_name='Tipo')),
                ('unidade', sloth.db.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auditoria.unidade', verbose_name='Unidade')),
            ],
            options={
                'verbose_name': 'Auditoria',
                'verbose_name_plural': 'Auditorias',
                'fieldsets': {'Dados Gerais': (('tipo', 'unidade'), ('data_prevista_inicio', 'data_prevista_fim'))},
            },
            bases=(models.Model, sloth.core.base.ModelMixin),
        ),
    ]
