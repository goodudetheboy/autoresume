from jinja2 import Environment, FileSystemLoader
import json
import os
import yaml

from content.utils import send_openai_request

# Setup Jinja2 environment and load template
file_loader = FileSystemLoader('templates')
env = Environment(
    loader=file_loader,
)
prompt_template = env.get_template('./tailor_resume_prompt_template.jinja')

# Get resume template
with open("./templates/resume_template.yaml") as file:
    resume_yaml_template = file.read()


def tailor_resume_by_job_description(resume: dict, job_description: str) -> dict:
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

    response = send_openai_request(payload, headers)

    response_json = json.loads(response)

    return response_json
