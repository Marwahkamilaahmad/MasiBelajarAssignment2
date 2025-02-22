from flask import Blueprint, request
from ..helpers import JsonResponses

HumidityController = Blueprint('HumidityController', __name__)

@HumidityController.route('/iot/humidity', methods=["GET"])
def humidity_get():
    try:
        humidity = 50

        return JsonResponses.success(
            data = {
                "humidity": humidity
                },
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
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

        return JsonResponses.success(
            data = {
                "humidity": humidity,
                "device": device
                },
            message = "Berhasil menambahkan data ke database"
        )
    
    except Exception as e:
        return JsonResponses.error(
            message = "Gagal menambahkan data ke database",
        )