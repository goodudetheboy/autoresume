import io
import json
import requests


def send_openai_request(
    payload: dict,
    headers: dict
) -> str:
    payload_bytes = io.BytesIO(json.dumps(payload).encode('utf-8'))

    response = requests.post(
        url="https://api.openai.com/v1/chat/completions",
        data=payload_bytes,
        headers=headers
    )
    response_json = response.json()
    content_raw = response_json["choices"][0]["message"]["content"]

    return content_raw
