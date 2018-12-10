# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _


class SelectColor(models.Model):
    _name = "set.progressbar.color"
    _rec_name = 'color'

    range_start = fields.Integer(string='Range From', required=True, help="Starting range")
    range_stop = fields.Integer(string='Range To', required=True, help="Stop range")
    color = fields.Selection([('red', 'Rouge'), ('green', 'Vert'), ('yellow', 'Jaune'),
                             ('pink', 'Rose'), ('orange', 'Orange'),
                             ('light_green', 'Verte Claire'), ('grey', 'Gris'),
                              ('blue', 'Bleu'), ('purple', 'Violet'),
                              ('black', 'Noir'), ('brown', 'Brun')],
                             string='Couleur', required=True, default='red',
                             help="Choose a color for selected range")

    @api.multi
    def assign_progress_bar_color(self):
        values = self.env['set.progressbar.color'].search([])
        list_ret = []
        for value in values:
            list_temp = []
            list_temp.append(value.range_start)
            list_temp.append(value.range_stop)
            list_temp.append(value.color)
            list_ret.append(list_temp)
        return list_ret

    @api.multi
    @api.constrains('range_start', 'range_stop')
    def check_range(self):
        if self.range_start > self.range_stop:
            raise exceptions.ValidationError("Start range should be less than stop range")
