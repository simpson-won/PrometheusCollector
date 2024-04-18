from elasticsearch import Elasticsearch
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from lib.syncmanager import SMManagerPutDeco
from config import els_address, slack_channel_name

slack_token = ""

esl_query = {
    "bool": {
        "must": {
            "match": {
                "log.level": "INFO"
            }
        },
        "filter": {
            "range": {
                "@timestamp": {
                    "gte": "now-40s", "lt": "now"
                }
            }
        }
    }
}


slack_msg_format = "[\tSystem = {system}\n\tLevel = {level}\n\tMsg = {msg}\n\tDate = {date}\n]"


def send_msg(system: str, level: str, msg: str):
    with WebClient(token=slack_token) as client:
        try:
            response = client.chat_postMessage(
                channel=slack_channel_name,
                text=slack_msg_format.join(system=system, level=level, msg=msg, date=datetime.now()))
            print(response)
        except SlackApiError as e:
            assert e.response["error"]


def get_errors(els_uri: str) -> int:
    cnt = 0
    with Elasticsearch(els_uri) as es:
        results = es.search(index="file*",
                            query=esl_query,
                            sort="@timestamp:desc")
        if len(results['hits']['hits']) > 0:
            for log in results['hits']['hits']:
                system = log['_source']['host']['hostname']
                level = log['_source']['log']['level']
                msg_parts = log['_source']['log']['log'].split(level + "  ")
                send_msg(system=system,
                         level=level,
                         msg=msg_parts[1])
                cnt += 1
    return cnt


@SMManagerPutDeco
def synchronize_metric() -> dict:
    metrics = {}
    cnt = get_errors(els_address)
    # metrics[f"{redis[2]}:{redis[3]}"] = get_metric(host=redis[2], port=int(redis[3]), user=redis[0], passwd=redis[1], is_ssl=redis_use_ssl)
    return metrics


def run():
    import os
    global slack_token
    slack_token = os.environ["SLACK_API_TOKEN"]
    synchronize_metric()
