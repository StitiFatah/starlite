from random import randint

from pydantic import BaseModel
from starlite import Starlite, Response, Router, get
from starlite.datastructures import ResponseHeader


class Resource(BaseModel):
    id: int
    name: str


@get(
    "/resources",
    response_headers={
        "Random-Header": ResponseHeader(
            description="a random number in the range 100 - 1000",
            documentation_only=True,
        )
    },
)
def retrieve_resource() -> Response[Resource]:
    return Response(
        Resource(
            id=1,
            name="my resource",
        ),
        headers={"Random-Header": str(randint(100, 1000))},
    )


def after_request_handler(response: Response) -> Response:
    response.headers.update({"Random-Header": str(randint(1, 100))})
    return response


router = Router(
    path="/router-path",
    route_handlers=[retrieve_resource],
    after_request=after_request_handler,
    response_headers={
        "Random-Header": ResponseHeader(
            description="a random number in the range 1 - 100",
            documentation_only=True,
        )
    },
)


app = Starlite(route_handlers=[router])
