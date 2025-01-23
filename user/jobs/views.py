from django.shortcuts import render, redirect
from django.http import JsonResponse
import json


def send_to_recommendation_system(job_data):
    """
    Mock function to send job data to a recommendation system and get a response.
    Replace this with actual API integration when available.
    """
    # Mock response data
    mock_response = {
        'status_code': 200,
        'json': lambda: {
            "101": {
                "Experience": "5+ years",
                "Qualifications": "Bachelor's in Computer Science",
                "Salary_Range": "$80,000 - $100,000",
                "location": "New York",
                "Country": "USA",
                "latitude": "40.7128",
                "longitude": "-74.0060",
                "Work_Type": "Full-time",
                "Company_Size": "100-500",
                "Job_Posting_Date": "2025-01-01",
                "Preference": "Immediate Joining",
                "Contact_Person": "John Doe",
                "Contact": "john.doe@example.com",
                "Job_Title": "Senior Software Engineer",
                "Role": "Development",
                "Job_Portal": "LinkedIn",
                "Job_Description": "Develop and maintain software applications.",
                "Benefits": "Health Insurance, 401(k)",
                "skills": "Python, Django, SQL",
                "Responsibilities": "Code, review, debug.",
                "Company": "TechCorp",
                "Company_Profile": "A leading tech solutions provider."
            },
            # Additional job entries here
        }
    }
    return mock_response


def home(request):
    """
    Handles form submission and renders the job recommendations page.
    """
    if request.method == "POST":
        # Get job data from the form
        job_data = request.POST.dict()  # Convert POST data to dictionary
        response = send_to_recommendation_system(job_data)

        # Check if the API call was successful
        if response['status_code'] == 200:
            result = response['json']()  # Extract job data
            request.session['result'] = result  # Store result in session
            return redirect("jobs:results")  # Redirect to results page
        else:
            return render(request, "jobs/home.html", {"error": "Error fetching job recommendations."})

    return render(request, "jobs/home.html")


def results(request):
    """
    Displays job recommendations.
    """
    result = request.session.get("result", {})  # Retrieve results from session
    return render(request, "jobs/results_table.html", {"result": result})
