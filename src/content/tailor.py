from jinja2 import Environment, FileSystemLoader
import io
import json
import requests
import os
import yaml

# Setup Jinja2 environment and load template
file_loader = FileSystemLoader('templates')
env = Environment(
        loader=file_loader, 
    )
prompt_template = env.get_template('./tailor_resume_prompt_template.jinja')

# Get resume template
with open("./templates/resume_template.yaml") as file:
    resume_yaml_template = file.read()

def tailor_resume_by_job_description(resume: dict, job_description: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer { os.environ.get('OPENAI_API_KEY') }"
    }

    prompt = prompt_template.render(
        resume_yaml_template=resume_yaml_template,
        resume=yaml.dump(resume),
        job_description=job_description
    )

    content = []
    content.append(
        {
            "type": "text",
            "text": prompt
        })

    payload = {
        "model": "gpt-4o-mini",
      "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": 10000
    }

    response = _send_request(payload, headers)

    response_json = json.loads(response)

    return response_json

def _send_request(
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

