from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from recsapp.forms import LogForm, filterForm

import sqlite3
import json
import pandas as pd
import subprocess
from django.conf import settings
import os

# Create your views here.
def home(request):
    return render(request, '_index.html')

def about(request):
    return render(request, 'about.html')

def results(request):
    return render(request, 'results.html')

def inputForm(request):
    form = LogForm()
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'form.html', context)

#
##
### User-Generated Data
USERDATA = os.path.join(settings.MEDIA_ROOT, 'recommendations.json')
shared_data = {}
###
##
#

def submitFilter(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    table_name = 'recsapp_logger'
    json_file_path = USERDATA

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = f'SELECT id, skills, workexp FROM {table_name} ORDER BY id DESC LIMIT 1'

        cursor.execute(query)
        row = cursor.fetchone()

        if row:
            data = {"id": row[0], "skills":row[1], "experience":row[2]}
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            
        else:
            return JsonResponse({"status": "error", "message": "No data found in the database"}, status=404)
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    finally:
        if conn:
            conn.close()
        
        form = filterForm()

        if request.method == 'GET' and 'country' in request.GET and 'salary' in request.GET:
            form =filterForm(request.GET)

            if form.is_valid():
                shared_data['filter_data'] = form.cleaned_data
        
        else:
            form = filterForm(initial=shared_data.get('filtered_data', {}))

        context = {"filter": form}

        return render(request, 'fullfilter.html', context)
    

# script_path = os.path.join(settings.BASE_DIR, 'the_script')


RUNSKILLS = os.path.join(settings.BASE_DIR, 'model/bash', 'run_skills.sh')
RUNWORKEXP = os.path.join(settings.BASE_DIR, 'model/bash', 'run_workex.sh')


def processing(request):
    try:
        subprocess.run([RUNSKILLS, USERDATA], check=True)
    except subprocess.CalledProcessError as e:
            return JsonResponse({"status": "error", "message": f"Script execution failed: {e}"}, status=500)
    
    try:
        subprocess.run([RUNWORKEXP, USERDATA], check=True)
    except subprocess.CalledProcessError as e:
            return JsonResponse({"status": "error", "message": f"Script execution failed: {e}"}, status=500)
    
    return render(request, 'processing.html')


SKILLRECS = os.path.join(settings.BASE_DIR, 'model/responses/skills', 'recommendations.json')
XPRECS = os.path.join(settings.BASE_DIR, 'model/responses/workEx', 'recommendations.json')

DATAPATH = os.path.join(settings.BASE_DIR, 'model/data', 'dataset_first_50k.csv')

print(XPRECS)
print(SKILLRECS)


def post_processing(request):
    # Load JSON files
    with open(SKILLRECS, 'r') as file:
        skill_recs = json.load(file)

    with open(XPRECS, 'r') as file:
        xp_recs = json.load(file)

    # Convert JSON to DataFrames
    skill_df = pd.DataFrame(skill_recs)
    xp_df = pd.DataFrame(xp_recs)

    # Combine DataFrames
    combined_df = pd.concat([skill_df, xp_df], ignore_index=True)

    # Explode 'Recommended Job IDs' to flatten the lists
    if 'Recommended Job IDs' in combined_df.columns:
        combined_df = combined_df.explode('Recommended Job IDs')
        combined_df['Recommended Job IDs'] = combined_df['Recommended Job IDs'].astype(int)

        # Combine rows with the same index into one entry
        grouped_df = combined_df.groupby('Applicant ID').agg({
            'Recommended Job IDs': list
        }).reset_index()

        # Extract unique job IDs
        all_ids = grouped_df['Recommended Job IDs'].explode().unique()

        # Load the reference dataset
        reference_df = pd.read_csv(DATAPATH)

        # Filter the reference dataset by the job IDs
        filtered_df = reference_df[reference_df['Job Id'].isin(all_ids)]
    else:
        filtered_df = pd.DataFrame()

    # Save filtered data to shared_data for use in `another_function`
    shared_data['initial_filtered_data'] = filtered_df

    # Proceed to further filtering in another_function
    return filter_results(request)


def filter_results(request):
    # Get filtered data from post_processing
    filtered_df = shared_data.get('initial_filtered_data', pd.DataFrame())

    # Get additional filters from `shared_data['filter_data']`
    filter_data = shared_data.get('filter_data', {})

    # Apply filters if available
    if not filtered_df.empty and filter_data:
        # Example filters from `filter_data`: 'country', 'salary'
        country_filter = filter_data.get('country', '').lower()
        salary_filter = filter_data.get('salary', None)

        if country_filter:
            filtered_df = filtered_df[filtered_df['Country'].str.lower().str.contains(country_filter)]
        if salary_filter:
            filtered_df = filtered_df[filtered_df['Salary'] >= int(salary_filter)]

    # Convert the final DataFrame to context
    context = {"dataframe": filtered_df.to_dict('records')}

    # Render the results page
    return render(request, 'results.html', context)









# try:
#     subprocess.run([script_path, json_file_path], check=True)
#     return JsonResponse({"status": "success", "message": "Script executed Successfully", "data": data})
# except subprocess.CalledProcessError as e: 
#         return JsonResponse({"status": "error", "message": f"Script execution failed: {e}"}, status=500)