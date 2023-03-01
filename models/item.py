from db import db
import datetime


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    category = db.Column(db.String(50), unique=False, nullable=False)
    expiry_time = db.Column(db.DateTime, unique=False, nullable=True)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    manufacturing_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False, nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="items")
