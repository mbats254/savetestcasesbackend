# products/views.py

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TestCase
from .serializers import TestCaseSerializer
import json
import os
from django.http import JsonResponse
from django.conf import settings
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse

# List and Create View for TestCase
class TestCaseListView(APIView):
    """
    Retrieve a list of all test cases or create a new test case.
    """
    def get(self, request, format=None):
        test_cases = TestCase.objects.all()
        serializer = TestCaseSerializer(test_cases, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TestCaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Detail, Update, and Delete View for a single TestCase
class TestCaseDetailView(APIView):
    """
    Retrieve, update, or delete a specific test case.
    """
    def get(self, request, pk, format=None):
        test_case = get_object_or_404(TestCase, pk=pk)
        serializer = TestCaseSerializer(test_case)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        test_case = get_object_or_404(TestCase, pk=pk)
        serializer = TestCaseSerializer(test_case, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        test_case = get_object_or_404(TestCase, pk=pk)
        test_case.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def load_all_test_cases(request):
    # Path to the JSON file
    json_file_path = os.path.join(settings.BASE_DIR, "data/data_with_ids.json")

    try:
        # Open and load the JSON data
        with open(json_file_path, "r") as file:
            test_cases = json.load(file)
        
        # Return data as JSON response
        return JsonResponse(test_cases, safe=False, status=200)

    except FileNotFoundError:
        return JsonResponse({"error": "File not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error decoding JSON data"}, status=500)    
    


def download_testcases_excel(request):
    # Create a new Excel workbook and a worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "TestCases"

    # Define the headers based on TestCase model fields
    headers = ["ID", "Test Case", "Pre-condition", "Test Steps", "Test Data", "Expected Result", "Pass/Fail"]
    for col_num, header in enumerate(headers, 1):
        sheet[f"{get_column_letter(col_num)}1"] = header

    # Retrieve all records from the TestCase model
    test_cases = TestCase.objects.all()

    # Populate the Excel sheet with data from the TestCase model
    for row_num, test_case in enumerate(test_cases, start=2):
        sheet[f"A{row_num}"] = test_case.test_case_id
        sheet[f"B{row_num}"] = test_case.test_case
        sheet[f"C{row_num}"] = test_case.pre_condition
        sheet[f"D{row_num}"] = test_case.test_steps
        sheet[f"E{row_num}"] = test_case.test_data
        sheet[f"F{row_num}"] = test_case.expected_result
        sheet[f"G{row_num}"] = test_case.pass_fail

    # Set the response with the correct content type and filename for download
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="test_cases.xlsx"'

    # Save the workbook to the response
    workbook.save(response)
    return response    

    
