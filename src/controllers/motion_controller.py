import logging
from flask import Blueprint, request
from ..helpers import JsonResponses

MotionController = Blueprint('MotionController', __name__)
logger = logging.getLogger(__name__)

@MotionController.route('/iot/motion', methods=["GET"])
def motion_get():
    try:
        motion = 1

        return JsonResponses.success(
            data = {
                "motion": motion
                },
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
        logger.error(f"motion_get: {e}")
        return JsonResponses.error(
            message = "Gagal mendapatkan data dari database",
        )
    
@MotionController.route('/iot/motion', methods=["POST"])
def motion_post():
    try:
        motion = request.json.get('motion')
        device = request.json.get('device')

        errors = {}

        if motion is None:
            errors['motion'] = "Motion tidak boleh kosong"
        
        if device is None:
            errors['device'] = "Device tidak boleh kosong"

        if errors:
            return JsonResponses.validation_error(
                errors = errors
            )

        return JsonResponses.success(
            data = {
                "motion": motion,
                "device": device
                },
            message = "Berhasil menambahkan data ke database"
        )
    
    except Exception as e:
        logger.error(f"motion_post: {e}")
        return JsonResponses.error(
            message = "Gagal menambahkan data ke database",
        )
    

    