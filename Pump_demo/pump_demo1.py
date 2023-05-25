from microdot import Microdot, Response
import pandas as pd

app = Microdot()
Response.default_content_type = 'text/html'

CSV_FILE = 'state.csv'

# Initialize the DataFrame
system_df = pd.DataFrame([{
    'water_pump': 'OFF',
    'air_pump': 'OFF',
    'light': 'OFF',
    'water_level': '0',
    'temperature': '0',
    'pH_level': '0',
}])

def load_state_from_csv():
    global system_df
    system_df = pd.read_csv(CSV_FILE)


def save_state_to_csv():
    system_df.to_csv(CSV_FILE, index=False)

def htmldoc(water_pump_status, air_pump_status, light_status, water_level, temperature, pH_level):
    return f'''
        <html>
            <head>
                <title>Aquaponics System Control</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                    }}
                    h1 {{
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                    }}
                    .container {{
                        padding: 20px;
                    }}
                    button {{
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 10px 2px;
                        cursor: pointer;
                        border-radius: 4px;
                        width: 200px;
                    }}
                    .ON {{
                        background-color: #4CAF50;
                    }}
                    .ON:hover {{
                        background-color: #45a049;
                    }}
                    .OFF {{
                        background-color: #f44336;
                    }}
                    .OFF:hover {{
                        background-color: #da190b;
                    }}
                    .parameter {{
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <h1>Aquaponics System Control</h1>
                <div class="container">
                    <a href="/toggle/water_pump">
                        <button class="{water_pump_status}">
                            Water Pump: {water_pump_status}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/air_pump">
                        <button class="{air_pump_status}">
                            Air Pump: {air_pump_status}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/light">
                        <button class="{light_status}">
                            Light: {light_status}
                        </button>
                    </a>
                    <br><br>
                    <div class="parameter">System Parameters:</div>
                    <ul>
                        <li>Water Level: {water_level}</li>
                        <li>Temperature: {temperature}</li>
                        <li>pH Level: {pH_level}</li>
                    </ul>
                </div>
            </body>
        </html>
    '''

def generate_html_doc():
    load_state_from_csv()
    data = system_df.iloc[0]
    return htmldoc(
        data['water_pump'],
        data['air_pump'],
        data['light'],
        data['water_level'],
        data['temperature'],
        data['pH_level'],
    )

@app.route('/')
def control(request):
    save_state_to_csv()
    return generate_html_doc()

@app.route('/toggle/<component>')
def toggle(request, component):
        system_df.at[0, component] = 'ON' if system_df.at[0, component] == 'OFF' else 'OFF'
        save_state_to_csv()
        return generate_html_doc()

@app.route('/set_parameter/<parameter>/<value>')
def set_parameter(request, parameter, value):
        system_df.at[0, parameter] = str(value)
        save_state_to_csv()
        return generate_html_doc()


app.run(debug=True, port=8008)
