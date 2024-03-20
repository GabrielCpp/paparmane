import requests
import phpserialize
from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv
import json
from willy_gaby.match import check_match

load_dotenv()

from google.cloud import storage, firestore
import os 
from dataclasses import asdict

project_id = os.getenv("PROJECT_ID")
db = firestore.AsyncClient(project=project_id, database="paparmane")

@dataclass
class Profile:
    user_id: int
    name: str
    questions: dict[str, str]

    def to_prompt(self):
        return "\n".join(
            [
                f"{question} {answer}"
                for question, answer in self.questions.items()
            ]
        )

async def create_user_profile_db(profile: Profile):
    await db.collection("users").document(profile.user_id).set(asdict(profile))

async def get_user_user_profile_db(user_id):
    doc_ref = db.collection("users").document(str(user_id))
    doc = await doc_ref.get()

    if not doc.exists:
        return None

    return Profile(**doc.to_dict())

def all_user_user_profile_db():
    return db.collection("users").order_by("name", direction=firestore.Query.ASCENDING).stream()

def all_user_user_profile_ids_db():
    return db.collection("users").stream()
    doc.reference.path

async def set_match(profileA: Profile, profileB: Profile, answer: str):
    await db.collection("matches").document(f"{profileA.user_id}_{profileB.user_id}").set({
        "profileA": asdict(profileA),
        "profileB": asdict(profileB),
        "answer": answer,
        "match": "YES" in answer
    })

def get_user_profile(user_id: int, token: str) -> Profile:
    response = requests.get(
        f"https://paparmaneintergeneration.com/wp-json/mo/v1/full_form?custom_id={user_id}",
        headers={"Authorization": "Bearer "},
    )

    metadata = response.json()
    questions = {}

    for meta in metadata:
        arm_form_field_option = meta["arm_form_field_option"]
        if arm_form_field_option is None:
            continue

        obj = phpserialize.loads(arm_form_field_option.encode("utf8"))
        value = meta["meta_value"]

        # // mean it is an uploaded file
        if value.startswith("//") or value.strip() == "":
            continue

        try:
            value2 = phpserialize.loads(value.encode("utf8"))
            value = ", ".join([v.decode("utf8") for v in value2.values()])
        except:
            pass

        key = obj[b"label"].decode("utf8").strip()
        if key == "":
            continue

        questions[key] = value

    if len(metadata) == 0:
        return None

    return Profile(user_id=user_id, name=metadata[0]["user_login"], questions=questions)


def get_users(token: str):
    response = requests.get(
        "https://paparmaneintergeneration.com/wp-json/mo/v1/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    users = response.json()

    return [user["ID"] for user in users if not user["user_login"].startswith("admin")]


