# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class ProjectReportButton(models.TransientModel):
    _name = 'wizard.project.report'

    task_select = fields.Boolean(string="Taches", default=True)
    issue_select = fields.Boolean(string="Incidents", default=True)
    partner_select = fields.Many2many('res.users', string='Assigne a')
    stage_select = fields.Many2many('project.task.type', string="Phases")

    @api.multi
    def print_project_report_pdf(self):

        active_record = self._context['active_id']
        record = self.env['project.project'].browse(active_record)
        return self.env['report'].get_action(record, "gestion_chantier.project_report_transition")

    @api.multi
    def print_project_report_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'project.project'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return {'type': 'ir.actions.report.xml',
                'report_name': 'project_report_pdf.project_report_xls.xlsx',
                'datas': datas,
                'name': 'Project Report'
                }
