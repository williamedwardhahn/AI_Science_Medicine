

def perform_heimlich(request):
    return "Perform the Heimlich maneuver.<br>Call for medical help if necessary."

def perform_CPR(request):
    return "Begin chest compressions and rescue breaths if trained to do so.<br>Call for medical help if necessary."

def perform_FAST(request):
    return "Remember the FAST method - Face, Arms, Speech, Time.<br>If any of these signs are positive, call for medical help immediately."


rules = {
    "Choking": {
        "question": "Is the person able to speak or cough? (Yes/No)",
        "actions": {
            "Yes": "Encourage them to keep coughing to try and dislodge the object.<br>Call for medical help if necessary.",
            "No": perform_heimlich
        }
    },
    "Bleeding": {
        "question": "Is the bleeding severe? (Yes/No)",
        "actions": {
            "Yes": "Apply direct pressure to the wound.<br>Elevate the injured area above the heart if possible.<br>Call for medical help if necessary.",
            "No": "Clean the wound with soap and water.<br>Apply an antibiotic ointment and a sterile bandage."
        }
    },
    "Burns": {
        "question": "What is the severity of the burn? (First-degree/Second-degree/Third-degree)",
        "actions": {
            "First-degree": "Cool the burn with cool (not cold) water for several minutes.<br>Apply an antibiotic ointment and a sterile bandage.",
            "Second-degree": "Cool the burn with cool (not cold) water for several minutes.<br>Cover the burn with a sterile bandage or clean cloth.<br>Call for medical help if necessary.",
            "Third-degree": {
                "question": "Are there any additional injuries? (Yes/No)",
                "actions": {
                    "Yes": "Call for medical help immediately.<br>Cover the burn with a sterile bandage or clean cloth.<br>Do not apply any ointments or creams to the burn.",
                    "No": "Call for medical help immediately.<br>Cover the burn with a sterile bandage or clean cloth.<br>Do not apply any ointments or creams to the burn."
                }
            }
        }
    },
    "Cardiac arrest": {
        "question": "Has the person lost consciousness and not breathing? (Yes/No)",
        "actions": {
            "Yes": perform_CPR,
            "No": "Monitor the person and keep them calm.<br>Call for medical help if necessary."
        }
    },
    "Stroke": {
        "question": "Does the person show signs of stroke, like facial drooping, arm weakness or speech difficulties? (Yes/No)",
        "actions": {
            "Yes": perform_FAST,
            "No": "Monitor the person and keep them calm.<br>Call for medical help if necessary."
        }
    },
    "Fracture": {
        "question": "Is the fracture open or closed? (Open/Closed)",
        "actions": {
            "Open": "Do not attempt to realign the bone or push a bone that's sticking out back in.<br>Call for medical help immediately.",
            "Closed": "Immobilize the injured area if possible.<br>Apply ice to limit swelling and help relieve pain until medical help arrives."
        }
    }
}


from microdot import Microdot, Response
import urllib.parse

app = Microdot()
Response.default_content_type = 'text/html'

user_state = {}

def prompt_user(request, question, actions):
    buttons = ''.join(f'<a href="/handle_question/{urllib.parse.quote(choice)}"><button>{choice}</button></a><br>'
                      for choice in actions.keys())
    user_state['current_actions'] = actions  # Store the current state
    return f'{question}<br>{buttons}'

def handle_actions(request, actions):
    if callable(actions):
        return actions(request)
    elif isinstance(actions, str):
        return actions
    elif isinstance(actions, dict):
        if "question" in actions and "actions" in actions:
            return prompt_user(request, actions['question'], actions['actions'])
        else:
            return handle_actions(request, actions['actions'])

def handle_question(request, question):
    question = urllib.parse.unquote(question)
    actions = user_state['current_actions'].get(question)  # Get the actions for the current question
    if actions:
        return handle_actions(request, actions)
    else:
        keys = list(rules.keys())
        return f"Invalid question: {question}. Valid questions: {keys}"

@app.route('/')
def start(request):
    return prompt_user(request, "What is the nature of the emergency? (Choking/Bleeding/Burns/Cardiac arrest/Stroke/Fracture)", rules)

@app.route('/handle_question/<question>', methods=['GET', 'POST'])
def handle_question_request(request, question):
    return handle_question(request, question)



app.run(debug=True, port=8008)
