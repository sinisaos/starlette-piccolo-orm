from piccolo.apps.migrations.auto import MigrationManager


ID = "2021-06-30T07:57:01"
VERSION = "0.23.0"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="questions")

    manager.rename_column(
        table_class_name="Question",
        tablename="question",
        old_column_name="user",
        new_column_name="question_user",
    )

    return manager
