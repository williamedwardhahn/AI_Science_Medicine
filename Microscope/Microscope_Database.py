from microdot import Microdot, Response
import pandas as pd
import os

app = Microdot()
Response.default_content_type = 'text/html'

CSV_FILE = 'microscope_data.csv'

# Initialize the DataFrame
if not os.path.exists(CSV_FILE):
    microscope_df = pd.DataFrame(columns=['image_id', 'magnification', 'researcher', 'date', 'description'])
    microscope_df.to_csv(CSV_FILE, index=False)
else:
    microscope_df = pd.read_csv(CSV_FILE)

def load_data_from_csv():
    global microscope_df
    microscope_df = pd.read_csv(CSV_FILE)

def save_data_to_csv():
    microscope_df.to_csv(CSV_FILE, index=False)

def htmldoc():
    load_data_from_csv()
    html = '''
        <html>
            <head>
                <title>Microscope Dataset Management</title>
            </head>
            <body>
                <h1>Microscope Dataset Management</h1>
                <form method="post" action="/">
                    <label for="image_id">Image ID:</label><br>
                    <input type="text" id="image_id" name="image_id" required><br>
                    <label for="magnification">Magnification:</label><br>
                    <input type="text" id="magnification" name="magnification" required><br>
                    <label for="researcher">Researcher:</label><br>
                    <input type="text" id="researcher" name="researcher" required><br>
                    <label for="date">Date:</label><br>
                    <input type="text" id="date" name="date" required><br>
                    <label for="description">Description:</label><br>
                    <input type="text" id="description" name="description" required><br>
                    <input type="submit" value="Submit">
                </form>
                <h2>Current Records:</h2>
    '''
    for _, row in microscope_df.iterrows():
        html += f'''
        <div>
            Image ID: {row['image_id']}<br>
            Magnification: {row['magnification']}<br>
            Researcher: {row['researcher']}<br>
            Date: {row['date']}<br>
            Description: {row['description']}<br>
            <form method="POST" action="/remove/{row['image_id']}">
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
        microscope_df.loc[len(microscope_df)] = [
            request.form.get('image_id'),
            request.form.get('magnification'),
            request.form.get('researcher'),
            request.form.get('date'),
            request.form.get('description'),
        ]
        save_data_to_csv()

    return htmldoc()

@app.route('/remove/<image_id>', methods=['POST'])
def remove(request, image_id):
    global microscope_df
    microscope_df = microscope_df[microscope_df.image_id != int(image_id)]  # Convert image_id to int for comparison
    save_data_to_csv()
    return htmldoc()


app.run(debug=True, port=8008)
