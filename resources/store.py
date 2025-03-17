import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint,abort 
from schemas import StoreSchema
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("stores", __name__ , description = "Operations in Stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(201, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    def post(self, store_data):
        store =  StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400, 
                message="A store with that name already exists!"
            )
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")
        return store
