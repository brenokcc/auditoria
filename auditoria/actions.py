from sloth import actions


class IniciarAuditoria(actions.Action):
    class Meta:
        verbose_name = 'Iniciar Auditoria'
        modal = True
        style = 'primary'
        model = 'auditoria.auditoria'
        fields = 'lider', 'data_inicio'

    def submit(self):
        self.instance.situacao = self.objects('auditoria.situacaoauditoria').get(nome='Execução')
        super().submit()

    def has_permission(self, user):
        return self.instance.data_inicio is None

class Auditar(actions.Action):
    class Meta:
        icon = 'check2-all'
        verbose_name = 'Auditar'
        modal = True
        style = 'success'
        model = 'auditoria.itemauditoria'
        fields = 'evidencias', 'parecer', 'anexos'

    def view(self):
        self.info(self.instance.item.descricao)

    def submit(self):
        super().submit()
