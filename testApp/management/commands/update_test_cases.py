import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from testApp.models import TestCase

class Command(BaseCommand):
    help = "Update test cases from data_with_ids.json in the TestCase model, excluding 'pass_fail'."

    def handle(self, *args, **kwargs):
        # Path to the JSON file
        json_file_path = os.path.join(settings.BASE_DIR, "data/data_with_ids.json")

        try:
            # Open and load JSON data
            with open(json_file_path, "r") as file:
                test_cases_data = json.load(file)

            # Loop through each entry and update the existing test case
            for entry in test_cases_data:
                test_case_id = entry.get("id")

                # Check if a TestCase with this id exists
                try:
                    test_case = TestCase.objects.get(test_case_id=test_case_id)

                    # Update fields, but do not update 'pass_fail'
                    test_case.name = entry.get("__EMPTY", test_case.name)
                    test_case.test_case = entry.get("Test Case", test_case.test_case)
                    test_case.pre_condition = entry.get("Pre-condition", test_case.pre_condition)
                    test_case.test_steps = entry.get("Test Steps", test_case.test_steps)
                    test_case.test_data = entry.get("Test Data", test_case.test_data)
                    test_case.expected_result = entry.get("Expected Result", test_case.expected_result)
                    test_case.actual_result = entry.get("Actual Result", test_case.actual_result)
                    test_case.device = entry.get("Device", test_case.device)
                    test_case.bug_status = entry.get("Bug(Status)", test_case.bug_status)
                    test_case.category = entry.get("Category", test_case.bug_status)

                    # Save the updated test case
                    test_case.save()

                    self.stdout.write(f"TestCase with id {test_case_id} updated successfully.")

                except TestCase.DoesNotExist:
                    self.stdout.write(f"TestCase with id {test_case_id} not found.")

            self.stdout.write(self.style.SUCCESS("Test cases updated successfully."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error decoding JSON data"))
