# Group 5 Project - Job Matching Algorithm

## Business Understanding
### Problem Statement
Matching job seekers with relevant job opportunities is crucial for both candidates and employers. However, traditional keyword-based search systems lack the intelligence to align jobs with an individual's holistic profile—skills, experience, and preferences—leading to inefficiencies.
#### Objective
Develop an intelligent NLP-based job recommendation system that uses the job description dataset to recommend suitable roles for applicants based on:
Their skills, qualifications, and experience. Job descriptions, required skills, and responsibilities.
#### Key Stakeholders
Applicants: Need personalized recommendations to find jobs aligned with their skillset and career goals. Employers: Want efficient shortlisting of relevant candidates. Recruitment Platforms: Seek to enhance user engagement and improve match accuracy.
#### Goals
For Job Seekers: Deliver precise job recommendations tailored to their profiles. Save time by reducing the need for extensive manual searches.
For Employers: Improve applicant-job alignment, reducing hiring timelines.
For the Platform: Enhance user satisfaction and retention through advanced recommendations.

The project aims to analyze job descriptions to identify patterns in required skills, qualifications, and experience across industries and roles. It will map competencies to specific job titles using techniques like skill extraction and clustering. Recommendations will consider various factors, including geographical preferences, salary expectations, and work type, to create a comprehensive match.
To measure success, metrics like recommendation accuracy, user engagement, and system performance will be tracked. The next steps involve exploring the dataset further, defining applicant features, and designing the recommendation model, potentially leveraging collaborative filtering and content-based approaches.
#### System Functionality Overview
The job recommendation system will allow users to input their skills, work experience, job title, employment duration, and job description. Using NLP, the system will analyze this information to extract key skills and industry-specific terms, matching the user's profile against job descriptions in the dataset.
Recommendations will be tailored based on factors like required skills, experience, location, work type, and salary, ensuring a personalized and relevant list of job opportunities. This approach streamlines the job search process, helping users identify roles aligned with their expertise and career goals.

## How to run the algorithm
# How to run the algo

## Step One : Clone the repo.
Follow the necessary steps to clone the repo.

## Step Two: Install all required libraries.
To achieve this, run the following code snippets:

`python3 -m venv .virtualenv`
To setup the virtual environment for the project.
`source .virtualenv/bin/activate`
This step varies depending on your operating system.
`python3 -m pip install -r requirements.txt`
You may need to update your pip.

## Step Three: Initialize the vectorizers as follows
`./bash/save_skills.sh ['path-to-the-csv-data-file]`
Then:
`./bash/save_workex.sh ['path-to-the-csv-data-file]`

## Step Four: Run the algorithm to produce recommendations
`./bash/run_skills.sh ['path-to-input-json-file(queries/skills)']`
And:
`./bash/run_workex.sh ['path-to-input-json-file(queries/workEx)']`

Congratulations! More Coming soon...