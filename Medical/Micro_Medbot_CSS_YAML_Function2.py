import yaml
import urllib.parse
from microdot import Microdot, Response

# Define procedures as functions
def cpr_procedure():
    return "Perform CPR by giving chest compressions and rescue breaths."

def heimlich_maneuver():
    return "Perform the Heimlich maneuver to clear the airway obstruction."

def stroke_procedure():
    print("terminal message")
    return "Take the person to the hospital immediately for medical treatment."


# Define the nested dictionary
emergency_procedures = '''
Bleeding:
  question: Is the bleeding severe?
  responses:
    'No': Clean the wound with soap and water. Apply an antibiotic ointment and a
      sterile bandage.
    'Yes': Apply direct pressure to the wound. Elevate the injured area above the
      heart if possible. Call for medical help if necessary.
Burns:
  question: What is the severity of the burn?
  responses:
    First-degree: Cool the burn with cool (not cold) water for several minutes. Apply
      an antibiotic ointment and a sterile bandage.
    Second-degree: Cool the burn with cool (not cold) water for several minutes. Cover
      the burn with a sterile bandage or clean cloth. Call for medical help if necessary.
    Third-degree:
      question: Are there any additional injuries?
      responses:
        'No': Call for medical help immediately. Cover the burn with a sterile bandage
          or clean cloth. Do not apply any ointments or creams to the burn.
        'Yes': Call for medical help immediately. Cover the burn with a sterile bandage
          or clean cloth. Do not apply any ointments or creams to the burn.
Cardiac arrest:
  question: Has the person lost consciousness and not breathing?
  responses:
    'No': Monitor the person and keep them calm. Call for medical help if necessary.
    'Yes': $cpr_procedure
Choking:
  question: Is the person able to speak or cough?
  responses:
    'No': $heimlich_maneuver
    'Yes': Encourage them to keep coughing to try and dislodge the object. Call for
      medical help if necessary.
Fracture:
  question: Is the fracture open or closed?
  responses:
    Closed: Immobilize the injured area if possible. Apply ice to limit swelling and
      help relieve pain until medical help arrives.
    Open: Do not attempt to realign the bone or push a bone that's sticking out back
      in. Call for medical help immediately.
Stroke:
  question: Does the person show signs of stroke, like facial drooping, arm weakness,
    or speech difficulties?
  responses:
    'No': Monitor the person and keep them calm. Call for medical help if necessary.
    'Yes': $stroke_procedure
'''

# Convert YAML to dictionary
emergency_procedures = yaml.safe_load(emergency_procedures)

app = Microdot()
Response.default_content_type = 'text/html'

current_state = {}

css_style = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f0f8ff;
    margin: 0;
    padding: 0;
}

h1 {
    color: #0d6efd;
    text-align: center;
    padding: 20px;
}

a {
    color: #0d6efd;
    text-decoration: none;
}

button {
    display: block;
    width: 200px;
    height: 50px;
    margin: 20px auto;
    background-color: #0d6efd;
    color: white;
    border: none;
    border-radius: 5px;
}

button:hover {
    background-color: #0b5ed7;
}

.response-box {
    width: 60%;
    margin: 20px auto;
    padding: 20px;
    border-radius: 5px;
    background-color: white;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    text-align: center;
    font-size: 20px;
}
</style>
"""

def present_options(request, question, responses):
    options_html = ''.join(
        f'<a href="/handle_response/{urllib.parse.quote(option)}"><button>{option}</button></a>' for option in responses.keys())
    current_state['current_responses'] = responses  # Store the current state
    return f'<h1>{question}</h1><br>{options_html}'

def process_response(request, responses):
    if isinstance(responses, str):
        if responses.startswith('$'):
            func_name = responses[1:]  # Remove the "$" character
            func = globals().get(func_name)
            if func and callable(func):
                result = func()
            else:
                result = f"Function '{func_name}' not found."
        else:
            result = responses
    elif isinstance(responses, dict):
        if "question" in responses and "responses" in responses:
            result = present_options(request, responses['question'], responses['responses'])
        else:
            result = process_response(request, responses['responses'])
    else:
        result = str(responses)
    return f'<div class="response-box">{result}</div>'

@app.route('/')
def begin_procedure(request):
    current_state.clear()
    return css_style + present_options(request, "What is the nature of the emergency?", emergency_procedures)
    
@app.route('/handle_response/<response>', methods=['GET', 'POST'])
def handle_response_request(request, response):
    response = urllib.parse.unquote(response)
    next_step = current_state['current_responses'].get(response)  # Get the actions for the current response
    if next_step:
        return css_style + process_response(request, next_step)

app.run(debug=True, port=8008)
