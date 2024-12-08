from odoo import SUPERUSER_ID, _,http,exceptions
from odoo.http import request
import json
import logging

_logger=logging.getLogger(__name__)


class TodoApi(http.Controller):

    @http.route('/auth/',type='json', auth='none', methods=["POST"], csrf=False)
    def authenticate(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            login = vals["login"]
        except KeyError:
            raise exceptions.AccessDenied(message='`login` is required.')

        try:
            password = vals["password"]
        except KeyError:
            raise exceptions.AccessDenied(message='`password` is required.')

        try:
            db = vals["db"]
        except KeyError:
            raise exceptions.AccessDenied(message='`db` is required.')

        http.request.session.authenticate(db,login,password)
        res = request.env['ir.http'].session_info()
        return res

    # @http.route('/v1/todotask/login',type='http',auth='none',methods=["POST"],csrf=False)
    # def login(self):
    #     args=request.httprequest.data.decode()
    #     vals=json.loads(args)
    #     try:
    #         if(vals):
                
    #             db=vals.get('db')
    #             login=vals.get('login')
    #             password=vals.get('password')
    #             print(db,login,password,"data")
    #             uid=http.request.session.authenticate("todo_app", "admin", "admin")             
    #             return request.make_json_response({
    #                 "message":"loged in successfully",
    #                 "data":{
    #                     "user_id":uid.id,
    #                     "user_name":uid.name,
    #                 }
    #             },status=200)
            
    #     except Exception as error:
    #         return request.make_json_response({
    #             "message":error
    #         },status=400)
    
    @http.route("/v1/todotask/create",methods=['POST'],type='http',auth='none',csrf=False)
    def createSaleOrder(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        sale_order_lines=[(0, 0, {
                        'product_id': line["product_id"]
                        ,'product_uom_qty': line["product_id"],
                    })for line in vals.get('order_line')]
        print(sale_order_lines)
        try:
            if(vals):
                createorder=request.env['sale.order'].with_user(SUPERUSER_ID).create({'partner_id': vals.get('partner_id'),
                                                                                    'order_line':sale_order_lines
                                                                                    })
                order_confirm=createorder.action_confirm()
                return request.make_json_response({
                   "message":"order created successfully",
                   "data":{
                       "order_id":createorder.id,
                       "confirm":order_confirm
                    },
               },status=200) 
        except Exception as error:
            return request.make_json_response({
                "message":error
            },status=400)
