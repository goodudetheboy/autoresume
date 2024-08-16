# autoresume: A Resume Tailor CLI

This CLI application tailors a YAML-formatted resume to a specific job description provided in a TXT file. It processes the input files, customizes the resume content, and renders the output in LaTeX (`.tex`) and/or PDF formats.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Command Structure](#basic-command-structure)
  - [Generating PDF Output](#generating-pdf-output)
  - [Generating LaTeX (.tex) Output](#generating-latex-tex-output)
  - [Generating Both PDF and LaTeX Outputs](#generating-both-pdf-and-latex-outputs)
- [Examples](#examples)
- [Modules Description](#modules-description)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Tailoring**: Customizes your resume based on the job description.
- **Flexible Output**: Generates outputs in LaTeX (`.tex`) and/or PDF formats.
- **Customizable Output Directories**: Specify where to save the generated files.
- **Command-Line Interface**: Easy-to-use CLI with multiple options.

## Prerequisites

- **Python 3.6 or higher**
- **Required Python Packages**:
  - `PyYAML`
- **LaTeX Distribution**: For PDF generation, ensure that a LaTeX distribution (like TeX Live or MiKTeX) is installed and `pdflatex` is available in your system's PATH.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/goodudetheboy/autoresume.git
   cd autoresume
   ```

2. **Install Required Python Packages**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Ensure LaTeX Distribution is Installed**:
   - Install [TeX Live](https://www.tug.org/texlive/) or [MiKTeX](https://miktex.org/), depending on your operating system.

## Usage

### Basic Command Structure

```bash
python cli.py [OPTIONS] RESUME_PATH JOB_DESCRIPTION_PATH
```

- `RESUME_PATH`: Path to your resume YAML file.
- `JOB_DESCRIPTION_PATH`: Path to the job description TXT file.

### Generating PDF Output

To generate a tailored resume in PDF format:

```bash
python cli.py RESUME_PATH JOB_DESCRIPTION_PATH --pdf --output-dir-pdf OUTPUT_PDF_DIRECTORY
```

- `--pdf`: Flag to generate PDF output.
- `--output-dir-pdf`: (Optional) Directory to save the generated PDF. Defaults to the current directory if not specified.

### Generating LaTeX (.tex) Output

To generate a tailored resume in LaTeX (`.tex`) format:

```bash
python cli.py RESUME_PATH JOB_DESCRIPTION_PATH --tex --output-dir-tex OUTPUT_TEX_DIRECTORY
```

- `--tex`: Flag to generate LaTeX (`.tex`) output.
- `--output-dir-tex`: (Optional) Directory to save the generated `.tex` file. Defaults to the current directory if not specified.

### Generating Both PDF and LaTeX Outputs

To generate both PDF and LaTeX outputs simultaneously:

```bash
python cli.py RESUME_PATH JOB_DESCRIPTION_PATH --pdf --output-dir-pdf OUTPUT_PDF_DIRECTORY --tex --output-dir-tex OUTPUT_TEX_DIRECTORY
```

## Examples

1. **Generate Only PDF**:
   ```bash
   python cli.py resume.yaml job_description.txt --pdf --output-dir-pdf ./output/pdf
   ```

2. **Generate Only LaTeX (`.tex`) File**:
   ```bash
   python cli.py resume.yaml job_description.txt --tex --output-dir-tex ./output/tex
   ```

3. **Generate Both PDF and LaTeX Outputs in Default Directory**:
   ```bash
   python cli.py resume.yaml job_description.txt --pdf --tex
   ```

4. **Generate Both PDF and LaTeX Outputs in Specified Directories**:
   ```bash
   python cli.py resume.yaml job_description.txt --pdf --output-dir-pdf ./pdf_output --tex --output-dir-tex ./tex_output
   ```

## Modules Description

- **`cli.py`**: The main CLI application that parses arguments, processes inputs, and coordinates the tailoring and rendering processes.

- **`tailor` Module**:
  - **Function**: Processes the YAML resume and job description to tailor the resume content.
  - **Key Function**: `process_resume(resume_data, job_description)`

- **`render` Module**:
  - **Function**: Handles the rendering of the tailored resume into LaTeX and/or PDF formats.
  - **Key Function**: `render_latex(tailored_resume, generate_pdf=False, output_pdf_path=None, output_tex_path=None)`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit your Changes (`git commit -m 'Add Your Feature'`)
4. Push to the Branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE).

---

*For any questions or issues, please open an issue on the repository or contact the maintainer.*