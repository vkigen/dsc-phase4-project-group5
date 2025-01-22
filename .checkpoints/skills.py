import sys
import pandas as pd
import nltk
import sklearn
import json
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.spatial.distance import cdist
import csv


## initializing lemmatizer
lemmatizer = WordNetLemmatizer()

## preprocessing

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(lemmatized)

def mappingfunction(dataframe, column, function):
    dataframe[f'cleaned_{column}'] = dataframe[f'{column}'].apply(function)
    return dataframe

input_vector = []
reference_vector = []

def VectorProcessing(input_dataframe, column_x, reference_dataframe, column_y):
    all_text = pd.concat([input_dataframe[f'{column_x}'], reference_dataframe[f'{column_y}']])
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(all_text)

    input_vector.clear()
    reference_vector.clear()

    input_vector.append(tfidf_matrix[:len(input_dataframe)])
    reference_vector.append(tfidf_matrix[len(input_dataframe):])
    return


def hammingdistances(vector1, vector2):
    distances = cdist(vector1.toarray(),vector2.toarray(),metric='cityblock')
    return distances

def get_top_recommendations(input_dataframe, index,  reference_dataframe, ref_id, distances, num_recommendations=5):
    recommendations = {}

    for i, applicant_id in enumerate(input_dataframe[f'{index}']):
        top_job_indices = np.argsort(distances[i])[:num_recommendations]
        top_job_ids = reference_dataframe[f'{ref_id}'].iloc[top_job_indices].values
        recommendations[applicant_id] = top_job_ids

    return recommendations

def create_recommendations_dataframe(recommendations):
    recommendations_list = [
        {'Applicant ID': applicant_id, 'Recommended Job IDs': list(recommended_jobs)}
        for applicant_id, recommended_jobs in recommendations.items()
    ]
    return pd.DataFrame(recommendations_list)

def filter_jobs_for_applicant(data_df, recommendations_df, applicant_id):
    recommended_jobs = recommendations_df.loc[recommendations_df['Applicant ID'] == applicant_id, 'Recommended Job IDs']
    if not recommended_jobs.empty:
        job_ids = recommended_jobs.iloc[0]
        return data_df[data_df['Job Id'].isin(job_ids)]
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no recommendations found


applicants = [
    {"id": 1, "experience": "Data Scientist with 5 years experience in python, machine learning and NLP"},
    {"id": 2, "experience": "Software engineer skilled in Java, web development, and cloud infrastructure"}
]

def processPipeline(datapath, inputpath, index, input_column, ref_id, data_field, num_recs):
    
    with open(datapath) as datafile:
        data = pd.read_csv(datafile, on_bad_lines='skip')

    input = pd.DataFrame(inputpath)

    input_df = mappingfunction(input, f'{input_column}', preprocess_text)

    reference_df = mappingfunction(data, f'{data_field}', preprocess_text)

    vectors = VectorProcessing(input_df, f'cleaned_{input_column}', reference_df, f'cleaned_{data_field}')

    hammings = hammingdistances(input_vector[0], reference_vector[0])

    toprecs = get_top_recommendations(input_df, index, reference_df, ref_id, hammings, num_recs)

    recs_df = create_recommendations_dataframe(toprecs)

    return recs_df

def main(args):
    resultsdf = processPipeline(args[0], args[1] == applicants, args[2], args[3], args[4], args[5], args[6])
    return resultsdf

if __name__ == "__main__":
    main(sys.argv)
