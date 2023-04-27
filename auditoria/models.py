from sloth.db import models, role, meta

ADM = 'Administrador'


class MacroProcessoManager(models.Manager):
    def all(self):
        return self.display('nome', 'get_processos')


class MacroProcesso(models.Model):
    nome = models.CharField('Nome')
    objects = MacroProcessoManager()

    class Meta:
        icon = 'card-text'
        verbose_name = 'Macroprocesso'
        verbose_name_plural = 'Macroprocessos'

    def __str__(self):
        return self.nome

    def get_dados_gerais(self):
        return self.value_set('nome')

    def get_processos(self):
        return self.processo_set.related_field('macroprocesso')

    def view(self):
        return self.value_set('get_dados_gerais', 'get_processos')

    def has_permission(self, user):
        return user.is_superuser


class ProcessoManager(models.Manager):
    def all(self):
        return self


class Processo(models.Model):
    nome = models.CharField('Nome')
    macroprocesso = models.ForeignKey(MacroProcesso, verbose_name='Macroprocesso')

    objects = ProcessoManager()

    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
        select_fields = 'nome', 'macroprocesso'

    def __str__(self):
        return self.nome

    def view(self):
        return self.value_set('nome', 'macroprocesso')

    def has_permission(self, user):
        return user.is_superuser


class UnidadeManager(models.Manager):
    def all(self):
        return self


class Unidade(models.Model):
    nome = models.CharField('Nome')
    objects = UnidadeManager()

    class Meta:
        icon = 'building'
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.nome

    def has_permission(self, user):
        return user.is_superuser


class AuditorManager(models.Manager):
    def all(self):
        return self


class Auditor(models.Model):
    cpf = models.BrCpfField('CPF')
    nome = models.CharField('Nome')

    objects = AuditorManager()

    class Meta:
        icon = 'person-check'
        verbose_name = 'Auditor'
        verbose_name_plural = 'Auditores'

    def __str__(self):
        return self.nome

    def has_permission(self, user):
        return user.is_superuser

class TipoAuditoriaManager(models.Manager):
    def all(self):
        return self


class TipoAuditoria(models.Model):
    nome = models.CharField('Nome')
    objects = TipoAuditoriaManager()

    class Meta:
        verbose_name = 'Tipo de Auditoria'
        verbose_name_plural = 'Tipos de Auditorias'

    def __str__(self):
        return self.nome

    def has_permission(self, user):
        return user.is_superuser


class ChecklistManager(models.Manager):
    def all(self):
        return self.display('processo', 'descricao', 'get_numero_itens')


class Checklist(models.Model):
    processo = models.ForeignKey(Processo, verbose_name='Processo')
    descricao = models.TextField('Descrição', null=True, blank=True)
    objects = ChecklistManager()

    class Meta:
        icon = 'card-checklist'
        verbose_name = 'Checklist'
        verbose_name_plural = 'Checklist'

    def __str__(self):
        return '{} - {}'.format(self.id, self.processo)

    def get_dados_gerais(self):
        return self.value_set('processo', 'descricao')

    def get_itens(self):
        return self.itemchecklist_set.related_field('checklist').display('descricao').accordion()

    @meta('Número de Itens', renderer='badges/primary')
    def get_numero_itens(self):
        return self.get_itens().count()

    def view(self):
        return self.value_set('get_dados_gerais', 'get_itens')

    def has_permission(self, user):
        return user.is_superuser


class ItemChecklistManager(models.Manager):
    def all(self):
        return self


class ItemChecklist(models.Model):
    checklist = models.ForeignKey(Checklist, verbose_name='Checklist')
    enunciado = models.CharField('Enunciado')
    descricao = models.TextField('Descrição')

    objects = ItemChecklistManager()

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

    def __str__(self):
        return self.enunciado

    def has_permission(self, user):
        return user.is_superuser

class SituacaoAuditoriaManager(models.Manager):
    def all(self):
        return self


class SituacaoAuditoria(models.Model):
    nome = models.CharField('Nome')
    cor = models.ColorField('Cor')
    auditavel = models.BooleanField('Auditável')

    objects = SituacaoAuditoriaManager()

    class Meta:
        verbose_name = 'Situação de Auditoria'
        verbose_name_plural = 'Situações de Auditoria'

    def __str__(self):
        return self.nome

    def has_permission(self, user):
        return user.is_superuser


class AuditoriaManager(models.Manager):
    def all(self):
        return self.display('tipo', 'unidade', 'data_prevista_inicio', 'data_inicio', 'lider', 'get_situacao')

    def programadas(self):
        return self.filter(data_inicio__isnull=True)

    def em_andamento(self):
        return self.filter(data_inicio__isnull=False, data_fim__isnull=True)

    def get_total_por_tipo(self):
        return self.count('tipo')

    def get_total_por_situacao(self):
        return self.count('situacao')

class Auditoria(models.Model):
    tipo = models.ForeignKey(TipoAuditoria, verbose_name='Tipo')
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade')
    data_prevista_inicio = models.DateField('Data Prevista para Início')
    data_prevista_fim = models.DateField('Data Prevista para Fim')

    data_inicio = models.DateField('Data de Início', null=True)
    data_fim = models.DateField('Data de Fim', null=True)

    lider = models.ForeignKey(Auditor, verbose_name='Líder', null=True)
    situacao = models.ForeignKey(SituacaoAuditoria, verbose_name='Situação', null=True)

    objects = AuditoriaManager()

    class Meta:
        icon = 'file-earmark-check'
        verbose_name = 'Auditoria'
        verbose_name_plural = 'Auditorias'
        fieldsets = {
            'Dados Gerais': (('tipo', 'unidade'), ('data_prevista_inicio', 'data_prevista_fim')),
        }

    def get_dados_gerais(self):
        return self.value_set(('tipo', 'unidade'), ('lider', 'get_situacao'))

    def get_datas(self):
        return self.value_set(('data_prevista_inicio', 'data_prevista_fim'), ('data_inicio', 'data_fim')).actions('iniciar_auditoria')

    @meta('Situação', renderer='badges/badge')
    def get_situacao(self):
        return self.situacao.cor, self.situacao.nome

    def get_checklists(self):
        return self.checklistauditoria_set.related_field('auditoria').accordion().actions('view').expand()

    def view(self):
        return self.value_set('get_dados_gerais', 'get_datas', 'get_checklists')

    def __str__(self):
        return 'Auditoria {} - {}'.format(self.tipo, self.unidade)

    def save(self, *args, **kwargs):
        if self.situacao_id is None:
            self.situacao = SituacaoAuditoria.objects.get(nome='Programada')
        super().save(*args, **kwargs)

    def has_permission(self, user):
        return user.is_superuser


class ChecklistAuditoriaManager(models.Manager):
    def all(self):
        return self


class ChecklistAuditoria(models.Model):
    auditoria = models.ForeignKey(Auditoria, verbose_name='Auditoria')
    checklist = models.ForeignKey(Checklist, verbose_name='Checklist')
    responsavel = models.ForeignKey(Auditor, verbose_name='Responsável')
    prazo_final = models.DateField('Prazo Final')

    objects = ChecklistAuditoriaManager()

    class Meta:
        verbose_name = 'Checklist'
        verbose_name_plural = 'Checklist'

    def __str__(self):
        return '{} ({})'.format(self.checklist, self.responsavel)

    def get_dados_gerais(self):
        return self.value_set('auditoria', ('responsavel', 'prazo_final'))

    @meta('Quesitos')
    def get_itens(self):
        return self.itemauditoria_set.display('evidencias', 'get_parecer').actions('auditar').filters('parecer').accordion().expand().preview('get_anexos', icon='files')

    @meta('Total por Parecer')
    def get_total_itens_por_parecer(self):
        return self.itemauditoria_set.get_total_por_parecer().bar_chart()

    def view(self):
        return self.value_set('get_dados_gerais', 'get_itens').append('get_total_itens_por_parecer')

    def has_permission(self, user):
        return user.is_superuser

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for item in self.checklist.itemchecklist_set.all():
            dados = dict(checklist_auditoria=self, item=item)
            if not ItemAuditoria.objects.filter(**dados):
                ItemAuditoria.objects.create(**dados)


class ParecerManager(models.Manager):
    def all(self):
        return self


class Parecer(models.Model):
    nome = models.CharField('Nome')
    cor = models.ColorField('Cor')

    objects = ParecerManager()

    class Meta:
        verbose_name = 'Parecer'
        verbose_name_plural = 'Pareceres'

    def __str__(self):
        return self.nome

    def has_permission(self, user):
        return user.is_superuser


class AnexoManager(models.Manager):
    def all(self):
        return self


class Anexo(models.Model):
    nome = models.CharField('Nome')
    arquivo = models.FileField('Arquivo', upload_to='anexos')

    objects = AnexoManager()

    class Meta:
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'

    def __str__(self):
        return '{}'.format(self.pk)

    def has_permission(self, user):
        return user.is_superuser


class ItemAuditoriaManager(models.Manager):
    def all(self):
        return self

    def get_total_por_parecer(self):
        return self.count('parecer')


class ItemAuditoria(models.Model):
    checklist_auditoria = models.ForeignKey(ChecklistAuditoria, verbose_name='Checklist')
    item = models.ForeignKey(ItemChecklist, verbose_name='Enunciado')
    evidencias = models.TextField('Evidências', null=True, blank=True)
    parecer = models.ForeignKey(Parecer, null=True, blank=True)
    anexos = models.OneToManyField(Anexo, verbose_name='Anexos', min=0, max=5)

    objects = ItemAuditoriaManager()

    class Meta:
        verbose_name = 'Quesito'
        verbose_name_plural = 'Quesitos'

    def __str__(self):
        return '{}'.format(self.item)

    def has_permission(self, user):
        return user.is_superuser

    @meta('Parecer', renderer='badges/badge')
    def get_parecer(self):
        return (self.parecer.cor, self.parecer.nome) if self.parecer_id else None

    @meta('Anexos', renderer='images/group')
    def get_anexos(self):
        return [(a.nome, a.arquivo.url) for a in self.anexos.all()]