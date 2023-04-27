from sloth.api.dashboard import Dashboard
from .models import *


class AppDashboard(Dashboard):

    def __init__(self, request):
        super().__init__(request)
        self.styles('/static/css/sloth.css')
        self.scripts('/static/js/sloth.js')
        self.libraries(fontawesome=False, materialicons=False)
        self.web_push_notification(False)
        self.login(title='Auditoria', logo='/static/images/audit.png', mask=None, two_factor=False)
        self.navbar(title='Auditoria', icon='/static/images/audit.png', favicon='/static/images/audit.png')
        self.header(logo='/static/images/audit.png', title='Auditoria', shadow=True)
        self.settings_menu('change_password')
        self.tools_menu('show_icons')
        self.footer(title='© 2023 Auditoria', text='Todos os direitos reservados', version='1.0.0')

        self.shortcuts('auditoria.macroprocesso')
        self.shortcuts('auditoria.unidade')
        self.shortcuts('auditoria.auditor')
        self.shortcuts('auditoria.checklist')
        self.shortcuts('auditoria.auditoria')

    def view(self):
        return self.value_set('get_auditorias_em_andamento', 'get_auditorias_programadas').append('get_total_auditorias_por_tipo', 'get_total_auditorias_por_situacao')

    @meta('Auditorias em Andamento')
    def get_auditorias_em_andamento(self):
        return self.objects('auditoria.auditoria').all().em_andamento().actions('view')

    @meta('Auditorias Programadas')
    def get_auditorias_programadas(self):
        return self.objects('auditoria.auditoria').all().programadas().actions('view').calendar('data_prevista_inicio')

    @meta('Auditorias por Tipo')
    def get_total_auditorias_por_tipo(self):
        return self.objects('auditoria.auditoria').get_total_por_tipo().donut_chart()

    @meta('Auditorias por Situação')
    def get_total_auditorias_por_situacao(self):
        return self.objects('auditoria.auditoria').get_total_por_situacao().donut_chart()
