# -*- coding: utf-8 -*-

from odoo import models, fields, api
from woocommerce import API



class Productos(models.Model):
    _inherit = 'product.template'

    name = fields.Char(string='Name')
    
    
    @api.model
    def sync_stock_product(self):
        url=self.env["enotif_woo.keys"].search([],limit=1).woocommerce_url
        key=self.env["enotif_woo.keys"].search([],limit=1).woocommerce_api_key
        secret=self.env["enotif_woo.keys"].search([],limit=1).woocommerce_api_secret
        wcapi = API(
        url=url,
        consumer_key=key,
        consumer_secret=secret,
        #wp_api=True,
        version="wc/v3"
        )

        #print(wcapi.get("products").json())
        #stock_quantity	integer	Stock quantity.
        #stock_status	
        #           string	Controls the stock status of the product. Options: 
        #           instock, 
        #           outofstock, 
        #           onbackorder. 
        #         
        # Default is instock.
        productos_woo = wcapi.get('products', params={'per_page': 100}).json()
        for pw in productos_woo:
            sku=pw['sku']
            id=pw['id']
            name=pw['name']
            descripton_sale=pw['description']
            list_price=pw['price']
            type="product"
            
                    
            productos_all=self.env['product.template'].search([('default_code', '=', sku)],limit=1)
            if productos_all:
                stock=productos_all.qty_available
                if productos_all.qty_available<=0:
                    stock_status="outofstock"
                else:
                    stock_status="instock"
                data = {
                    'stock_quantity': stock,
                    'stock_status': stock_status
                    }
                #wcapi.put("products/attributes/"+str(id), data).json()
                wcapi.put("products/"+str(id), data).json()
                values = {
                            "name": name,
                            "lst_price": list_price,
                            "descripton_sale":descripton_sale,
                        }                
                self.write(values)
            else:
                values = {
                            "default_code": sku,
                            "name": name,
                            "lst_price": list_price,
                            "descripton_sale":descripton_sale,
                            "type":type,
                        }
                self.create(values)
