from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import subprocess
import uuid
from django.views.decorators.csrf import csrf_exempt


def send_to_recommendation_system(job_data):
    """
    Mock function to send job data to a recommendation system and get a response.
    Needs to be integrated with the process_data function.

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


def process_data(request):
    if request.method == "POST":
        # Step 1: Extract input data from the form
        input_text = request.POST.get("inputText", "")
        filter_criteria = request.POST.get("filter", "")

        # Step 2: Create a JSON file with ID and input text
        unique_id = str(uuid.uuid4())
        input_json_path = f"/tmp/input_{unique_id}.json"
        output_json_path = f"/tmp/output_{unique_id}.json"

        input_data = {
            "id": unique_id,
            "inputText": input_text
        }
        with open(input_json_path, "w") as f:
            json.dump(input_data, f)

        try:
            # Step 3: Call the Python script, passing the input JSON file and output location as arguments
            result = subprocess.run(
                ["python3", "path/to/your_script.py",
                    input_json_path, output_json_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Check for script errors
            if result.returncode != 0:
                return JsonResponse({"error": result.stderr}, status=500)

            # Step 4: Read the generated JSON file
            with open(output_json_path, "r") as f:
                output_data = json.load(f)

            # Step 5: Filter the output data based on user criteria
            # Assuming output_data is a list of dictionaries
            filtered_data = [
                item for item in output_data if filter_criteria.lower() in item.get("field", "").lower()
            ]

            return JsonResponse({"filtered_data": filtered_data})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
