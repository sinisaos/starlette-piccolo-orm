from starlette.routing import Route, Router

from questions.endpoints import (accepted_answer, answer_create,
                                 question_detail, questions_categories,
                                 questions_list, questions_search)

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
            "/answer-create",
            endpoint=answer_create,
            methods=["GET", "POST"],
            name="answer_create",
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
