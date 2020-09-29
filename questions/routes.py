from starlette.routing import Route, Router

from questions.endpoints import (
    accepted_answer,
    answer_create,
    answer_edit,
    answer_delete,
    question_detail,
    questions_categories,
    questions_list,
    questions_search,
    question_create,
    question_edit,
    question_delete,
)

questions_routes = Router(
    [
        Route(
            "/",
            endpoint=questions_list,
            methods=["GET", "POST"],
            name="questions_list",
        ),
        Route(
            "/category/{category:str}",
            endpoint=questions_categories,
            methods=["GET"],
            name="questions_categories",
        ),
        Route(
            "/{id:int}/{slug:str}",
            endpoint=question_detail,
            methods=["GET", "POST", "PATCH"],
            name="question_detail",
        ),
        Route(
            "/create",
            endpoint=question_create,
            methods=["GET", "POST"],
            name="question_create",
        ),
        Route(
            "/edit/{id:int}",
            endpoint=question_edit,
            methods=["GET", "POST"],
            name="question_edit",
        ),
        Route(
            "/delete/{id:int}",
            endpoint=question_delete,
            methods=["GET", "POST"],
            name="question_delete",
        ),
        Route(
            "/answer-create",
            endpoint=answer_create,
            methods=["GET", "POST"],
            name="answer_create",
        ),
        Route(
            "/answer-edit/{id:int}",
            endpoint=answer_edit,
            methods=["GET", "POST"],
            name="answer_edit",
        ),
        Route(
            "/answer-delete/{id:int}",
            endpoint=answer_delete,
            methods=["GET", "POST"],
            name="answer_delete",
        ),
        Route(
            "/accepted-answer",
            endpoint=accepted_answer,
            methods=["GET", "POST"],
            name="accepted_answer",
        ),
        Route(
            "/search",
            endpoint=questions_search,
            methods=["GET"],
            name="questions_search",
        ),
    ]
)
