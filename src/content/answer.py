import json
import os
import yaml
import urllib.parse

# Setup Jinja2 environment and load template
from jinja2 import Environment, FileSystemLoader

from content.utils import send_openai_request


file_loader = FileSystemLoader("templates")
env = Environment(
    loader=file_loader,
)
prompt_template = env.get_template("./answer_app_question_template.jinja")

# Get resume template
with open("./templates/resume_template.yaml") as file:
    resume_yaml_template = file.read()


def answer_app_question(question: str, resume: dict, job_description: str) -> tuple[dict, str]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer { os.environ.get('OPENAI_API_KEY') }"
    }
    prompt = prompt_template.render(
        resume_yaml_template=resume_yaml_template,
        resume=yaml.dump(resume),
        job_description=job_description,
        app_question=question
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

    response = send_openai_request(payload, headers)

    response_json = json.loads(response)

    return response_json, prompt
