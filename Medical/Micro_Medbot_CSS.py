def heimlich_maneuver(request):
    return "Perform the Heimlich maneuver.<br>Call for medical help if necessary."

def cpr_procedure(request):
    return "Begin chest compressions and rescue breaths if trained to do so.<br>Call for medical help if necessary."

def stroke_procedure(request):
    return "Remember the FAST method - Face, Arms, Speech, Time.<br>If any of these signs are positive, call for medical help immediately."

emergency_procedures = {
    "Choking": {
        "question": "Is the person able to speak or cough?",
        "responses": {
            "Yes": "Encourage them to keep coughing to try and dislodge the object.<br>Call for medical help if necessary.",
            "No": heimlich_maneuver
        }
    },
    "Bleeding": {
        "question": "Is the bleeding severe?",
        "responses": {
            "Yes": "Apply direct pressure to the wound.<br>Elevate the injured area above the heart if possible.<br>Call for medical help if necessary.",
            "No": "Clean the wound with soap and water.<br>Apply an antibiotic ointment and a sterile bandage."
        }
    },
    "Burns": {
        "question": "What is the severity of the burn?",
        "responses": {
            "First-degree": "Cool the burn with cool (not cold) water for several minutes.<br>Apply an antibiotic ointment and a sterile bandage.",
            "Second-degree": "Cool the burn with cool (not cold) water for several minutes.<br>Cover the burn with a sterile bandage or clean cloth.<br>Call for medical help if necessary.",
            "Third-degree": {
                "question": "Are there any additional injuries?",
                "responses": {
                    "Yes": "Call for medical help immediately.<br>Cover the burn with a sterile bandage or clean cloth.<br>Do not apply any ointments or creams to the burn.",
                    "No": "Call for medical help immediately.<br>Cover the burn with a sterile bandage or clean cloth.<br>Do not apply any ointments or creams to the burn."
                }
            }
        }
    },
    "Cardiac arrest": {
        "question": "Has the person lost consciousness and not breathing?",
        "responses": {
            "Yes": cpr_procedure,
            "No": "Monitor the person and keep them calm.<br>Call for medical help if necessary."
        }
    },
    "Stroke": {
        "question": "Does the person show signs of stroke, like facial drooping, arm weakness or speech difficulties?",
        "responses": {
            "Yes": stroke_procedure,
            "No": "Monitor the person and keep them calm.<br>Call for medical help if necessary."
        }
    },
    "Fracture": {
        "question": "Is the fracture open or closed?",
        "responses": {
            "Open": "Do not attempt to realign the bone or push a bone that's sticking out back in.<br>Call for medical help immediately.",
            "Closed": "Immobilize the injured area if possible.<br>Apply ice to limit swelling and help relieve pain until medical help arrives."
        }
    }
}

from microdot import Microdot, Response
import urllib.parse

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
    if callable(responses):
        result = responses(request)
    elif isinstance(responses, str):
        result = responses
    elif isinstance(responses, dict):
        if "question" in responses and "responses" in responses:
            result = present_options(request, responses['question'], responses['responses'])
        else:
            result = process_response(request, responses['responses'])
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
