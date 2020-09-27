from piccolo.apps.migrations.auto import MigrationManager

ID = "2020-09-12T18:56:15"
VERSION = "0.12.6"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="questions")

    manager.add_table("Category", tablename="category")

    manager.add_column(
        table_class_name="Category",
        tablename="category",
        column_name="name",
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
