from litestar import Litestar, get, post
from dataclasses import dataclass
from willy_gaby.query import Profile
from willy_gaby.match import check_match
from typing import Annotated
from litestar.params import Body

@dataclass
class MatchRequest:
    profileA: Profile
    profileB: Profile

@get("/")
async def index() -> str:
    return "Hello, world!"


@post("/matchs/execute")
async def request_match(data: Annotated[MatchRequest, Body(title="Create User", description="Create a new user.")]) -> dict[str, int]:
    return check_match(data.profileA, data.profileB)

app = Litestar([index, request_match])

# curl -X POST  --data '{"profileA":{ "user_id": 1, "name": "john", "questions": { "description": "I am in the nuts house" } },"profileB":{ "user_id": 2, "name": "does", "questions": { "description": "I am crazy" } }}' 'http://localhost:8000/matchs/execute'