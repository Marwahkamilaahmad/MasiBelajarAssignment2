from flask import jsonify

class JsonResponses:
    def __init__(self, data = None, message = None):
        self.data = data
        self.message = message

    def response(self):
        return jsonify({
            "data": self.data,
            "message": self.message
        })
    
    @staticmethod
    def success(data, message):
        return jsonify({
            "data": data,
            "message": message
        })
    
    @staticmethod
    def validation_error(errors: dict, message = "Kesalahan validasi"):
        return jsonify({
            "message": message,
            "errors": errors
        }), 400

    @staticmethod
    def error(message, errors: dict = None):
        return jsonify({
            "message": message,
            "errors": errors
        }), 500
    
