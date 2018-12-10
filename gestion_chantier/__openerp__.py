# -*- coding: utf-8 -*-
{

	'name' : 'Gestion de suivi de Chantiers',
	'author' : 'Serigne Diagne & Fatou Dieng',
	'version' : '0.1',
	'description' : 'Module de gestion de suivi de chantiers',
	'category' : 'Project Management',
	'summary' : 'Chantiers',
	'sequence' : 1,
	'depends' : ['base','project','project_issue'],
	'data' : [
		'views/gestion_chantier_view.xml',
        #progression
		'views/task_lifeline_view.xml',
		'views/progress_bar_view.xml',
        'views/progress_bar_settings.xml',
		#rapport
		'views/wizard_report.xml',
        'views/project_report_pdf_view.xml',
        'views/project_report_button.xml',
        'views/project_report.xml',

	],
	'installable' : True,
	'application' : False,
	'auto_install' : False,
	
}
