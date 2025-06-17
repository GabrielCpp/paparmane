import os
import datetime
import logging
from litestar import Litestar, get, post, Request, Response, MediaType
from litestar.exceptions import HTTPException
from litestar.logging import LoggingConfig
from dataclasses import dataclass
from paparmane.query import Profile, get_users, get_user_profile, create_user_profile_db, all_user_user_profile_ids_db, all_user_user_profile_db, set_match, get_user_user_profile_db
from paparmane.match import check_match
from paparmane.tasks import queue_match
from typing import Annotated
from litestar.params import Body

TOKEN = os.getenv("WORDPRESS_TOKEN")
logging_config = LoggingConfig(
    root={"level": logging.getLevelName(logging.INFO), "handlers": ["console"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
)

@dataclass
class SpotCheckMatchRequest:
    profileA: Profile
    profileB: Profile


@dataclass
class MatchRequest:
    profileA_id: str
    profileB_id: str

@post("/users/sync")
async def sync_users() -> None:
    user_ids = set(get_users(TOKEN))

    for user_id in user_ids:
        profile = get_user_profile(user_id, TOKEN)

        if profile:
            await create_user_profile_db(profile)


    async for profile in all_user_user_profile_db():
        if profile.id not in user_ids:
            await profile.reference.delete()


@post("/users/make_matchs")
async def make_matchs() -> None:
    profiles = []
    async for profile in all_user_user_profile_ids_db():
        profiles.append(int(profile.reference.path[-1]))

    profiles = sorted(profiles)

    schedule_time = datetime.datetime.now(datetime.timezone.utc)
    bucket_index = 0

    for index in range(0, len(profiles)):
        for index2 in range(index + 1, len(profiles)):
            bucket_index += 1
            if bucket_index % 3 == 0:
                schedule_time = schedule_time + datetime.timedelta(minutes=4)

            queue_match(profiles[index], profiles[index2], schedule_time)

@post("/users/register_match")
async def register_match(data: Annotated[MatchRequest, Body(title="Check match", description="Check match of existing profil")]) -> None:
    profileA = await get_user_user_profile_db(data.profileA_id)
    profileB = await get_user_user_profile_db(data.profileB_id)

    if not profileA or not profileB:
        return {"error": "Profile not found"}

    answer = check_match(profileA, profileB)
    await set_match(profileA, profileB, answer)
    return answer

@post("/matchs/spot_check_match")
async def spot_check_match(data: Annotated[SpotCheckMatchRequest, Body(title="Check match", description="Check match with custom profile")]) -> dict[str, int]:
    return check_match(data.profileA, data.profileB)


def plain_text_exception_handler(request: Request, exc: Exception) -> Response:
    """Default handler for exceptions subclassed from HTTPException."""
    request.logger.error(exc)
    return Response(
        media_type=MediaType.JSON,
        content={"message": "Internal Server Error"},
        status_code=500,
    )


app = Litestar(
    route_handlers=[sync_users, make_matchs, register_match, spot_check_match],
    exception_handlers={Exception: plain_text_exception_handler},
    logging_config=logging_config
)

