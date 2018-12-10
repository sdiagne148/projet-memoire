# -*- coding: utf-8 -*-

from openerp import fields, models, api, exceptions, _
from dateutil.relativedelta import relativedelta

class EquipeChantier(models.Model):

    _name = 'gestion_chantier.team'

    code=fields.Char('Code')
    name = fields.Char('Nom')
    type_activity = fields.Char("Type d'activite")
    user_id = fields.Many2one('res.users', 'Responsable')
    active = fields.Boolean('Active') 
    team_members = fields.Many2many('res.users', 'project_team_user_rel','team_id', 'uid', "Membres de l'equipe",
                                    help="""Les membres sont des utilisateurs 
                                    qui peuvent effectuer des taches sur le projet.""")

class  Chantier(models.Model):

    _inherit = 'project.project'
	
    
       
    #Colonnes
    lieu = fields.Char(string='Lieu', required=True, readonly=False)
    members_ids = fields.Many2many('res.users', 'project_user_rel', 'project_id','uid', 'Intervenats', 
								    help="""Ce sont des utilisateurs qui peuvent effectuer des taches sur le projet.""",
                                    states={'close': [('readonly', True)],'cancelled': [('readonly', True)]})
    #team_id = fields.Many2one('crm.team', string="Equiqe Project")
    
   
    @api.onchange('team_id')
    def get_team_members(self):
        self.members_ids = [(6, 0, [rec.id for rec in self.team_id.team_members])]


class TaskChantier(models.Model):
    _inherit = 'project.task'

    lifeline = fields.Float(string="Progression de la tache", default='100', copy=False, readonly=True)
    date_deadline = fields.Datetime('Date limite', required=True)

    def process_lifeline_scheduler(self, cr, uid, context=None):
        task_obj = self.pool.get('project.task')
        task_ids = task_obj.search(cr, uid, [])
        time_now = fields.Datetime.from_string(fields.Datetime.now())
        for task_id in task_ids:
            task = task_obj.browse(cr, uid, task_id, context=context)
            start_date = fields.Datetime.from_string(task.date_assign)
            end_date = fields.Datetime.from_string(task.date_deadline)
            if task.stage_id and (task.stage_id.name == 'Done' or task.stage_id.name == 'Cancelled'):
                task.lifeline = 0
            else:
                if task.date_deadline and task.date_assign and end_date > start_date:
                    if time_now < end_date:
                        total_difference_days = relativedelta(end_date, start_date)
                        difference_minute = total_difference_days.hours * 60 + total_difference_days.minutes
                        date_difference = end_date - start_date
                        total_difference_minute = int(date_difference.days) * 24 * 60 + difference_minute

                        remaining_days = relativedelta(time_now, start_date)
                        remaining_minute = remaining_days.hours * 60 + remaining_days.minutes
                        date_remaining = time_now - start_date
                        total_minute_remaining = int(date_remaining.days) * 24 * 60 + remaining_minute
                        if total_difference_minute != 0:
                            task.lifeline = (100 - ((total_minute_remaining * 100) / total_difference_minute))
                        else:
                            task.lifeline = 0
                    else:
                        task.lifeline = 0
