# app.py
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import sys

# Import your module here
sys.path.append("C:/Users/oskar/OneDrive/Dokumenty/")
import planDefiner3000  # Replace with your actual module name

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_file():
    file = request.files.get('file')
    if not file:
        return 'No file uploaded.', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(os.getcwd(), filename)
    file.save(filepath)

    # Call your module function
    planDefiner3000.main(filepath)

    # The directory where the Schedules_ file is being created
    directory = os.path.dirname(filepath)
    # Assuming your program generates a file named "Schedules_" + file_to_read
    generated_file_path = os.path.join(directory, "Schedules_" + filename)
    return send_file(generated_file_path, as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
