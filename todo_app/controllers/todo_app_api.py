from odoo import fields
from datetime import datetime, timedelta
from odoo import SUPERUSER_ID,http,exceptions
from odoo.http import request
import json
import re


def valid_response(msg,data):
    return request.make_json_response({
        "message":msg,
        "data":data
    },status=200)

def in_valid_response(msg):
    return request.make_json_response({
        "message":msg
    },status=400)



def is_valid(mail):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@gmail.com')
    if re.fullmatch(regex,mail):
        return True
    else:
        return False
    
def egypt_code(number):
    regex=re.compile(r'\+20+[0-9]+')
    if re.fullmatch(regex,number):
        return True
    else:
        return False



class TodoApi(http.Controller):

    # @http.route(
    #     '/auth/login',
    #     type='json', auth='none', methods=["POST"], csrf=False)
    # def authenticate(self):
    #     args=request.httprequest.data.decode()
    #     post=json.loads(args)
    #     print(post)
    #     try:
    #         login = post["login"]
    #     except KeyError:
    #         raise exceptions.AccessDenied(message='`login` is required.')

    #     try:
    #         password = post["password"]
    #     except KeyError:
    #         raise exceptions.AccessDenied(message='`password` is required.')

    #     try:
    #         db = post["db"]
    #     except KeyError:
    #         raise exceptions.AccessDenied(message='`db` is required.')

    #     http.request.session.authenticate(db, login, password)
    #     res = request.env['ir.http'].session_info()
    #     return res

        
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

    # @http.route('/auth/login',type="http",methods=['POST'],auth="none",csrf=False)
    # def login(self):
    #     args=request.httprequest.data.decode()
    #     vals=json.loads(args)
    #     try:
    #         if vals:
    #             db=vals.get('db')
    #             username=vals.get('username')
    #             password=vals.get('password')
    #             if not username or not password:
    #                 return in_valid_response("missing username or password")
    #             user=request.env['res.users'].with_user(SUPERUSER_ID)
    #             print(user,"data#####")
    #             auth=user._login(db,username,password)
    #             print(auth,"auth####")
    #             if not user or not user._check_password(password):
    #                 return in_valid_response("username or password are invalid!")
    #             else:
    #                 return valid_response("successfuly",{"user_id":user.id})
    #     except Exception as error:
    #         return in_valid_response(error)

    # @http.route(
    #     '/auth/logout',
    #     auth="user", type="http", methods=['GET', 'POST'], csrf=False)
    # def Logout(self):
    #     try:
    #         request.session.logout(keep_db=True)
    #         return valid_response("successful")
    #     except Exception as error:
    #         return in_valid_response(error)
    
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
                return valid_response(msg="order created successfully",data={
                       "order_id":createorder.id,
                       "confirm":order_confirm
                    }) 
        except Exception as error:
            return in_valid_response(error)
        
    @http.route('/v1/createinvoice',type="http",methods=["POST"],auth="none",csrf=False)
    def create_invoice(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            if vals.get('token'):
                print(vals.get('token'),"token data!#######")
                token=request.env['token'].with_user(SUPERUSER_ID).search([('token','=',vals.get('token'))])
                print(token.estimated_date,datetime.now())
                if token.estimated_date < datetime.now()+timedelta(hours=2):
                    if vals.get('order_id'):
                        order=request.env['sale.order'].sudo().search([('id','=',vals.get('order_id'))])
                        if(order):
                            print(order)
                            invoice=order.with_user(SUPERUSER_ID)._create_invoices()
                            if invoice:
                                print(invoice)
                                invoice_confirm=invoice.with_user(SUPERUSER_ID).action_post()
                                return valid_response(msg="invoice created successfully",data={
                                    "invoice_id":invoice.id,
                                    "invoice_confirm":invoice_confirm
                                })
                            else:
                                return in_valid_response(msg="can't create the invoice")
                        else:
                            return in_valid_response(msg="order dosn't exist!")
                    else:
                        return in_valid_response("no order id givin in data!")
                else:
                    return in_valid_response("invalid token!")
            else:
                return in_valid_response("no token givin!")
        except Exception as error:
            return in_valid_response(error)
        
    @http.route('/v1/createpartner',type="http",auth="none",methods=['POST'],csrf=False)
    def create_partner(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            if vals:
                check=request.env['res.partner'].with_user(SUPERUSER_ID).search([("phone","=",vals.get('phone')),("email","=",vals.get('email'))])
                if not check:
                    if is_valid(vals.get('email')):
                        if egypt_code(vals.get('phone')):
                            partner=request.env['res.partner'].with_user(SUPERUSER_ID).create({"is_company":True,
                                                                                            "name":vals.get('name'),
                                                                                            "phone":vals.get('phone'),
                                                                                            "mobile":vals.get('mobile'),
                                                                                            "email":vals.get('email'),
                                                                                            "website":vals.get('website')
                                                                                            })
                            if partner:
                                return valid_response("partner created successfully",{"partner_id":partner.id})
                            else:
                                return in_valid_response("can't create this partner")
                        else:
                            return in_valid_response("phone number is not valid!\negyption code only")
                    else: 
                        return in_valid_response("email is not valid!\nit should be xxx@gmail.com")
                    
                else:
                    redundancy_fields=list()
                    records=list()
                    for rec in check:
                        records.append(rec.id)
                        if rec.phone==vals.get('phone'):
                            redundancy_fields.append('phone')
                        if rec.email==vals.get('email'):
                            redundancy_fields.append('email')
                    redundancy_fields=list(set(redundancy_fields))
                    return in_valid_response(f"the {redundancy_fields} you give is already exists in record{records}!")    
        except Exception as error:
            return in_valid_response(error)
        

    @http.route('/v1/updatepartner/<int:partner_id>',type="http",auth="none",methods=['PUT'],csrf=False)
    def update_partner(self,partner_id):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            partner=request.env['res.partner'].with_user(SUPERUSER_ID).browse(partner_id)
            if partner:
                if vals:
                    if is_valid(vals.get('email')):
                        if egypt_code(vals.get('phone')):
                            # check=request.env['res.partner'].with_user(SUPERUSER_ID).search([('phone','=',vals.get('phone')),'|',('email','=',vals.get('email'))])
                            check_phone=request.env['res.partner'].with_user(SUPERUSER_ID).search([('phone','=',vals.get('phone'))])
                            check_email=request.env['res.partner'].with_user(SUPERUSER_ID).search([('email','=',vals.get('email'))])
                            print(check_phone,check_email)
                            if not check_phone and not check_email:
                                partner.write({
                                    "name":vals.get('name'),
                                    "phone":vals.get('phone'),
                                    "mobile":vals.get('mobile'),
                                    "email":vals.get('email'),
                                    "website":vals.get('website')
                                })
                                return valid_response("partner updated successfully",{"partner_id":partner.id,
                                                                                      "partner_name":partner.name})
                            else:
                                redundancy_fields=list()
                                records=list()
                                if check_phone:
                                    redundancy_fields.append('phone')
                                    for rec in check_phone:
                                        records.append(rec.id)
                                        print(rec.phone)
                                if check_email:
                                    redundancy_fields.append('email')
                                    for rec in check_email:
                                        records.append(rec.id)
                                records=list(set(records))
                                print(records)
                                return in_valid_response(f"the {redundancy_fields} you give is already exists in record{records}")
                        else:
                            return in_valid_response("phone number is not valid!\negyption code only")
                    else:
                        return in_valid_response("invalid email!\nit should be x@gmail.com")
                else:
                    return in_valid_response("you should give some values to update")
            else:
                return in_valid_response("partner not found!")
        except Exception as error:
            return in_valid_response(error)
        
    @http.route('/v1/createproduct',type='http',methods=['POST'],auth='none',csrf=False)
    def create_product(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            if vals:
                product=request.env['product.product'].with_user(SUPERUSER_ID).create({"name":vals.get('name')})
                return valid_response("product created successfully!",{"product_id":product.id,
                                                                    "product_name":product.name})
            else:
                return in_valid_response("you should give some values to create")
        except Exception as error:
            return in_valid_response(error)
        

    @http.route('/createtoken',type='http',auth='none',methods=['POST'],csrf=False)
    def token(self):
        try:
            token=request.env['token'].with_user(SUPERUSER_ID).create({})
            return valid_response("token craeted successfuly!",{"token":token.token,
                                                                "token_id":token.id})
        except Exception as error:
            return in_valid_response(error)
        
    @http.route('/v1/createpayment',type='http',methods=['POST'],auth='none',csrf=False)
    def create_payment(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            if vals:
                if vals.get('invoice_id'):
                    payment_register=request.env['account.payment.register'].with_user(SUPERUSER_ID).with_context({"active_model":"account.move",
                                                                                                                   "active_ids":vals.get('invoice_id')})
                    payment_register.create({"amount":vals.get('amount')}).action_create_payments()
                    invoice_payment=request.env['account.payment'].with_user(SUPERUSER_ID).browse(vals.get('invoice_id'))
                    print(invoice_payment)
                    return valid_response("payment created successfully!")
                else:
                    return in_valid_response("invoice id is required!")
            else:
                return in_valid_response("you should give some values")
        except Exception as error:
            return in_valid_response(error)