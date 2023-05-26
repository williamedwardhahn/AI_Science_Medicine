def heimlich_maneuver(request):
    return "Perform the Heimlich maneuver.<br>Call for medical help if necessary."

def cpr_procedure(request):
    return "Begin chest compressions and rescue breaths if trained to do so.<br>Call for medical help if necessary."

def stroke_procedure(request):
    return "Remember the FAST method - Face, Arms, Speech, Time.<br>If any of these signs are positive, call for medical help immediately."

emergency_procedures = {
    "Choking": {
        "question": "Is the person able to speak or cough? (Yes/No)",
        "responses": {
            "Yes": "Encourage them to keep coughing to try and dislodge the object.<br>Call for medical help if necessary.",
            "No": heimlich_maneuver
        }
    },
    "Bleeding": {
        "question": "Is the bleeding severe? (Yes/No)",
        "responses": {
            "Yes": "Apply direct pressure to the wound.<br>Elevate the injured area above the heart if possible.<br>Call for medical help if necessary.",
            "No": "Clean the wound with soap and water.<br>Apply an antibiotic ointment and a sterile bandage."
        }
    },
    "Burns": {
        "question": "What is the severity of the burn? (First-degree/Second-degree/Third-degree)",
        "responses": {
            "First-degree": "Cool the burn with cool (not cold) water for several minutes.<br>Apply an antibiotic ointment and a sterile bandage.",
            "Second-degree": "Cool the burn with cool (not cold) water for several minutes.<br>Cover the burn with a sterile bandage or clean cloth.<br>Call for medical help if necessary.",
            "Third-degree": {
                "question": "Are there any additional injuries? (Yes/No)",
                "responses": {
                    "Yes": "Call for medical help immediately.<br>Cover the burn with a sterile bandage or clean cloth.<br>Do not apply any ointments or creams to the burn.",
                    "No": "Call for medical help immediately.<br>Cover the burn with a sterile bandage or clean cloth.<br>Do not apply any ointments or creams to the burn."
                }
            }
        }
    },
    "Cardiac arrest": {
        "question": "Has the person lost consciousness and not breathing? (Yes/No)",
        "responses": {
            "Yes": cpr_procedure,
            "No": "Monitor the person and keep them calm.<br>Call for medical help if necessary."
        }
    },
    "Stroke": {
        "question": "Does the person show signs of stroke, like facial drooping, arm weakness or speech difficulties? (Yes/No)",
        "responses": {
            "Yes": stroke_procedure,
            "No": "Monitor the person and keep them calm.<br>Call for medical help if necessary."
        }
    },
    "Fracture": {
        "question": "Is the fracture open or closed? (Open/Closed)",
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

def present_options(request, question, responses):
    options_html = ''.join(
        f'<a href="/handle_response/{urllib.parse.quote(option)}"><button>{option}</button></a><br>' for option in responses.keys())
    current_state['current_responses'] = responses  # Store the current state
    return f'{question}<br>{options_html}'

def process_response(request, responses):
    if callable(responses):
        return responses(request)
    elif isinstance(responses, str):
        return responses
    elif isinstance(responses, dict):
        if "question" in responses and "responses" in responses:
            return present_options(request, responses['question'], responses['responses'])
        else:
            return process_response(request, responses['responses'])

def handle_response(request, response):
    response = urllib.parse.unquote(response)
    next_step = current_state['current_responses'].get(response)  # Get the actions for the current response
    if next_step:
        return process_response(request, next_step)
    

@app.route('/')
def begin_procedure(request):
    current_state = {}
    return present_options(request, "What is the nature of the emergency? (Choking/Bleeding/Burns/Cardiac arrest/Stroke/Fracture)", emergency_procedures)

@app.route('/handle_response/<response>', methods=['GET', 'POST'])
def handle_response_request(request, response):
    return handle_response(request, response)

app.run(debug=True, port=8008)
