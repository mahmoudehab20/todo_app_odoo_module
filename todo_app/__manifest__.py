{
    'name':"Todo App",
    'author':"Mahmoud Ehab",
    'category':'',
    'version':'18.0.0.1.0',
    'depends':[
        'base','mail','sale','account','sale_management','stock'
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_menu.xml',
        'data/todo_sequence.xml',
        'reports/task_report.xml',
        'reports/sale_order_report.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'todo_app/static/src/components/ListView/ListView.js',
            'todo_app/static/src/components/ListView/ListView.xml',

        ]
    },
    'application':True,
    'license':'LGPL-3',
}