import logging
from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from ..helpers import JsonResponses
from ..data.database import TEMPERATURE_COLLECTION

TemperatureController = Blueprint('TemperatureController', __name__)
logger = logging.getLogger(__name__)

@TemperatureController.route('/iot/temperature', methods=["GET"])
def temperature_get():
    try:
        data = []
        for temperature in TEMPERATURE_COLLECTION.find().sort("timestamp", -1):
            temperature['_id'] = str(temperature['_id'])
            data.append(temperature)

        return JsonResponses.success(
            data = data,
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
        logger.error(f"temperature_get: {e}")
        return JsonResponses.error(
            message = "Gagal mendapatkan data dari database",
        )
    
@TemperatureController.route('/iot/temperature/<id>', methods=["GET"])
def temperature_get_by_id(id):
    try:
        temperature = TEMPERATURE_COLLECTION.find_one({"_id": ObjectId(id)})
        if temperature is None:
            return JsonResponses.not_found(
                message = "Data tidak ditemukan"
            )

        temperature['_id'] = str(temperature['_id'])

        return JsonResponses.success(
            data = temperature,
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
        logger.error(f"temperature_get_by_id: {e}")
        return JsonResponses.error(
            message = "Gagal mendapatkan data dari database",
        )

@TemperatureController.route('/iot/temperature', methods=["POST"])
def temperature_post():
    try:
        temperature = request.json.get('temperature')
        device = request.json.get('device')

        errors = {}

        if temperature is None:
            errors['temperature'] = "Temperature tidak boleh kosong"

        if device is None:
            errors['device'] = "Device tidak boleh kosong"

        if errors:
            return JsonResponses.validation_error(
                errors = errors
            )
        
        result = TEMPERATURE_COLLECTION.insert_one({
            "temperature": temperature,
            "device": device,
            "timestamp": datetime.now()
        })

        result = TEMPERATURE_COLLECTION.find_one({"_id": result.inserted_id})
        result['_id'] = str(result['_id'])

        return JsonResponses.success(
            data = result,
            message = "Berhasil menambahkan data ke database"
        )
    
    except Exception as e:
        logger.error(f"temperature_post: {e}")
        return JsonResponses.error(
            message = "Gagal menambahkan data ke database",
        )
    
@TemperatureController.route('/iot/temperature/<id>', methods=["DELETE"])
def temperature_delete(id):
    try:
        result = TEMPERATURE_COLLECTION.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return JsonResponses.not_found(
                message = "Data tidak ditemukan"
            )

        return JsonResponses.success(
            data = None,
            message = "Berhasil menghapus data dari database"
        )
    
    except Exception as e:
        logger.error(f"temperature_delete: {e}")
        return JsonResponses.error(
            message = "Gagal menghapus data dari database",
        )