from odoo import http
from odoo.http import request
import io 
import xlsxwriter
from ast import literal_eval


class XlsxReport(http.Controller):

    @http.route('/todotask/excel/report/<string:task_ids>', type='http',auth='user')
    def xlsx_todo_task_report(self,task_ids):
        task_ids=request.env['todo.task'].browse(literal_eval(task_ids))
        output=io.BytesIO()
        workbook=xlsxwriter.Workbook(output,{'in_memory':True})
        worksheet_tasks=workbook.add_worksheet('Tasks')
        headers_tasks=['Referance','Name','Description','Due Date','Status','Assigned To','Estimated Time']
        for colnum,header in enumerate(headers_tasks):
            worksheet_tasks.write(0,colnum,header)

        row_num=1
        for task_id in task_ids:
            worksheet_tasks.write(row_num,0,task_id.ref)
            worksheet_tasks.write(row_num,1,task_id.name)
            worksheet_tasks.write(row_num,2,task_id.description)
            worksheet_tasks.write(row_num,3,task_id.due_date)
            worksheet_tasks.write(row_num,4,task_id.status)
            worksheet_tasks.write(row_num,5,task_id.assign_to_id.name)
            worksheet_tasks.write(row_num,6,task_id.estimated_time)
            row_num+=1


        workbook.close()
        output.seek(0)
        file_name='Tasks Report.xlsx'
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="{file_name}"')
            ]
        )
