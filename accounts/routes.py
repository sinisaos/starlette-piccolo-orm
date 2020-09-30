from starlette.routing import Route, Router

from accounts.endpoints import (login, logout, profile, profile_answers,
                                profile_questions, register, user_delete)

accounts_routes = Router(
    [
        Route("/login", endpoint=login, methods=["GET", "POST"], name="login"),
        Route(
            "/register",
            endpoint=register,
            methods=["GET", "POST"],
            name="register",
        ),
        Route(
            "/logout", endpoint=logout, methods=["GET", "POST"], name="logout"
        ),
        Route(
            "/user-delete/{id:int}",
            endpoint=user_delete,
            methods=["GET", "POST"],
            name="user_delete",
        ),
        Route("/profile", endpoint=profile, methods=["GET"], name="profile"),
        Route(
            "/profile/questions",
            endpoint=profile_questions,
            methods=["GET"],
            name="profile_questions",
        ),
        Route(
            "/profile/answers",
            endpoint=profile_answers,
            methods=["GET"],
            name="profile_answers",
        ),
    ]
)
