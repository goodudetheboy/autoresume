import yaml

from pydantic import ValidationError
from templates.pydantic_models import Resume


def validate_resume(resume_yaml: str) -> tuple[bool, dict | None]:
    try:
        # Load the YAML content
        parsed_yaml = yaml.safe_load(resume_yaml)

        # Validate the parsed YAML data using the Pydantic model
        Resume(**parsed_yaml)

        return True, None
    except yaml.YAMLError as e:
        return False, {"error": "Invalid YAML", "details": [str(e)]}

    except ValidationError as e:
        # Return Pydantic validation errors
        details = []
        for error in e.errors():
            location, msg = "->".join([str(loc)
                                       for loc in error["loc"]]), error["msg"]
            details.append(f"Problem at [{location}] with error [{msg}]")
        return False, {
            "error": "Schema validation failed",
            "details": details
        }

    except Exception as e:
        return False, {"error": "An unknown error occurred"}
