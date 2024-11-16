# products/models.py

from django.db import models




class TestCase(models.Model):
    test_case_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    test_case = models.CharField(max_length=255, blank=True, null=True)
    pre_condition = models.TextField(blank=True, null=True)
    test_steps = models.TextField(blank=True, null=True)
    test_data = models.TextField(blank=True, null=True)
    expected_result = models.TextField(blank=True, null=True)
    actual_result = models.TextField(blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    pass_fail = models.CharField(max_length=10, blank=True, null=True)
    bug_status = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Test Case {self.test_case_id} - {self.test_case or 'Unnamed'} - {self.pass_fail}"