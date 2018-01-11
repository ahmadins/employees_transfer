# -*- coding: utf-8 -*-
from odoo import http

# class EmployeeTransfer(http.Controller):
#     @http.route('/employee_transfer/employee_transfer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_transfer/employee_transfer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_transfer.listing', {
#             'root': '/employee_transfer/employee_transfer',
#             'objects': http.request.env['employee_transfer.employee_transfer'].search([]),
#         })

#     @http.route('/employee_transfer/employee_transfer/objects/<model("employee_transfer.employee_transfer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_transfer.object', {
#             'object': obj
#         })