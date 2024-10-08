import pandas as pd
from pyxdameraulevenshtein import damerau_levenshtein_distance
import regex as re

def string_cleaning(string):
    clean_string = re.sub(r"\n", "", string)
    clean_string = re.sub(r"nan", "", clean_string)
    clean_string = re.sub(r" ", "", clean_string)
    clean_string = re.sub(r"\r", "", clean_string)
    clean_string = clean_string.lower()
    clean_string = re.sub(r'[^a-zA-zäöüÄÖÜß]', '', clean_string)
    return clean_string

def score_response_damerau(response, length_group):
    if length_group == "short_word" and response <= 1:
        return 1
    elif length_group == "short_word" and response > 1:
        return 0
    elif length_group == "long_word" and response <= 2:
        return 1
    elif length_group == "long_word" and response > 2:
        return 0
    else:
        return "error"

def score_response_leveinshtein(response):
    if response > 90:
        return 1
    else:
        return 0

def clean_df(df):

    # Create a copy of the DataFrame slice
    df_short = df[["Word1", "Word2", "Response.text", "length_group_ima"]].copy()

    # Ensure all values are treated as strings, replacing NaNs with empty strings
    df_short["Word2"] = df_short["Word2"].astype(str).fillna("")
    df_short = df_short[df_short["Word2"] != "nan"]
    df_short["Response.text"] = df_short["Response.text"].astype(str).fillna("")

    # remove unwanted characters from result string and make every letter lowercase
    df_short["Response.text"] = df_short["Response.text"].apply(string_cleaning)

    # make every letter lowercase in the solution string
    df_short["Word2"] = df_short["Word2"].str.lower()

    # calculate distance based on Damerau Levenshtein Distance
    df_short["distance_damerau"] = df_short.apply(
        lambda row: damerau_levenshtein_distance(row["Word2"], row["Response.text"]), axis=1)

    df_short["scoring_damerau"] = df_short.apply(
        lambda row: score_response_damerau(row['distance_damerau'], row['length_group_ima']), axis=1)

    result_damerau = df_short["scoring_damerau"].sum()
    result_damerau = int(result_damerau)
    return result_damerau, df_short

# A simple scoring function that reads a CSV and calculates a score
def calculate_score(file_path):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(file_path)

        score = clean_df(df)[0]

        return score
    except Exception as e:
        return f"An error occurred: {str(e)}"

def clean_df_return(path):
    try:
        df = pd.read_csv(path)
        cleaned_df = clean_df(df)[1]
        return cleaned_df
    except Exception as e:
        return f"An error occurred: {str(e)}"

#clean_df_return(path)
#print(f"Result damerau: {result_damerau}")

#df_short[["Word1", "Word2", "Response.text", "distance_damerau", "length_group_ima", "scoring_damerau"]].head(50)