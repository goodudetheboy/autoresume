import yaml
from jinja2 import Environment, FileSystemLoader
import os

# Setup Jinja2 environment and load template
file_loader = FileSystemLoader("templates")
env = Environment(
		loader=file_loader, 
		comment_start_string="{=",
		comment_end_string="=}",
	)
template = env.get_template("resume_template.jinja")

def render_data_to_latex(data):
	"""
	Converts a dictionary of resume data to a LaTeX string using a Jinja2 template.

	Parameters:
	- data: Dictionary containing resume data.

	Returns:
	- LaTeX string.
	"""

	# Escape special characters, see latex_escape for more about what is escaped
	data = escape_dict(data)

	# Render the LaTeX template with data
	latex_string = template.render(
		name=data["name"],
		phone=data["phone"],
		email=data["email"],
		website=data["website"],
		linkedin=data["linkedin"],
		github=data["github"],
		education_list=data["education_list"],
		skills=data["skills"],
		experience_list=data["experience_list"],
		project_list=data["project_list"],
		awards_list=data["awards_list"]
	)

	return latex_string

def read_yaml_and_write_latex(yaml_file, output_file):
	"""
	Reads YAML data from a file, generates LaTeX string, and writes it to an output file.

	Parameters:
	- yaml_file: Path to the YAML file containing resume data.
	- output_file: Path to save the generated LaTeX file.
	"""
	# Load the YAML data
	with open(yaml_file, "r") as file:
		data = yaml.safe_load(file)


	# Generate LaTeX string from dictionary
	latex_string = render_data_to_latex(data)

	# Save the rendered LaTeX to a file
	with open(output_file, "w") as file:
		file.write(latex_string)

	return os.path.abspath(output_file)

# Example usage
# read_yaml_and_write_latex("data.yaml", "resume.tex")

# Max size all uppercase with dot at end: 69
# Max size all lowercase with dot at end: 103

def latex_escape(text):
	"""
	Escapes special characters for LaTeX.

	Parameters:
	- text: The string to escape.

	Returns:
	- Escaped string.
	"""
	if not isinstance(text, str):
		return text

	replacements = {
		"&": r"\&",
		"%": r"\%",
		"#": r"\#",
	}
	for key, value in replacements.items():
		text = text.replace(key, value)
	return text

def escape_dict(data):
	"""
	Recursively applies the latex_escape function to all string values in a dictionary.
	
	Parameters:
	- data: The dictionary or list to process.

	Returns:
	- A new dictionary or list with all strings escaped.
	"""
	if isinstance(data, dict):
		return {key: escape_dict(value) for key, value in data.items()}
	elif isinstance(data, list):
		return [escape_dict(item) for item in data]
	elif isinstance(data, str):
		return latex_escape(data)
	else:
		return data
