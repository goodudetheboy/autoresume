import io
import os
import uuid
import yaml
import tempfile

from content.validate import validate_resume
from content.render import render_data, render_latex_to_pdf
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
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

        result, errors = validate_resume(yaml_content)

        if result:
            return jsonify({"result": "valid"}), 200
        else:
            errors["result"] = "invalid"
            return jsonify(errors), 200

    except Exception as e:
        return jsonify({"error": "An unknown error occurred"}), 500


@app.route("/api/resume/render", methods=["POST"])
def post_generate_resume():
    try:
        # Get JSON data from the request
        data = request.get_json()
        yaml_content = data.get("resume")

        if yaml_content is None:
            return jsonify({"error": "No resume provided"}), 400

        result, errors = validate_resume(yaml_content)

        if not result:
            errors["result"] = "invalid"
            return jsonify(errors), 200

        latex_content = render_data(yaml.safe_load(yaml_content))

        with tempfile.TemporaryDirectory(dir=os.getcwd()) as temp_dir:
            resume_name = str(uuid.uuid4())
            render_result = render_latex_to_pdf(
                latex_content, temp_dir, resume_name)
            if not render_result:
                return jsonify({"error": "Unable to render your resume to PDF"}), 500
            resume_path = os.path.join(temp_dir, f"{resume_name}.pdf")

            return_data = io.BytesIO()
            with open(resume_path, "rb") as file:
                return_data.write(file.read())
            return_data.seek(0)

            return send_file(
                return_data,
                mimetype="application/pdf",
                as_attachment=True,
                download_name="generated.pdf")
    except Exception as e:
        print(e)
        return jsonify({"error": "An unknown error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True)
