{
    "name": "Purchase Order Approval",
    "summary": "",
    "version": "11.0.1.0.0",
    "category": "Purchases",
    "website": "",
    "author": "",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base","purchase",
    ],
    "data": [
        "security/po_director_group.xml",
        "views/res_company_view.xml",
        "views/purchase_order_view.xml",
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'uninstall_hook': "uninstall_hook",
    'css': [''],
    'installable': True,
    'auto_install': False,
}
