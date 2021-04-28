import datetime

from starlette.authentication import requires
from starlette.responses import RedirectResponse

from accounts.tables import User
from questions.forms import (
    AcceptedAnswerForm,
    AnswerEditForm,
    AnswerForm,
    AnswerLikesForm,
    QuestionEditForm,
    QuestionForm,
    QuestionLikesForm,
)
from questions.helpers import (
    count_search_questions,
    get_answers,
    get_questions,
    get_search_questions,
)
from questions.tables import Answer, Category, Question
from settings import BASE_HOST, templates
from utils import pagination


async def questions_list(request):
    """
    All questions
    """
    p = Question
    # pagination
    page_query = pagination.get_page_number(url=request.url)
    count = await p.count().run()
    paginator = pagination.Pagination(page_query, count)
    # filter and sort
    try:
        tab = request.query_params["tab"]
        if tab == "oldest":
            results = (
                await get_questions()
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=True)
                .run()
            )
        if tab == "unsolved":
            count = await p.count().where(p.accepted_answer == False).run()
            paginator = pagination.Pagination(page_query, count)
            results = (
                await get_questions()
                .where(p.accepted_answer == False)
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=False)
                .run()
            )
        if tab == "solved":
            count = await p.count().where(p.accepted_answer == True).run()
            paginator = pagination.Pagination(page_query, count)
            results = (
                await get_questions()
                .where(p.accepted_answer == True)
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=False)
                .run()
            )
    except KeyError:
        results = (
            await get_questions()
            .limit(paginator.page_size)
            .offset(paginator.offset())
            .order_by(p.id, ascending=False)
            .run()
        )
    # counting answers per question
    answer_count = [
        await p.raw(
            f"select count(answer.id) from answer "
            f"join question on answer.question = question.id "
            f"where question.id = {item['id']};"
        ).run()
        for item in results
    ]
    # categories
    c = Category
    categories = await c.select().order_by(c.name, ascending=True).run()
    category_count = [
        await p.count().where(p.category.name == item["name"]).run()
        for item in categories
    ]
    # pagination links in templates
    page_controls = pagination.get_page_controls(
        url=request.url,
        current_page=paginator.current_page(),
        total_pages=paginator.total_pages(),
    )
    return templates.TemplateResponse(
        "questions/questions_list.html",
        {
            "request": request,
            "results": zip(results, answer_count),
            "categories": zip(categories, category_count),
            "page_controls": page_controls,
        },
    )


async def questions_search(request):
    """
    Search questions
    """
    try:
        page_query = pagination.get_page_number(url=request.url)
        q = request.query_params["q"]
        tab = request.query_params["tab"]
        p = Question
        count = await p.count().run()
        paginator = pagination.Pagination(page_query, count)
        results = (
            await get_search_questions(q)
            .limit(paginator.page_size)
            .offset(paginator.offset())
            .order_by(p.id, ascending=False)
            .run()
        )
        if tab == "oldest":
            count = await count_search_questions(q).run()
            paginator = pagination.Pagination(page_query, count)
            results = (
                await get_search_questions(q)
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=True)
                .run()
            )
        if tab == "unsolved":
            count = (
                await count_search_questions(q)
                .where(p.accepted_answer == False)
                .run()
            )
            paginator = pagination.Pagination(page_query, count)
            results = (
                await get_search_questions(q)
                .where(p.accepted_answer == False)
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=True)
                .run()
            )
        if tab == "solved":
            count = (
                await count_search_questions(q)
                .where(p.accepted_answer == True)
                .run()
            )
            paginator = pagination.Pagination(page_query, count)
            results = (
                await get_search_questions(q)
                .where(p.accepted_answer == True)
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=True)
                .run()
            )
    except KeyError:
        p = Question
        page_query = pagination.get_page_number(url=request.url)
        count = await count_search_questions(q).run()
        paginator = pagination.Pagination(page_query, count)
        results = (
            await get_search_questions(q)
            .limit(paginator.page_size)
            .offset(paginator.offset())
            .order_by(p.id, ascending=False)
            .run()
        )
    c = Category
    categories = await c.select().order_by(c.name, ascending=True).run()
    category_count = [
        await p.count().where(p.category.name == item["name"]).run()
        for item in categories
    ]
    answer_count = [
        await p.raw(
            f"select count(answer.id) from answer "
            f"join question on answer.question = question.id "
            f"where question.id = {item['id']};"
        ).run()
        for item in results
    ]

    page_controls = pagination.get_page_controls(
        url=request.url,
        current_page=paginator.current_page(),
        total_pages=paginator.total_pages(),
    )
    return templates.TemplateResponse(
        "questions/questions_search.html",
        {
            "request": request,
            "results": zip(results, answer_count),
            "categories": zip(categories, category_count),
            "page_controls": page_controls,
            "count": count,
            "q": q,
        },
    )


async def questions_categories(request):
    """
    Questions categories
    """
    p = Question
    category = request.path_params["category"]
    page_query = pagination.get_page_number(url=request.url)
    count = await p.count().where(p.category.name == category).run()
    paginator = pagination.Pagination(page_query, count)
    try:
        tab = request.query_params["tab"]
        if tab == "oldest":
            results = (
                await get_questions()
                .where(p.category.name == category)
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=True)
                .run()
            )
        if tab == "unsolved":
            count = (
                await p.count()
                .where(
                    (p.accepted_answer == False)
                    & (p.category.name == category)
                )
                .run()
            )
            paginator = pagination.Pagination(page_query, count)
            results = (
                await get_questions()
                .where(
                    (p.accepted_answer == False)
                    & (p.category.name == category)
                )
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=False)
                .run()
            )
        if tab == "solved":
            count = (
                await p.count()
                .where(
                    (p.accepted_answer == True) & (p.category.name == category)
                )
                .run()
            )
            paginator = pagination.Pagination(page_query, count)
            results = (
                await get_questions()
                .where(
                    (p.accepted_answer == True) & (p.category.name == category)
                )
                .limit(paginator.page_size)
                .offset(paginator.offset())
                .order_by(p.id, ascending=False)
                .run()
            )
    except KeyError:
        results = (
            await get_questions()
            .where(p.category.name == category)
            .limit(paginator.page_size)
            .offset(paginator.offset())
            .order_by(p.id, ascending=False)
            .run()
        )
    answer_count = [
        await p.raw(
            f"select count(answer.id) from answer "
            f"join question on answer.question = question.id "
            f"where question.id = {item['id']};"
        ).run()
        for item in results
    ]
    c = Category
    categories = await c.select().order_by(c.name, ascending=True).run()
    category_count = [
        await p.count().where(p.category.name == item["name"]).run()
        for item in categories
    ]
    page_controls = pagination.get_page_controls(
        url=request.url,
        current_page=paginator.current_page(),
        total_pages=paginator.total_pages(),
    )
    return templates.TemplateResponse(
        "questions/questions_categories.html",
        {
            "request": request,
            "results": zip(results, answer_count),
            "categories": zip(categories, category_count),
            "page_controls": page_controls,
            "r": results,
        },
    )


async def question_detail(request):
    """
    One question with answers
    """
    request_path_id = request.path_params["id"]
    path = request.url.path
    p = Question
    results = (
        await get_questions().where(p.id == request_path_id).first().run()
    )
    a = Answer
    answers = (
        await get_answers()
        .where(a.question.id == request_path_id)
        .order_by(a.id, ascending=False)
        .run()
    )
    answers_count = (
        await a.count().where(a.question.id == request_path_id).run()
    )
    # update question views per session
    session_key = f"viewed_question_{results['id']}"
    if not request.session.get(session_key, False):
        await p.update({p.view: p.view + 1}).where(
            p.id == int(request_path_id)
        ).run()
        request.session[session_key] = True
    qus_data = await request.form()
    question_likes_form = QuestionLikesForm(qus_data)
    ans_data = await request.form()
    likes_form = AnswerLikesForm(ans_data)
    accepted_data = await request.form()
    accepted_form = AcceptedAnswerForm(accepted_data)
    try:
        # answer like per session
        if request.method == "POST" and likes_form.validate():
            session_key_like = f"liked_answer_{likes_form.answer_id.data}"
            if not request.session.get(session_key_like, False):
                await a.update({a.answer_like: a.answer_like + 1}).where(
                    a.id == int(likes_form.answer_id.data)
                ).run()
                request.session[session_key_like] = True
                return RedirectResponse(BASE_HOST + path, status_code=302)
    except ValueError:
        # question like per session
        if request.method == "POST" and question_likes_form.validate():
            session_key_quslike = f"liked_question_{question_likes_form.data}"
            if not request.session.get(session_key_quslike, False):
                await p.update({p.question_like: p.question_like + 1}).where(
                    p.id == int(question_likes_form.question_id.data)
                ).run()
                request.session[session_key_quslike] = True
                return RedirectResponse(BASE_HOST + path, status_code=302)
    return templates.TemplateResponse(
        "questions/question_detail.html",
        {
            "request": request,
            "path": path,
            "item": results,
            "answers": answers,
            "answers_count": answers_count,
            "likes_form": likes_form,
            "question_likes_form": question_likes_form,
            "accepted_form": accepted_form,
        },
    )


@requires("authenticated")
async def question_create(request):
    """
    Question form
    """
    u = User
    c = Category
    session_user = (
        await u.select(u.id, u.username)
        .where(u.username == request.user.username)
        .first()
        .run()
    )
    data = await request.form()
    form = QuestionForm(data)
    form.category.choices = [
        (item["id"], item["name"]) for item in await c.select().run()
    ]
    title = form.title.data
    if request.method == "POST" and form.validate():
        query = Question(
            title=title,
            slug="-".join(title.lower().split()),
            description=form.description.data,
            created_at=datetime.datetime.now(),
            category=form.category.data,
            user=session_user["id"],
        )
        await query.save().run()
        return RedirectResponse(url="/questions", status_code=302)
    return templates.TemplateResponse(
        "questions/question_create.html",
        {
            "request": request,
            "form": form,
        },
    )


@requires("authenticated")
async def question_edit(request):
    """
    Question edit form
    """
    p = Question
    c = Category
    request_path_id = request.path_params["id"]
    # only question owner can edit question
    try:
        question = (
            await get_questions()
            .where(
                (p.id == request_path_id)
                & (p.user.username == request.user.username)
            )
            .first()
            .run()
        )
        data = await request.form()
        form = QuestionEditForm(obj=question, formdata=data)
        new_form_value, form.description.data = (
            form.description.data,
            question["description"],
        )
        form.category.choices = [
            (item["id"], item["name"]) for item in await c.select().run()
        ]
        title = form.title.data
        if request.method == "POST" and form.validate():
            await p.update(
                {
                    p.title: title,
                    p.slug: "-".join(title.lower().split()),
                    p.description: new_form_value,
                    p.category: form.category.data,
                }
            ).where(p.id == request_path_id).run()
            return RedirectResponse(url="/accounts/profile", status_code=302)
        return templates.TemplateResponse(
            "questions/question_edit.html",
            {
                "request": request,
                "form": form,
                "question": question,
            },
        )
    except TypeError:
        return templates.TemplateResponse(
            "403.html",
            {
                "request": request,
            },
        )


@requires("authenticated")
async def question_delete(request):
    """
    Delete question
    """
    p = Question
    request_path_id = request.path_params["id"]
    if request.method == "POST":
        await p.delete().where(p.id == request_path_id).run()
        return RedirectResponse(url="/accounts/profile", status_code=302)


@requires("authenticated")
async def answer_create(request):
    """
    Answer form
    """
    request_path_id = int(request.query_params["next"].split("/")[2])
    request_query_next = request.query_params["next"]
    data = await request.form()
    form = AnswerForm(data)
    u = User
    session_user = (
        await u.select(u.id, u.username)
        .where(u.username == request.user.username)
        .first()
        .run()
    )
    if request.method == "POST" and form.validate():
        query = Answer(
            content=form.content.data,
            created_at=datetime.datetime.now(),
            answer_like=0,
            is_accepted_answer=False,
            question=request_path_id,
            ans_user=session_user["id"],
        )
        await query.save().run()
        return RedirectResponse(
            BASE_HOST + request_query_next, status_code=302
        )
    return templates.TemplateResponse(
        "questions/answer_create.html",
        {
            "request": request,
            "form": form,
            "next": request_query_next,
        },
    )


@requires("authenticated")
async def answer_edit(request):
    """
    Answer edit form
    """
    request_path_id = int(request.path_params["id"])
    a = Answer
    # only answer owner can edit answer
    try:
        answer = (
            await get_answers()
            .where(
                (a.id == request_path_id)
                & (a.ans_user.username == request.user.username)
            )
            .first()
            .run()
        )
        data = await request.form()
        form = AnswerEditForm(data)
        new_form_value, form.content.data = (
            form.content.data,
            answer["content"],
        )
        if request.method == "POST" and form.validate():
            await a.update({a.content: new_form_value}).where(
                a.id == request_path_id
            ).run()
            return RedirectResponse("/accounts/profile", status_code=302)
        return templates.TemplateResponse(
            "questions/answer_edit.html",
            {"request": request, "form": form, "answer": answer},
        )
    except TypeError:
        return templates.TemplateResponse(
            "403.html",
            {
                "request": request,
            },
        )


@requires("authenticated")
async def answer_delete(request):
    """
    Delete answer
    """
    p = Question
    a = Answer
    request_path_id = int(request.path_params["id"])
    answer = list(await a.select().where(a.id == request_path_id).run())[0]
    if request.method == "POST":
        if answer["is_accepted_answer"] == True:
            await p.update({p.accepted_answer: False}).where(
                p.id == answer["question"]
            ).run()
        await a.delete().where(a.id == request_path_id).run()
        return RedirectResponse("/accounts/profile", status_code=302)


async def accepted_answer(request):
    """
    Accepted answer form
    """
    request_query_next = request.query_params["next"]
    request_path_id = int(request_query_next.split("/")[2])
    answer_id = int(request_query_next.split("/")[-1])
    path = "/".join(request_query_next.split("/")[:-1])
    p = Question
    a = Answer
    data = await request.form()
    form = AcceptedAnswerForm(data)
    if request.method == "POST" and form.validate():
        # accept answer
        await a.update({a.is_accepted_answer: True}).where(
            a.id == answer_id
        ).run()
        await p.update({p.accepted_answer: True}).where(
            p.id == request_path_id
        ).run()
        return RedirectResponse(BASE_HOST + path, status_code=302)
    return templates.TemplateResponse(
        "questions/accepted_answer.html",
        {
            "request": request,
            "form": form,
            "path": path,
            "answer_id": answer_id,
        },
    )
