# Define the expert system rules
def perform_heimlich():
    print("Perform the Heimlich maneuver.\nCall for medical help if necessary.")

rules = {
    "emergency": ["What is the nature of the emergency? (Choking/Bleeding/Burns)",
                  {"Choking": ["Is the person able to speak or cough? (Yes/No)",
                               {"Yes": "Encourage them to keep coughing to try and dislodge the object.\nCall for medical help if necessary.",
                                "No": perform_heimlich}],
                   "Bleeding": ["Is the bleeding severe? (Yes/No)",
                                {"Yes": "Apply direct pressure to the wound.\nElevate the injured area above the heart if possible.\nCall for medical help if necessary.",
                                 "No": "Clean the wound with soap and water.\nApply an antibiotic ointment and a sterile bandage."}],
                   "Burns": ["What is the severity of the burn? (First-degree/Second-degree/Third-degree)",
                             {"First-degree": "Cool the burn with cool (not cold) water for several minutes.\nApply an antibiotic ointment and a sterile bandage.",
                              "Second-degree": "Cool the burn with cool (not cold) water for several minutes.\nCover the burn with a sterile bandage or clean cloth.\nCall for medical help if necessary.",
                              "Third-degree": ["Are there any additional injuries? (Yes/No)",
                                               {"Yes": "Call for medical help immediately.\nCover the burn with a sterile bandage or clean cloth.\nDo not apply any ointments or creams to the burn.",
                                                "No": "Call for medical help immediately.\nCover the burn with a sterile bandage or clean cloth.\nDo not apply any ointments or creams to the burn."}]}]}]
}

# Define a function to prompt the user for input and return their response
def prompt_user(question):
    print(question)
    return input().capitalize()

# Define a recursive function to handle nested questions
def handle_question(question, actions):
    response = prompt_user(question)

    # Ensure the user provides a valid response
    while response not in actions:
        print("I'm sorry, I didn't understand your response. Please try again.")
        response = prompt_user(question)

    action = actions[response]

    if isinstance(action, str):
        print(action)
    elif callable(action):
        action()  # Call the Python function
    else:
        # If the action contains another question, call handle_question recursively
        nested_question, nested_actions = action
        handle_question(nested_question, nested_actions)

# Define a function to run the expert system
def run_expert_system():
    # Start the expert system with the top-level question and actions
    question, actions = rules["emergency"]

    # Call the handle_question function to handle the question and any nested questions
    handle_question(question, actions)

# Call the run_expert_system function to start the expert system
run_expert_system()
