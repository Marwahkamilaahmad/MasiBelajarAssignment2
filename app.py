import logging
from flask import Flask
from src.controllers import HumidityController, TemperatureController, MotionController

app = Flask(__name__)

# Service
log_format = "%(levelname)s | %(name)s | %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
logger = logging.getLogger(__name__)

# Disable watchdog logging
logging.getLogger('watchdog').setLevel(logging.WARNING)

# Controller
app.register_blueprint(HumidityController)
app.register_blueprint(TemperatureController)
app.register_blueprint(MotionController)

if __name__ == '__main__':
    app.run()