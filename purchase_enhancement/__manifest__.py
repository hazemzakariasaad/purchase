{
    'name': ' purchase Enhancements',
    'version': '1.0',
    'summary': 'Add custom fields to Sale Order',
    'depends':  ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/Purchase_request.xml',
        'views/rejection_wizard.xml',
        'data/send_mail_temp.xml',
    ],
    # 'installable': True,
    # 'auto_install': False,
    # 'application': True,

}