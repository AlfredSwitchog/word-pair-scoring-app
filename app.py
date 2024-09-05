from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import os
import utils  # contains all the calculation functions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # For flashing messages
app.config['UPLOAD_FOLDER'] = '/tmp'  # Folder to store uploaded files

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    df_html = None
    error = None

    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check if the file is a CSV
        if file and file.filename.endswith('.csv'):
            # Save the file to the tmp folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Call the calculate_score function with the saved file path
            score = utils.calculate_score(file_path)

            # Call the clean_df_return function to process the file and return a cleaned DataFrame
            df_cleaned = utils.clean_df_return(file_path)

            if isinstance(df_cleaned, pd.DataFrame):
                # Convert the DataFrame to HTML if it's valid
                df_html = df_cleaned.to_html(classes='table table-bordered table-hover', index=False)
            else:
                # If result is an error message (string), assign it to error
                error = df_cleaned

            # Optionally delete the file after processing
            os.remove(file_path)
        else:
            flash('Allowed file type is CSV')

    # Render the index.html template and pass the score, df_html, and error to it
    return render_template('index.html', score=score, df_html=df_html, error=error)


if __name__ == "__main__":
    app.run(debug=True)
