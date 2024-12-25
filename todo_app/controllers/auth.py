# from odoo import http
# from odoo.http import request
# import json
# import xmlrpc.client

# class Auth(http.Controller):


#     @http.route('/v1/auth/login',auth="none",methods=['POST'],csrf=False,type="http")
#     def login(self):
#         args=request.httprequest.data.decode()
#         vals=json.loads(args)
#         try:
#             url="http://localhost:8069"
#             db=vals.get('db')
#             username=vals.get('username')
#             password=vals.get('password')

#             common=xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
#             uid=common.authenticate(db,username,password,{})
#             if uid:
#                 return request.make_json_response({
#                     "message":"successful",
#                     "data":{
#                         "user_id":uid
#                     }
#                 },status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message":error
#             },status=400)
        
#     def login(self):
#         args=request.httprequest.data.decode()
#         vals=json.loads(args)
#         try:
#             url="http://localhost:8069"
#             db=vals.get('db')
#             username=vals.get('username')
#             password=vals.get('password')

#             common=request.session.authenticate(db,)
#             uid=common.authenticate(db,username,password,{})
#             if uid:
#                 return request.make_json_response({
#                     "message":"successful",
#                     "data":{
#                         "user_id":uid
#                     }
#                 },status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message":error
#             },status=400)
        
#     @http.route('/v2/auth/login',type="http",auth='none',methods=["POST"],csrf=False)
#     def login(self):
#         args=request.httprequest.data.decode()
#         vals=json.loads(args)
#         try:
#             db=vals.get('db')
#             username=vals.get('username')
#             password=vals.get('password')
#             credential = {'login': username, 'password': password, 'type': 'password'}

#             common=request.session.authenticate(db,credential)
#             if common:
#                 return request.make_json_response({
#                     "message":"successful",
#                     "data":{
#                         "user":request.env.user.name
#                     }
#                 },status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message":error
#             },status=400)
# #         args=request.httprequest.data.decode()
# #         vals=json.loads(args)
# #         try:
# #             if vals:
# #                 url="http://localhost:8069"
# #                 db=vals.get('db')
# #                 username=vals.get('name')
# #                 password=vals.get('password')
# #                 common=xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
# #                 uid=common.authenticate(db,username,password,{})

# #                 if not uid:
# #                     print(uid,"UID Data!")
# #                     return request.make_json_response({
# #                         "message":"logged in successfully!",
# #                         "user_id":uid.id
# #                     },status=400)

# #                 else:
# #                     print(uid,"UID Data!")
# #                     return request.make_json_response({
# #                         "message":"logged in successfully!",
# #                         "user_id":uid.id
# #                     },status=200)

# #         except Exception as error:
# #             return request.make_json_response({
# #                 "message":error
# #             },status=400)