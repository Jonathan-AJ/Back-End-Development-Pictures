from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    try:
        if data and len(data) > 0:
            return jsonify(data), 200
        else:
            return jsonify({"message": "Data is empty"}), 500
    except NameError:  # or a more specific exception if defined like PictureError
        return jsonify({"message": "Data not found"}), 404

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            # Return only the matching picture
            return jsonify(picture), 200

    # Moved outside the loop: only return 404 if no match found
    return jsonify({"message": "Data not found"}), 404




######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json

    if not new_picture:
        return jsonify({"message": "Invalid input parameter"}), 422

    try:
        # Check for duplicate
        for pic in data:
            if pic['id'] == new_picture['id']:
                return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

        data.append(new_picture)
    except NameError:
        return jsonify({"message": "data not defined"}), 500

    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_data = request.json
    if not updated_data:
        return jsonify({"message": "Invalid input"}), 422

    for picture in data:
        if picture["id"] == id:
            # Return only the matching picture
            picture.update(updated_data)
            return jsonify(picture), 200

    # Moved outside the loop: only return 404 if no match found
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return '', 204  # Successfully deleted

    return jsonify({"message": "picture not found"}), 404