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

Congratulations
