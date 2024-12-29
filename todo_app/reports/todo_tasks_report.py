from odoo import models,fields,api

class PdfReport(models.AbstractModel):
    _name='report.todo_app.report'

    def get_report_data(self,docids,data=None):
        report=self.env['ir.actions.report']._get_report_from_name('todo_app.task_report_template')
        obj=self.env['todo.tasks'].browse(docids)
        return {
            "lines":docids.get_lines()
        }