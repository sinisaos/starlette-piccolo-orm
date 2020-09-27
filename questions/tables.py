from piccolo.columns import (Boolean, ForeignKey, Integer, Text, Timestamp,
                             Varchar)
from piccolo.columns.readable import Readable
from piccolo.table import Table

from accounts.tables import User


class Category(Table):
    """
    An category table.
    """

    name = Varchar(length=200)
    slug = Varchar(length=200)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Question(Table):
    """
    An question table.
    """

    title = Varchar(length=200)
    slug = Varchar(length=200)
    description = Text()
    created_at = Timestamp()
    view = Integer(default=0)
    question_like = Integer(default=0)
    accepted_answer = Boolean(default=False)
    user = ForeignKey(references=User)
    category = ForeignKey(references=Category)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.title])


class Answer(Table):
    """
    An answer table.
    """

    content = Text()
    created_at = Timestamp()
    answer_like = Integer(default=0)
    is_accepted_answer = Boolean(default=False)
    ans_user = ForeignKey(references=User)
    question = ForeignKey(references=Question)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.question])
