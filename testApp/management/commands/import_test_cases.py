import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from testApp.models import TestCase

class Command(BaseCommand):
    help = "Load test cases from data_with_ids.json into the TestCase model."

    def handle(self, *args, **kwargs):
        # Path to the JSON file
        json_file_path = os.path.join(settings.BASE_DIR, "data/data_with_ids.json")

        try:
            # Open and load JSON data
            with open(json_file_path, "r") as file:
                test_cases_data = json.load(file)
            
            # Loop through each entry and save to the database
            for entry in test_cases_data:
                test_case_id = entry.get("id")
                               
                # Check if a TestCase with this id already exists
                if TestCase.objects.filter(test_case_id=test_case_id).exists():
                    

                    self.stdout.write(f"Skipping TestCase with id {test_case_id} as it already exists.")
                    continue


                TestCase.objects.create(
                    name=entry.get("__EMPTY"),
                    # test_case_id=entry.get("id"),
                    test_case=entry.get("Test Case"),
                    pre_condition=entry.get("Pre-condition"),
                    test_steps=entry.get("Test Steps"),
                    test_data=entry.get("Test Data"),
                    expected_result=entry.get("Expected Result"),
                    actual_result=entry.get("Actual Result"),
                    device=entry.get("Device"),
                    pass_fail=entry.get("Pass/Fail"),
                    bug_status=entry.get("Bug(Status)"),
                )
            self.stdout.write(self.style.SUCCESS("Test cases loaded successfully."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error decoding JSON data"))
