{
    'name':"Todo App",
    'author':"Mahmoud Ehab",
    'category':'',
    'version':'18.0.0.1.0',
    'depends':[
        'base','mail'
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_menu.xml',
        'data/todo_sequence.xml',
        'reports/task_report.xml'
    ],
    'application':True,
    'license':'LGPL-3',
}