#!/usr/bin/python3
""" Flask routes for handling URI subpaths concerning `Place` - `Amenity`
object relationships in storage, using `app_views` Blueprint.
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
def GET_all_Place_amenities(place_id):
    """ Returns JSON list of all `Amenity` instances associated
    with a given `Place` instance in storage

    Return:
        JSON list of all `Amenity` instances for a given `Place` instance
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


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def DELETE_Place_amenities(place_id, amenity_id):
    """ Deletes relationship between a `Place` and an `Amenity` instance in
    storage by ids in URI subpath

    Args:
        place_id: uuid of `Place` instance in storage
        amenity_id: uuid of `Amenity` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place and amenity and amenity in place.amenities:
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.remove(amenity)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def POST_Place_amenities(place_id, amenity_id):
    """ Links a new `Amenity` instance to a `Place` instance in storage,
    by ids in URI subpath

    Return:
        Linked `Amenity` instance and response status 201, or 404 response
    on error
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenities, amenity_id)

    if place and amenity:
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenities:
                return (jsonify(amenity.to_dict()))
            else:
                place.amenities.append(amenity)
        else:
            if amenity in place.amenity_ids:
                return (jsonify(amenity.to_dict()))
            else:
                place.amenity_ids.append(amenity)
        place.save()
        return (jsonify(amenity.to_dict()), 201)
    else:
        abort(404)
