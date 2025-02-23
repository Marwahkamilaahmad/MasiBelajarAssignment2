import logging
from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from ..helpers import JsonResponses
from ..data.database import MOTION_COLLECTION

MotionController = Blueprint('MotionController', __name__)
logger = logging.getLogger(__name__)

@MotionController.route('/iot/motion', methods=["GET"])
def motion_get():
    try:
        data = []
        for motion in MOTION_COLLECTION.find().sort("timestamp", -1):
            motion['_id'] = str(motion['_id'])
            data.append(motion)

        return JsonResponses.success(
            data = data,
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
        logger.error(f"motion_get: {e}")
        return JsonResponses.error(
            message = "Gagal mendapatkan data dari database",
        )
    
@MotionController.route('/iot/motion/<id>', methods=["GET"])
def motion_get_by_id(id):
    try:
        motion = MOTION_COLLECTION.find_one({"_id": ObjectId(id)})
        if motion is None:
            return JsonResponses.not_found(
                message = "Data tidak ditemukan"
            )

        motion['_id'] = str(motion['_id'])

        return JsonResponses.success(
            data = motion,
            message = "Berhasil mendapatkan data dari database"
        )
    
    except Exception as e:
        logger.error(f"motion_get_by_id: {e}")
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
        
        result = MOTION_COLLECTION.insert_one({
            "motion": motion,
            "device": device,
            "timestamp": datetime.now()
        })

        result = MOTION_COLLECTION.find_one({"_id": result.inserted_id})
        result['_id'] = str(result['_id'])

        return JsonResponses.success(
            data = result,
            message = "Berhasil menambahkan data ke database"
        )
    
    except Exception as e:
        logger.error(f"motion_post: {e}")
        return JsonResponses.error(
            message = "Gagal menambahkan data ke database",
        )
    
@MotionController.route('/iot/motion/<id>', methods=["DELETE"])
def motion_delete(id):
    try:
        result = MOTION_COLLECTION.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            return JsonResponses.not_found(
                message = "Data tidak ditemukan"
            )

        return JsonResponses.success(
            data = None,
            message = "Berhasil menghapus data dari database"
        )
    
    except Exception as e:
        logger.error(f"motion_delete: {e}")
        return JsonResponses.error(
            message = "Gagal menghapus data dari database",
        )
    