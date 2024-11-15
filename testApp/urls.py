# products/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('testcases/', TestCaseListView.as_view(), name='testcase-list'),       # URL for listing and creating test cases
    path('testcases/<int:pk>/', TestCaseDetailView.as_view(), name='testcase-detail'),  # URL for retrieving, updating, and deleting a specific test case
     path('download-testcases/', download_testcases_excel, name='download_testcases_excel'),
     path('download-testcases-json/', download_testcases_json, name='download_testcases_json'),
]
