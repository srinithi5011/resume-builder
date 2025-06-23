from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from parsers.extract_data import extract_resume_data

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route: Upload Page (GET)
@app.route('/')
def index():
    return render_template('upload.html')

# Route: Handle Resume Upload (POST)
@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return "No file part", 400
    
    file = request.files['resume']
    if file.filename == '':
        return "No selected file", 400

    # Save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Extract data using AI parser
    extracted_data = extract_resume_data(filepath)

    # Pass extracted data to form.html
    return render_template('form.html', data=extracted_data)

@app.route('/preview')
def preview():
    # Get the data from URL query parameters
    name = request.args.get('name', '')
    email = request.args.get('email', '')
    linkedin = request.args.get('linkedin', '')
    github = request.args.get('github', '')
    summary = request.args.get('summary', '')
    template = request.args.get('template', 'template1')  # default

    return render_template('preview.html', name=name, email=email, linkedin=linkedin, github=github, summary=summary, template=template)



@app.route('/template')
def template_selection():
    # Get data from query params (if passed)
    name = request.args.get('name', '')
    email = request.args.get('email', '')
    linkedin = request.args.get('linkedin', '')
    github = request.args.get('github', '')
    summary = request.args.get('summary', '')

    return render_template('template.html', name=name, email=email, linkedin=linkedin, github=github, summary=summary)

@app.route('/continue-existing', methods=['POST'])
def continue_existing():
    filename = request.form['filename']
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    doc = Document(filepath)

    # Prevent adding duplicate data
    existing_text = "\n".join(p.text.lower() for p in doc.paragraphs)

    def add_if_not_present(label, value):
        if value and value.lower() not in existing_text:
            doc.add_paragraph(f"{label}: {value}")

    add_if_not_present("Name", request.form['name'])
    add_if_not_present("Email", request.form['email'])
    add_if_not_present("LinkedIn", request.form['linkedin'])
    add_if_not_present("GitHub", request.form['github'])
    add_if_not_present("Summary", request.form['summary'])

    output_path = os.path.join(OUTPUT_FOLDER, f'modified_{filename}')
    doc.save(output_path)

    return send_file(output_path, as_attachment=True)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
