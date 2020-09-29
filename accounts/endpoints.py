from starlette.responses import RedirectResponse
from starlette.authentication import requires

from accounts.forms import LoginForm, RegistrationForm
from accounts.tables import User, generate_jwt
from questions.tables import Question, Answer
from questions.helpers import get_questions, get_answers
from settings import BASE_HOST, templates
from utils import pagination


async def register(request):
    """
    Validate form, register and authenticate user
    """
    data = await request.form()
    form = RegistrationForm(data)
    username = form.username.data
    email = form.email.data
    password = form.password.data
    if request.method == "POST" and form.validate():
        if (
            await User.exists().where(User.email == email).run()
            or await User.exists().where(User.username == username).run()
        ):
            user_error = "User with that email or username already exists."
            return templates.TemplateResponse(
                "accounts/register.html",
                {
                    "request": request,
                    "form": form,
                    "user_error": user_error,
                },
            )
        query = User(
            username=username,
            email=email,
            password=password,
        )
        await query.save().run()
        results = await (
            User.select()
            .columns(User.id, User.username, User.password)
            .where((User.username == username))
            .first()
        ).run()
        valid_user = await User.login(username=username, password=password)
        if not valid_user:
            user_error = "Invalid username or password"
            return templates.TemplateResponse(
                "accounts/login.html",
                {
                    "request": request,
                    "form": form,
                    "user_error": user_error,
                },
            )
        response = RedirectResponse(BASE_HOST, status_code=302)
        response.set_cookie(
            "jwt", generate_jwt(results["username"]), httponly=True
        )
        return response
    return templates.TemplateResponse(
        "accounts/register.html", {"request": request, "form": form}
    )


async def login(request):
    """
    Validate form, login and authenticate user
    """
    path = request.query_params["next"]
    data = await request.form()
    form = LoginForm(data)
    username = form.username.data
    password = form.password.data
    if request.method == "POST" and form.validate():
        if await User.exists().where(User.username == username).run():
            results = await (
                User.select()
                .columns(User.id, User.username, User.password)
                .where((User.username == username))
                .first()
            ).run()
            valid_user = await User.login(username=username, password=password)
            if not valid_user:
                user_error = "Invalid username or password"
                return templates.TemplateResponse(
                    "accounts/login.html",
                    {
                        "request": request,
                        "form": form,
                        "user_error": user_error,
                    },
                )
            response = RedirectResponse(BASE_HOST + path, status_code=302)
            response.set_cookie(
                "jwt", generate_jwt(results["username"]), httponly=True
            )
            return response
        else:
            user_error = "Please register you don't have account"
            return templates.TemplateResponse(
                "accounts/login.html",
                {
                    "request": request,
                    "form": form,
                    "user_error": user_error,
                },
            )

    return templates.TemplateResponse(
        "accounts/login.html", {"request": request, "form": form}
    )


@requires("authenticated", redirect="index")
async def profile(request):
    if request.user.is_authenticated:
        a = Answer
        p = Question
        u = User
        auth_user = request.user.display_name
        results = await u.select().where(u.username == auth_user).run()
        questions_count = (
            await p.count().where(p.user.username == auth_user).run()
        )
        answers_count = (
            await a.count().where(a.ans_user.username == auth_user).run()
        )
        return templates.TemplateResponse(
            "accounts/profile.html",
            {
                "request": request,
                "results": results,
                "auth_user": auth_user,
                "questions_count": questions_count,
                "answers_count": answers_count,
            },
        )


@requires("authenticated", redirect="index")
async def profile_questions(request):
    p = Question
    auth_user = request.user.display_name
    page_query = pagination.get_page_number(url=request.url)
    count = await p.count().where(p.user.username == auth_user).run()
    paginator = pagination.Pagination(page_query, count)
    if request.user.is_authenticated:
        questions = (
            await get_questions()
            .where(p.user.username == auth_user)
            .limit(paginator.page_size)
            .offset(paginator.offset())
            .run()
        )
        page_controls = pagination.get_page_controls(
            url=request.url,
            current_page=paginator.current_page(),
            total_pages=paginator.total_pages(),
        )
        return templates.TemplateResponse(
            "accounts/profile_questions.html",
            {
                "request": request,
                "questions": questions,
                "page_controls": page_controls,
            },
        )


@requires("authenticated", redirect="index")
async def profile_answers(request):
    a = Answer
    auth_user = request.user.display_name
    page_query = pagination.get_page_number(url=request.url)
    count = await a.count().where(a.ans_user.username == auth_user).run()
    paginator = pagination.Pagination(page_query, count)
    if request.user.is_authenticated:
        answers = (
            await get_answers()
            .where(a.ans_user.username == auth_user)
            .limit(paginator.page_size)
            .offset(paginator.offset())
            .run()
        )
        page_controls = pagination.get_page_controls(
            url=request.url,
            current_page=paginator.current_page(),
            total_pages=paginator.total_pages(),
        )
        return templates.TemplateResponse(
            "accounts/profile_answers.html",
            {
                "request": request,
                "answers": answers,
                "page_controls": page_controls,
            },
        )


async def logout(request):
    """
    Logout user
    """
    request.session.clear()
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("jwt")
    return response
