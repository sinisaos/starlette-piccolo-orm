from piccolo.apps.migrations.auto import MigrationManager
from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.table import Table


class Category(Table, tablename="category"):
    pass


class User(Table, tablename="piccolo_user"):
    pass


ID = "2020-09-12T20:02:49"
VERSION = "0.12.6"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="questions")

    manager.add_table("Question", tablename="question")

    manager.add_column(
        table_class_name="Question",
        tablename="question",
        column_name="title",
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

    manager.add_column(
        table_class_name="Question",
        tablename="question",
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

    manager.add_column(
        table_class_name="Question",
        tablename="question",
        column_name="description",
        column_class_name="Text",
        params={
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Question",
        tablename="question",
        column_name="created_at",
        column_class_name="Timestamp",
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Question",
        tablename="question",
        column_name="view",
        column_class_name="Integer",
        params={
            "default": 0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Question",
        tablename="question",
        column_name="question_like",
        column_class_name="Integer",
        params={
            "default": 0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Question",
        tablename="question",
        column_name="accepted_answer",
        column_class_name="Boolean",
        params={
            "default": False,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Question",
        tablename="question",
        column_name="user",
        column_class_name="ForeignKey",
        params={
            "references": User,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    manager.add_column(
        table_class_name="Question",
        tablename="question",
        column_name="category",
        column_class_name="ForeignKey",
        params={
            "references": Category,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
        },
    )

    return manager
