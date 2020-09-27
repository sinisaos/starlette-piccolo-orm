from starlette.routing import Route, Router

from accounts.endpoints import login, logout, register

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
    ]
)
