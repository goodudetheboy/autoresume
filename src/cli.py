import argparse
import subprocess
import yaml
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from content.tailor import tailor_resume_by_job_description
from content.render import render_data

def load_yaml_file(yaml_path):
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)

def load_job_description(txt_path):
    with open(txt_path, "r") as file:
        return file.read()

def check_pdflatex_installed():
    try:
        # Attempt to run the 'pdflatex' command with the version flag to check if it's installed
        result = subprocess.run(['pdflatex', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the command was successful (exit code 0)
        return result.returncode == 0
    except FileNotFoundError:
            # This will catch the case where 'pdflatex' is not found in the system PATH
            return False

def main():
    parser = argparse.ArgumentParser(description="Tailor your resume to a job description.")
    parser.add_argument("resume", type=str, help="Path to the resume YAML file.")
    parser.add_argument("job_description", type=str, help="Path to the job description TXT file.")
    parser.add_argument("--resume-name", type=str, default="tailored_resume", help="Name of the output resume")
    parser.add_argument("--pdf", action="store_true", help="Generate the tailored resume as a PDF.")
    parser.add_argument("--tex", action="store_true", help="Generate the tailored resume as a .tex file.")
    parser.add_argument("--output-dir-pdf", type=str, default=".", help="Directory where the PDF should be saved.")
    parser.add_argument("--output-dir-tex", type=str, default=".", help="Directory where the .tex file should be saved.")

    args = parser.parse_args()

    # Load the YAML resume and job description
    resume_data = load_yaml_file(args.resume)
    job_description = load_job_description(args.job_description)

    # Ensure the output directories exist
    if args.pdf:
        if not check_pdflatex_installed():
            print("Unfortunately you can't compile .tex files on this system, please install pdflatex.")
            print("You can instead go to https://overleaf.com to compile the generated LaTeX resume file.")
            args.pdf = False
        else:
            os.makedirs(args.output_dir_pdf, exist_ok=True)
    if args.tex:
        os.makedirs(args.output_dir_tex, exist_ok=True)

    # Process the resume with the tailor module
    analysis = tailor_resume_by_job_description(resume_data, job_description)

    # Print resume in YAML
    print("Here is your resume in YAML")
    print(yaml.safe_dump(analysis["resume"]))

    # Print keywords
    print("Keywords detected in your job description: ")
    for keyword in analysis["keywords"]:
        print(f"\t- {keyword}")
    print()

    try:
        # Handle LaTeX rendering and PDF generation
        render_data(
            analysis["resume"],
            resume_name=args.resume_name,
            output_latex_path=args.output_dir_tex if args.tex else None,
            output_pdf_path=args.output_dir_pdf if args.pdf else None
        )

        
        # Print confirmation
        if args.tex:
            output_latex_path = os.path.join(args.output_dir_tex, f"{args.resume_name}.tex")
            print(f"Your resume has been saved into a LaTeX file at {os.path.abspath(output_latex_path)}")
        if args.pdf:
            output_pdf_path = os.path.join(args.output_dir_pdf, f"{args.resume_name}.pdf")
            print(f"Your resume has been saved into a PDF file at {os.path.abspath(output_pdf_path)}")
    except Exception as e:
        print("There was an error rendering your resume o.o")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
