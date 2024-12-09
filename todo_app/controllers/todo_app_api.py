from odoo import SUPERUSER_ID, _,http,exceptions
from odoo.http import request
import json
import logging


_logger=logging.getLogger(__name__)

class TodoApi(http.Controller):

    @http.route(
        '/auth/login',
        type='json', auth='none', methods=["POST"], csrf=False)
    def authenticate(self):
        args=request.httprequest.data.decode()
        post=json.loads(args)
        print(post)
        try:
            login = post["login"]
        except KeyError:
            raise exceptions.AccessDenied(message='`login` is required.')

        try:
            password = post["password"]
        except KeyError:
            raise exceptions.AccessDenied(message='`password` is required.')

        try:
            db = post["db"]
        except KeyError:
            raise exceptions.AccessDenied(message='`db` is required.')

        http.request.session.authenticate(db, login, password)
        res = request.env['ir.http'].session_info()
        return res

    @http.route(
        '/auth/logout',
        auth="user", type="http", methods=['GET', 'POST'], csrf=False
    )
    def Logout(self):
        try:
            request.session.logout(keep_db=True)
        except exceptions as e:
            return request.make_json_response({
                "message":e
            },status=400)
        
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
        
    @http.route('/v1/createinvoice',type="http",methods=["POST"],auth="none",csrf=False)
    def create_invoice(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            if vals.get('order_id'):
                order=request.env['sale.order'].sudo().search([('id','=',vals.get('order_id'))])
                if(order):
                    print(order)
                    invoice=order.with_user(SUPERUSER_ID)._create_invoices()
                    if invoice:
                        print(invoice)
                        invoice_confirm=invoice.with_user(SUPERUSER_ID).action_post()
                        return request.make_json_response({
                            "message":"invoice created successfully",
                            "invoice_id":invoice.id,
                            "invoice_confirm":invoice_confirm
                        },status=200)
                    else:
                        return request.make_json_response({
                            "message":"can't create the invoice",
                        },status=400)
                else:
                    return request.make_json_response({
                        "message":"order dosn't exist!"
                    },status=400)
                
        except Exception as error:
            return request.make_json_response({
                "message":error
            },status=400)
        
    @http.route('/v1/createpartner',type="http",auth="none",methods=['POST'],csrf=False)
    def create_partner(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            if vals:
                check=request.env['res.partner'].with_user(SUPERUSER_ID).search([("phone","=",vals.get('phone')),("email","=",vals.get('email')),("mobile","=",vals.get('mobile'))])
                if not check:
                    partner=request.env['res.partner'].with_user(SUPERUSER_ID).create({"is_company":True,
                                                                                    "name":vals.get('name'),
                                                                                    "phone":vals.get('phone'),
                                                                                    "mobile":vals.get('mobile'),
                                                                                    "email":vals.get('email'),
                                                                                    "website":vals.get('website')
                                                                                    })
                
                    if partner:
                        return request.make_json_response({
                            "message":"partner created successfully",
                            "partner_id":partner.id
                        },status=200)
                    else:
                        return request.make_json_response({
                            "message":"can't create this partner"
                        })
                else:
                    return request.make_json_response({
                        "message":"data you give is already exist!"
                    },status=400)
        except Exception as error:
            return request.make_json_response({
                "message":error
            },status=400)