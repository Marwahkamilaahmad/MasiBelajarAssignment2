import logging
from flask import Blueprint, request
from ..helpers import JsonResponses

TemperatureController = Blueprint('TemperatureController', __name__)
logger = logging.getLogger(__name__)

@TemperatureController.route('/iot/temperature', methods=["GET"])
def temperature_get():
    try:
        temperature = 50

        return JsonResponses.success(
            data = {
                "temperature": temperature
                },
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
        logger.error(f"temperature_get: {e}")
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

        return JsonResponses.success(
            data = {
                "temperature": temperature,
                "device": device
                },
            message = "Berhasil menambahkan data ke database"
        )
    
    except Exception as e:
        logger.error(f"temperature_post: {e}")
        return JsonResponses.error(
            message = "Gagal menambahkan data ke database",
        )