{
    'name': 'HR Hospital',
    'version': '19.0.1.0.0',
    'summary': 'Модуль для автоматизації лікарні: облік лікарів та пацієнтів',
    'description': """
        Модуль для ведення обліку лікарів, пацієнтів,
        видів захворювань та візитів у лікарні.

        У цій версії додано:
        - довідник кваліфікацій лікарів (категорії лікарів);
        - історію персональних лікарів пацієнтів;
        - абстрактну модель загальної медичної інформації
          (група крові, стать, дата народження, вік);
        - категорію, ментора та ознаку "інтерн" для лікарів;
        - ієрархічну структуру видів захворювань;
        - розширені поля та правила для візитів пацієнтів;
        - візарди масового перевизначення лікаря та звіту по візитах.
    """,
    'author': 'Hospital Management',
    'category': 'Healthcare',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_hospital_doctor_category_data.xml',
        'data/hr_hospital_disease_data.xml',
        'views/hr_hospital_doctor_category_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_doctor_history_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/mass_reassign_doctor_wizard_views.xml',
        'views/visit_report_wizard_views.xml',
        'views/hr_hospital_menu.xml',
    ],
    'demo': [
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_doctor_history_demo.xml',
        'demo/hr_hospital_disease_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
