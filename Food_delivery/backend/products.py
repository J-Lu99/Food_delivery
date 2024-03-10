from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields, Namespace
from config import DevConfig
from models import Product, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

product_ns=Namespace('product', description='A namespace for Products')

product_model=product_ns.model(
    'Product',
    {
        'id':fields.Integer(),
        'title':fields.String(),
        'description':fields.String()
    }
)

#--------------------------------------------------------------------

@product_ns.route('/products')
class ProductsResource(Resource):
    @product_ns.marshal_list_with(product_model) #turn sql objects list into json so it might be compatible with frontend
    def get(self):
        '''Get all products'''
        products=Product.query.all()
        return products

    @product_ns.marshal_with(product_model) #turn sql object into json
    @product_ns.expect(product_model) # to be able to post
    @jwt_required()
    def post(self):
        '''Create a new product'''
        data=request.get_json()
        new_product=Product(
            title=data.get('title'),
            description=data.get('description')
        )
        new_product.save()
        return new_product, 201

#--------------------------------------------------------------------

@product_ns.route('/product/<int:id>')
class ProductResource(Resource):
    @product_ns.marshal_with(product_model)
    def get(self,id):
        '''Get a product by id'''
        product=Product.query.get_or_404(id)
        return product

    @product_ns.marshal_with(product_model )
    @product_ns.expect(product_model)
    @jwt_required()
    def put(self, id):
        '''Update a product by id'''
        product_to_update=Product.query.get_or_404(id)
        data=request.get_json()
        product_to_update.update(data.get('title'), data.get('description'))
        return product_to_update
    
    @product_ns.marshal_with(product_model)
    @jwt_required()
    def delete(self):
        '''Delete a product by id'''
        product_to_delete=Product.query.get_or_404(id)
        product_to_delete.delete()
        return product_to_delete