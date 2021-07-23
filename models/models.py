# -*- coding: utf-8 -*-

from odoo import models, fields, api
from woocommerce import API




class ModuleName(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def sync_sale_order(self):
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

        customers_woo=wcapi.get("orders").json()
        


class ModuleName(models.Model):
    _inherit = 'res.partner'

    @api.model
    def sync_partner(self):
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

        customers_woo=wcapi.get("customers").json()
                
        for pw in customers_woo:
            parent_id=0
            email=pw['email']
            nombre=pw['first_name']
            apellido=pw['last_name']
            direccion_facturacion=pw['billing']
            direcciones_envio=pw['shipping']
            
            calle=direccion_facturacion['address_1']
            comuna=direccion_facturacion['state']
            ciudad=direccion_facturacion['city']
            codigo_postal=direccion_facturacion['postcode']
            mobile=direccion_facturacion['phone']
                
                    
            clientes_method=self.env['res.partner'].search([('email', '=', email)],limit=1)
            if clientes_method:
                continue
            else:
                values = {
                            "name": nombre +" " +apellido,
                            "email": email,
                            'street':calle +" " +comuna,
                            'city':ciudad,
                            'zip':codigo_postal,
                            'mobile':mobile,
                            'customer':True,
                        }
                parent_id=self.create(values)   
                parent_id=parent_id.id
            if direccion_facturacion:
                values = {
                            "name": nombre +" " +apellido,
                            "email": email,
                            'street':calle +" " +comuna,
                            'city':ciudad,
                            'zip':codigo_postal,
                            'mobile':mobile,
                            'type':'invoice',
                            'parent_id':parent_id
                        }
                self.create(values)  
            if direcciones_envio:
                values = {
                            "name": nombre +" " +apellido,
                            'street':direcciones_envio['address_1']+" "+ direcciones_envio['state'],
                            'city':direcciones_envio['city'],
                            'zip':direcciones_envio['postcode'],
                            'type':'delivery',
                            'parent_id':parent_id
                        }
                self.create(values)  
                
                     


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
                            "available_in_pos":True,
                        }
                self.create(values)        
            
            
