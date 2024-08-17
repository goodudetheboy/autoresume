import yaml
from flask import Flask, render_template

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')

@app.route('/')
def index():
    # Load the YAML content
    with open('./templates/resume_template.yaml', 'r') as file:
        resume_template = file.read()
    
    return render_template('index.html', resume_yaml_template=resume_template)

if __name__ == '__main__':
    app.run(debug=True)