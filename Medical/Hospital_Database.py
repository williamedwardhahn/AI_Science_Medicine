from microdot import Microdot, Response
import pandas as pd
import os

app = Microdot()
Response.default_content_type = 'text/html'

CSV_FILE = 'patient_records.csv'

# Initialize the DataFrame
if not os.path.exists(CSV_FILE):
    patient_df = pd.DataFrame(columns=['patient_id', 'name', 'age', 'doctor', 'admission_date', 'diagnosis'])
    patient_df.to_csv(CSV_FILE, index=False)
else:
    patient_df = pd.read_csv(CSV_FILE)

def load_data_from_csv():
    global patient_df
    patient_df = pd.read_csv(CSV_FILE)

def save_data_to_csv():
    patient_df.to_csv(CSV_FILE, index=False)

def htmldoc():
    load_data_from_csv()
    html = '''
        <html>
            <head>
                <title>Hospital Patient Records Management</title>
            </head>
            <body>
                <h1>Hospital Patient Records Management</h1>
                <form method="post" action="/">
                    <label for="patient_id">Patient ID:</label><br>
                    <input type="text" id="patient_id" name="patient_id" required><br>
                    <label for="name">Patient Name:</label><br>
                    <input type="text" id="name" name="name" required><br>
                    <label for="age">Age:</label><br>
                    <input type="text" id="age" name="age" required><br>
                    <label for="doctor">Doctor:</label><br>
                    <input type="text" id="doctor" name="doctor" required><br>
                    <label for="admission_date">Admission Date:</label><br>
                    <input type="text" id="admission_date" name="admission_date" required><br>
                    <label for="diagnosis">Diagnosis:</label><br>
                    <input type="text" id="diagnosis" name="diagnosis" required><br>
                    <input type="submit" value="Submit">
                </form>
                <h2>Current Records:</h2>
    '''
    for _, row in patient_df.iterrows():
        html += f'''
        <div>
            Patient ID: {row['patient_id']}<br>
            Name: {row['name']}<br>
            Age: {row['age']}<br>
            Doctor: {row['doctor']}<br>
            Admission Date: {row['admission_date']}<br>
            Diagnosis: {row['diagnosis']}<br>
            <form method="POST" action="/remove/{row['patient_id']}">
                <input type="submit" value="Remove">
            </form>
            <hr>
        </div>
        '''
    html += '</body></html>'
    return html

@app.route('/', methods=['GET', 'POST'])
def home(request):
    if request.method == 'POST':
        patient_df.loc[len(patient_df)] = [
            request.form.get('patient_id'),
            request.form.get('name'),
            request.form.get('age'),
            request.form.get('doctor'),
            request.form.get('admission_date'),
            request.form.get('diagnosis'),
        ]
        save_data_to_csv()

    return htmldoc()

@app.route('/remove/<patient_id>', methods=['POST'])
def remove(request, patient_id):
    global patient_df
    patient_df = patient_df[patient_df.patient_id != int(patient_id)]  # Convert patient_id to int for comparison
    save_data_to_csv()
    return htmldoc()

app.run(debug=True, port=8008)
