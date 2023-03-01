from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from datetime import datetime
import pytz

from db import db
from models import ItemModel, StoreModel
from schemas import ItemSchema, ItemUpdateSchema, DeleteSchema
from logger_config import logger

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        if StoreModel.query.get(item_data[
                                    "store_id"]):  # and item_data["name"] not in StoreModel.query.get(item_data["store_id"])["items"]:
            logger.info("converting time into CTS timezone")
            item_data["expiry_time"] = item_data["expiry_time"].astimezone(pytz.timezone('US/Central'))
            item_data["manufacturing_time"] = item_data["manufacturing_time"].astimezone(pytz.timezone('US/Central'))

            logger.info("inserting item data")
            item = ItemModel(**item_data)

            try:
                db.session.add(item)
                db.session.commit()

            except IntegrityError as err:
                logger.error(err)
                abort(400, message="A item with that id is already exists.")

            except SQLAlchemyError as err:
                logger.error(err)
                abort(500, message="An error occurred while inserting the item.")

            return item

        else:
            abort(400, message="Store does not exist with given store id")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        logger.info("Fetching item data")
        return ItemModel.query.get_or_404(item_id)

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        logger.info("Deleting item data")
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            logger.info("Updating item data")
            item.name = item_data["name"]
            item.category = item_data["category"]
            item.expiry_time = item_data["expiry_time"]
            item.quantity = item_data["quantity"]
            item.manufacturing_time = item_data["manufacturing_time"]

        else:
            logger.info("Item not found therefor inserting item data")
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/del_item")
class MultipleItem(MethodView):
    @jwt_required()
    @blp.arguments(DeleteSchema)
    def post(self, item_id):
        try:
            logger.info("Deleting multiple items")
            for i in item_id["del_items"]:
                item = ItemModel.query.get(i)
                db.session.delete(item)
                db.session.commit()
            return {"message": "Deleted list of item"}

        except:
            abort(404, message="item not found.")


@blp.route("/item/search")
class SearchItem(MethodView):
    @blp.response(200, ItemSchema)
    def get(self):
        name = request.args.get("name")
        category = request.args.get("category")

        if name and category:
            logger.info("Filtering data with item name and category")
            item = ItemModel.query.filter(ItemModel.name == name, ItemModel.category == category).first()

        elif name and not category:
            logger.info("Filtering data with item name")
            item = ItemModel.query.filter(ItemModel.name == name).first()

        elif category and not name:
            logger.info("Filtering data with item category")
            item = ItemModel.query.get(ItemModel.category == category).first()

        else:
            abort(404, message="Does not exist any item")

        if datetime.now() > item.expiry_time:
            is_expired = False
        else:
            is_expired = True

        return jsonify(
            {"name": item.name, "category": item.category, "is_expired": is_expired, "expiry_time": item.expiry_time,
             "quantity": item.quantity, "id": item.id})
