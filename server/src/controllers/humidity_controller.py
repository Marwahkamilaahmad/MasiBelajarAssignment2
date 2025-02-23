import logging
from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from ..helpers import JsonResponses
from ..data.database import HUMIDITY_COLLECTION

HumidityController = Blueprint('HumidityController', __name__)
logger = logging.getLogger(__name__)

@HumidityController.route('/iot/humidity', methods=["GET"])
def humidity_get():
    try:
        data = []
        for humidity in HUMIDITY_COLLECTION.find().sort("timestamp", -1):
            humidity['_id'] = str(humidity['_id'])
            data.append(humidity)

        return JsonResponses.success(
            data = data,
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
        logger.error(f"humidity_get: {e}")
        return JsonResponses.error(
            message = "Gagal mendapatkan data dari database",
        )
    
@HumidityController.route('/iot/humidity/<id>', methods=["GET"])
def humidity_get_by_id(id):
    try:
        humidity = HUMIDITY_COLLECTION.find_one({"_id": ObjectId(id)})
        if humidity is None:
            return JsonResponses.not_found(
                message = "Data tidak ditemukan"
            )

        humidity['_id'] = str(humidity['_id'])

        return JsonResponses.success(
            data = humidity,
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
        logger.error(f"humidity_get_by_id: {e}")
        return JsonResponses.error(
            message = "Gagal mendapatkan data dari database",
        )

@HumidityController.route('/iot/humidity', methods=["POST"])
def humidity_post():
    try:
        humidity = request.json.get('humidity')
        device = request.json.get('device')

        errors = {}

        if humidity is None:
            errors['humidity'] = "Humidity tidak boleh kosong"
        
        if device is None:
            errors['device'] = "Device tidak boleh kosong"

        if errors:
            return JsonResponses.validation_error(
                errors = errors
            )
        
        result = HUMIDITY_COLLECTION.insert_one({
            "humidity": humidity,
            "device": device,
            "timestamp": datetime.now()
        })

        result = HUMIDITY_COLLECTION.find_one({"_id": result.inserted_id})
        result['_id'] = str(result['_id'])

        return JsonResponses.success(
            data = result,
            message = "Berhasil menambahkan data ke database"
        )
    
    except Exception as e:
        logger.error(f"humidity_post: {e}")
        return JsonResponses.error(
            message = "Gagal menambahkan data ke database",
        )
    

@HumidityController.route('/iot/humidity/<id>', methods=["DELETE"])
def humidity_delete(id):
    try:
        result = HUMIDITY_COLLECTION.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            return JsonResponses.not_found(
                message = "Data tidak ditemukan"
            )

        return JsonResponses.success(
            data = None,
            message = "Berhasil menghapus data dari database"
        )
    
    except Exception as e:
        logger.error(f"humidity_delete: {e}")
        return JsonResponses.error(
            message = "Gagal menghapus data dari database",
        )