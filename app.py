import utils
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

# A simple scoring function that reads a CSV and calculates a score
def calculate_score(file_path):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(file_path)

        score = utils.clean_df(df)[0]

        return score
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    df_html = None
    error = None

    if request.method == "POST":
        # Get the file path from the form
        file_path = request.form.get("file_path")

        # Call the calculate_score function with the provided file path
        score = calculate_score(file_path)

        #call the cleaned_df function to calculate the results and return as dataframe
        df_cleaned = utils.clean_df_return(file_path)

        if isinstance(df_cleaned, pd.DataFrame):
            # Convert the DataFrame to HTML if it's valid
            df_html = df_cleaned.to_html(classes='table table-bordered', index=False)
        else:
            # If result is an error message (string), assign it to error
            error = df_cleaned

    # Render the index.html file and pass the score and the DataFrame HTML to it
    return render_template('index.html', score=score, df_html=df_html, error=error)


if __name__ == "__main__":
    app.run(debug=True)

