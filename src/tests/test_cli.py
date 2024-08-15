import unittest
import argparse
import tempfile
import os

from unittest.mock import patch, mock_open, Mock
from cli import load_yaml_file, load_job_description, main

class SystemInterfaceTest(unittest.TestCase):
	def setUp(self):
		with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
			temp_file.write("name: Vuong Ho".encode('utf-8'))
			self.temp_resume_yaml = temp_file.name

		with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
			temp_file.write("PayPal - Software Engineering Intern".encode('utf-8'))
			self.temp_job_description = temp_file.name

	def tearDown(self):
		os.remove(self.temp_resume_yaml)
		os.remove(self.temp_job_description)

	@patch("builtins.open", new_callable=mock_open, read_data="name: John Doe")
	def test_load_yaml_file(self, mock_file: Mock):
		yaml_data = load_yaml_file("resume.yaml")
		self.assertEqual(yaml_data["name"], "John Doe")
		mock_file.assert_called_once_with("resume.yaml", "r")
	
	@patch("builtins.open", new_callable=mock_open, read_data="Software Engineer position")
	def test_load_job_description(self, mock_file: Mock):
		job_description = load_job_description("job_description.txt")
		self.assertEqual(job_description, "Software Engineer position")
		mock_file.assert_called_once_with("job_description.txt", "r")
	
	@patch("cli.tailor_resume_by_job_description")
	@patch("cli.os.makedirs")
	@patch("argparse.ArgumentParser.parse_args")
	def test_main_with_pdf(
		self,
		mock_parse_args: Mock,
		mock_makedirs: Mock,
		mock_tailor_resume_by_job_description: Mock
	):
		with tempfile.TemporaryDirectory() as temp_output_dir:
			mock_parse_args.return_value = argparse.Namespace(
				resume=self.temp_resume_yaml,
				job_description=self.temp_job_description,
				pdf=True,
				tex=True,
				output_dir_pdf=temp_output_dir,
				output_dir_tex=temp_output_dir
			)
			
			mock_tailor_resume_by_job_description.return_value = {"name": "Vuong Ho"}

			main()

			mock_tailor_resume_by_job_description.assert_called_once_with({"name": "Vuong Ho"}, "PayPal - Software Engineering Intern")
			self.assertEqual(mock_makedirs.call_count, 2)
