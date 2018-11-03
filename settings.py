import os


class MongoDBConfig(object):
    MONGODB_HOST = "mongodb://127.0.0.1:27017/"
    MONGODB_NAME = "tmadb"


class OnLineMongodbConfig(MongoDBConfig):
    pass


class DevConfig(MongoDBConfig):
    pass


class OnlineConfig(OnLineMongodbConfig):
    pass


run_env = os.getenv("RUN_ENV", "dev")
config = DevConfig
if run_env == "prod":
    config = OnlineConfig
