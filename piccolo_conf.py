from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

DB = PostgresEngine(
    config={
        "database": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
    }
)

APP_REGISTRY = AppRegistry(
    apps=[
        "piccolo_admin.piccolo_app",
        "piccolo.apps.user.piccolo_app",
        "home.piccolo_app",
        "accounts.piccolo_app",
        "questions.piccolo_app",
    ]
)
