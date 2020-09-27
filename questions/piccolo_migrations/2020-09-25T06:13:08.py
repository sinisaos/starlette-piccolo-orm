from piccolo.apps.migrations.auto import MigrationManager

ID = "2020-09-25T06:13:08"
VERSION = "0.12.6"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="questions")

    manager.add_column(
        table_class_name="Category",
        tablename="category",
        column_name="slug",
        column_class_name="Varchar",
        params={
            "length": 200,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    return manager
