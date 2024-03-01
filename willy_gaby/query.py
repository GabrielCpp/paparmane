import requests
import phpserialize
from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv
import json
from willy_gaby.match import check_match

load_dotenv()


@dataclass
class Profile:
    user_id: int
    name: str
    questions: dict[str, str]

    def to_prompt(self):
        return "\n".join(
            [
                f"{question} : {answer}"
                for question, answer in self.questions.items()
            ]
        )


def get_matches(user_id: int, token: str):
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

        questions[obj[b"label"].decode("utf8")] = value

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


# token = os.getenv("WORDPRESS_TOKEN")


# users = []
# for userId in get_users(token):
#     users.append(get_matches(userId, token))

# with open("matchs.json", "w") as f:
#     for userA in users:
#         for userB in users:
#             if userA == userB:
#                 continue

#             print(
#                 f""" 
#   ### Instruction
#   Determine if the following two profiles are a match. Answer with "yes" or "no", then explain why.
#   ### Profile A
#   {userA.to_prompt()}
#   ### Profile B 
#   {userB.to_prompt()}
#   ### Output
#   """
#             )

#             break

            # f.write(json.dumps(check_match(userA, userB)) + "\n")
