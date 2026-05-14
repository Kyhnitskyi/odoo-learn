{
    'name': 'HR Hospital',
    'version': '19.0.1.0.0',
    'summary': 'Модуль для автоматизації лікарні: облік лікарів та пацієнтів',
    'description': """
        Модуль для ведення обліку лікарів, пацієнтів,
        видів захворювань та візитів у лікарні.
    """,
    'author': 'Hospital Management',
    'category': 'Healthcare',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_hospital_disease_data.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_menu.xml',
    ],
    'demo': [
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
