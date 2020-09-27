from starlette.endpoints import HTTPEndpoint

from settings import templates


class HomeEndpoint(HTTPEndpoint):
    async def get(self, request):
        content = "Piccolo + ASGI"

        return templates.TemplateResponse(
            "index.html", {"request": request, "content": content}
        )
