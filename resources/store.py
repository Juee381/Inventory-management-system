from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # sqlalchemy exception
from flask_jwt_extended import jwt_required

from db import db
from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema
from logger_config import logger

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        if StoreModel.query.filter(StoreModel.name == store_data["name"]).first():
            abort(409, message="A store with that name already exists.")
        else:
            logger.info("inserting store data")
            store = StoreModel(**store_data)
            try:
                db.session.add(store)
                db.session.commit()
            except IntegrityError as err:
                logger.error(err)
                abort(400, message="A store with that name already exists.")
            except SQLAlchemyError as err:
                logger.error(err)
                abort(500, message="An error occurred creating the store.")

        return store


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        logger.info("Deleting store data")
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted"}, 200

    @jwt_required()
    @blp.response(201, StoreSchema)
    @blp.arguments(StoreUpdateSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)

        if store:
            logger.info("Inserting item data")
            store.name = store_data["name"]
        else:
            logger.info("Item not found therefor inserting item data")
            store = StoreModel(id=store_id, **store_data)

        db.session.add(store)
        db.session.commit()

        return store
