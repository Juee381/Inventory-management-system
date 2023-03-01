from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask import request
from flask_uploads import UploadNotAllowed

from db import db
from schemas import ImageSchema
from libs import image_helper

blp = Blueprint("Images", __name__, description="Operations on images")


@blp.route("/image/<int:store_id>")
class ImageUpload(MethodView):
    @jwt_required
    def post(self, store_id):
        """
        saves the image in particular store's folder
        If there is a filename conflict, it appends a number at the end.
        """
        data = ImageSchema.load(request.files)
        folder = f"store_{store_id}"
        try:
            image_helper.save_image(data["image"], folder=folder, name="item")
            return {"message": "Image uploaded"}, 200
        except UploadNotAllowed:
            return {"message": "Image has not proper extension"}, 400
