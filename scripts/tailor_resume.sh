#!/bin/bash

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
    echo "No company name provided."
    exit 1
fi

echo "Tailoring resume for $1"

cd src
python cli.py ../my_resume/resume.yaml ../my_resume/job_description/$1.txt \
  --resume-name $1 \
  --tex --output-dir-tex ../my_resume/output/$1 \
  --pdf --output-dir-pdf ../my_resume/output/$1 \

