# -*- coding: utf-8 -*-
from odoo import http

# class MethodWoocommerce(http.Controller):
#     @http.route('/method_woocommerce/method_woocommerce/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_woocommerce/method_woocommerce/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_woocommerce.listing', {
#             'root': '/method_woocommerce/method_woocommerce',
#             'objects': http.request.env['method_woocommerce.method_woocommerce'].search([]),
#         })

#     @http.route('/method_woocommerce/method_woocommerce/objects/<model("method_woocommerce.method_woocommerce"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_woocommerce.object', {
#             'object': obj
#         })