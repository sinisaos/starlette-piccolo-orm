from .tables import Answer, Question


def get_questions():
    p = Question
    qs = p.select(
        p.id,
        p.slug,
        p.title,
        p.description,
        p.created_at,
        p.view,
        p.question_like,
        p.accepted_answer,
        p.user.username,
        p.category.name,
        p.category.slug,
    )
    return qs


def get_answers():
    a = Answer
    qs = a.select(
        a.id,
        a.content,
        a.created_at,
        a.answer_like,
        a.is_accepted_answer,
        a.ans_user.username,
        a.question.id,
    )
    return qs


def get_search_questions(q):
    p = Question
    qs = p.select(
        p.id,
        p.slug,
        p.title,
        p.description,
        p.created_at,
        p.view,
        p.question_like,
        p.accepted_answer,
        p.user.username,
        p.category.name,
        p.category.slug,
    ).where(
        (
            (p.title.ilike("%" + q + "%"))
            | (p.description.ilike("%" + q + "%"))
            | (p.user.username.ilike("%" + q + "%"))
            | (p.category.name.ilike("%" + q + "%"))
        )
    )
    return qs


def count_search_questions(q):
    p = Question
    qs = p.count().where(
        (
            (p.title.ilike("%" + q + "%"))
            | (p.description.ilike("%" + q + "%"))
            | (p.user.username.ilike("%" + q + "%"))
            | (p.category.name.ilike("%" + q + "%"))
        )
    )
    return qs
