from flask import Flask
from src.controllers import HumidityController, TemperatureController

app = Flask(__name__)

app.register_blueprint(HumidityController)
app.register_blueprint(TemperatureController)

if __name__ == '__main__':
    app.run(
        load_dotenv=True,
        )