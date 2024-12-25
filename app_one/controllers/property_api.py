import json
from odoo import SUPERUSER_ID, http
from odoo.http import request


class PropertyApi(http.Controller):
    @http.route("/v1/property", method=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                "message": "name is required!",
            }, status=400)

        try:
            res = request.env['property'].sudo().create(vals)
            print(res)
            if res:
                return request.make_json_response({
                    "message": "Property has been created successfully",
                    "id": res.id,
                    "name": res.name
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)


    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        property_id = request.env['property'].sudo().search([('id', '=', property_id)])
        print(property_id)



    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return [{
                "message": "Property has been created successfully",
            }]
        
    @http.route('/v1/sql',type='http',methods=['POST'],auth='none',csrf=False)
    def sql_commands(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
            if vals:
                columns=','.join(vals.keys())
                name=vals.get('name')
                postcode=vals.get('postcode')
                bedrooms=vals.get('bed_rooms')
                cr=request.env.cr
                query=f"""INSERT INTO property ({columns}) VALUES ('{name}','{postcode}',{bedrooms}) RETURNING id,{columns};"""
                cr.execute(query)
                res=cr.fetchone()
                return request.make_json_response({
                    "message": "SQL query executed successfully",
                    "data":{
                        "id":res[0],
                        "name":res[1],
                        "postcode":res[2],
                        "bedrooms":res[3],
                    }
                },status=200)
        
        except Exception as error:
            return request.make_json_response({
                "message": error,
            },status=400)
