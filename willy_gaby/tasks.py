from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import datetime
import json

# Create a client.
client = tasks_v2.CloudTasksClient()

# Construct the fully qualified queue name.
project = "paparman"
location = "northamerica-northeast1"
queue = "match-profile"
task_queue = client.queue_path(project, location, queue)
schedule_time = datetime.datetime.now(tz=datetime.timezone.utc)

body = {
    "name": "Gaby",
}

url = "https://paparmane-ai-e3d2pnjrvq-uc.a.run.app/users/register_match"

def queue_match(profileA, profileB, schedule_time):
    # Add the task to the queue.
    task = tasks_v2.Task(
        http_request=tasks_v2.HttpRequest(
            http_method=tasks_v2.HttpMethod.POST,
            url=url,
            oidc_token=tasks_v2.OidcToken(
                service_account_email="706612247533-compute@developer.gserviceaccount.com",
                #audience=audience,
            ),
            headers={"Content-type": "application/json"},
            body=json.dumps(body).encode(),
        ),
        schedule_time=schedule_time,
    )

    client.create_task(parent=task_queue, task=task)


