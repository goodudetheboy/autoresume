import yaml
from flask import Flask, render_template, request, jsonify
from templates.pydantic_models import Resume
from pydantic import ValidationError

app = Flask(__name__,
            template_folder="frontend/templates",
            static_folder="frontend/static")


@app.route("/")
def index():
    # Load the YAML content
    with open("./templates/resume_template.yaml", "r") as file:
        resume_template = file.read()

    return render_template("index.html", resume_yaml_template=resume_template)


@app.route("/api/resume/validate", methods=["POST"])
def post_validate_resume():
    try:
        # Get JSON data from the request
        data = request.get_json()
        yaml_content = data.get("resume")

        if yaml_content is None:
            return jsonify({"error": "No resume provided"}), 400

        # Load the YAML content
        parsed_yaml = yaml.safe_load(yaml_content)

        # Validate the parsed YAML data using the Pydantic model
        Resume(**parsed_yaml)

        return jsonify({"result": "valid"}), 200

    except yaml.YAMLError as e:
        return jsonify({"result": "invalid", "error": "Invalid YAML", "details": [str(e)]}), 200

    except ValidationError as e:
        # Return Pydantic validation errors
        details = []
        for error in e.errors():
            location, msg = "->".join([str(loc)
                                       for loc in error["loc"]]), error["msg"]
            details.append(f"Problem at [{location}] with error [{msg}]")
        return jsonify(
            {
                "result": "invalid",
                "error": "Schema validation failed",
                "details": details
            }), 200

    except Exception as e:
        return jsonify({"error": "An unknown error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True)
