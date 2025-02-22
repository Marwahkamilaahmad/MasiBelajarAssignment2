from dotenv import dotenv_values

_env = dotenv_values(".env")

MONGO_DB_URI = _env["MONGO_DB_URI"]