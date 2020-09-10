#!/usr/bin/python3
""" Flask routes for `Place` object related URI subpaths using the
`app_views` Blueprint.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
import os

@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def GET_all_Place_Amenities(place_id):
    """ Returns JSON list of all `amenities` instances associated
    with a given `place` instance in storage

    Return:
        JSON list of all `Place` instances for a given `City` instance
    """
    place = storage.get(Place, place_id)

    if place:
        am_list = []
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            am_objs = place.amenities
        else:
            am_objs = place.amenity_ids
        for am in am_objs:
            am_list.append(am.to_dict())
        return jsonify(am_list.to_dict())
    else:
        abort(404)

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_Place_amenities(place_id, amenity_id):
    """ Deletes `Amenity` instance in storage by id in URI subpath

    Args:
        place_id: uuid of `Place` instance in storage
        amenity_id: uuid of `amenity` instance in storage
    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    place = storage.get(Place, place_id)
    am = storagy.get(Amenity, amenity_id)
    if place and am:
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            am_objs = place.amenities
        else:
            am_objs = place.aminity_ids
        am_objs.remove(amenity)
        place.save

        return ({})

    else:
        abort(404)


@app_views.route('/olaces/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def POST_Place_amenities(place_id, amenity_id):
    """ Creates new `Place` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    place = storage.get(Place, place_id)
    am = storage.get(Amenities, amenity_id)

    if place and am:
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            am_objs = place.amenities
        else:
            am_objs = place.amenity_ids
        am_objs.amenities.append(am)
        place.save()
        return (jsonify(am.to_dict()))
        place.save()
    else:
        abort(404)
