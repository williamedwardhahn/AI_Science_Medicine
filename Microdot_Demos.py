######################################################################
#Coin Flip
######################################################################

from microdot_asyncio import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc():
    coin_text = "Heads" if coin_state == 0 else "Tails"

    return f'''
        <html>
            <head>
                <title>Click to Flip Coin</title>
            </head>
            <body>
                <div>
                    <h1>Click the Coin to Flip</h1>
                    <svg width="200" height="200" viewBox="0 0 200 200">
                        <a href="/toggle">
                            <circle style="fill:#F0E68C" cx="100" cy="100" r="90"/>
                            <text x="50%" y="50%" font-size="24" text-anchor="middle" dy=".3em">{coin_text}</text>
                        </a>
                    </svg>
                </div>
            </body>
        </html>
        '''

coin_state = 0

@app.route('/')
def home(request):
    return htmldoc()

@app.route('/toggle')
def toggle_coin(request):
    global coin_state
    coin_state = 1 - coin_state
    return htmldoc()

app.run(debug=True, port=8008)


######################################################################
#Guessing Game
######################################################################

from microdot_asyncio import Microdot, Response
import random

app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc(guesses, message, color):
    return f'''
        <html>
            <head>
                <title>High Low Guessing Game</title>
            </head>
            <body>
                <div>
                    <h1>High Low Guessing Game</h1>
                    <p>{message}</p>
                    <form method="post" action="/">
                        <label for="guess">Guess a number between 1 and 100:</label>
                        <input type="number" name="guess" id="guess" min="1" max="100" required>
                        <button type="submit">Submit</button>
                    </form>
                    <p>Guesses: {guesses}</p>
                    <svg width="100" height="100" viewBox="0 0 512 512">
                        <circle style="fill:#{color}" cx="255.995" cy="255.995" r="200"/>
                    </svg>
                    <form method="post" action="/new_game">
                        <button type="submit">New Game</button>
                    </form>
                </div>
            </body>
        </html>
        '''

random_number = random.randint(1, 100)
guesses = 0

@app.route('/', methods=['GET', 'POST'])
async def home(request):
    global random_number, guesses

    if request.method == 'POST':
        guess = int(request.form.get('guess'))

        if guess < random_number:
            message = 'Too low!'
            color = '853737' # Red
        elif guess > random_number:
            message = 'Too high!'
            color = '907A4A' # Yellow
        else:
            message = 'Correct!'
            color = '4E7039' # Green

        guesses += 1

    else:
        message = 'Guess a number between 1 and 100.'
        color = '515262' # Grey

    return htmldoc(guesses, message, color)

@app.route('/new_game', methods=['POST'])
async def new_game(request):
    global random_number, guesses
    random_number = random.randint(1, 100)
    guesses = 0
    return htmldoc(guesses, 'Guess a number between 1 and 100.', '515262') # Grey

app.run(debug=True, port=8008)



######################################################################
# Dice
######################################################################

from microdot_asyncio import Microdot, Response
import random
app = Microdot()
Response.default_content_type = 'text/html'

def random_color():
    return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def htmldoc(dice_faces, background_colors):
    dice_faces_svg = {
        1: '''
            <circle cx="100" cy="100" r="10" fill="black" />
        ''',
        2: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        3: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="100" cy="100" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        4: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        5: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="100" cy="100" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        6: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="50" cy="100" r="10" fill="black" />
            <circle cx="150" cy="100" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        '''
    }

    dice_svgs = ''
    for i in range(len(dice_faces)):
        x_offset = 220 * i
        dice_svgs += f'''
            <svg x="{x_offset}" width="200" height="200" viewBox="0 0 200 200">
                <rect x="10" y="10" width="180" height="180" rx="20" ry="20" fill="#{background_colors[i]}" />
                {dice_faces_svg[dice_faces[i]]}
            </svg>
        '''

    return f'''
        <html>
            <head>
                <title>SVG Dice Roll</title>
            </head>
            <body>
                <div>
                    <h1>Click the Buttons to Roll Dice</h1>
                    <div>
                        {dice_svgs}
                    </div>
                    <div>
                        <a href="/roll/1"><button>Roll 1 Dice</button></a>
                        <a href="/roll/2"><button>Roll 2 Dice</button></a>
                        <a href="/roll/3"><button>Roll 3 Dice</button></a>
                        <a href="/roll/4"><button>Roll 4 Dice</button></a>
                        <a href="/roll/5"><button>Roll 5 Dice</button></a>
                        <a href="/roll/6"><button>Roll 6 Dice</button></a>
                    </div>
                </div>
            </body>
        </html>
    '''

@app.route('/')
async def home(request):
    return htmldoc([1], ['F0E68C'])

@app.route('/roll/<num_dice>')
async def roll_dice(request, num_dice):
    num_dice = int(num_dice)
    dice_faces = [random.randint(1, 6) for _ in range(num_dice)]
    background_colors = [random_color() for _ in range(num_dice)]
    return htmldoc(dice_faces, background_colors)


app.run(debug=True, port=8008)



######################################################################
# Traffic Light
######################################################################

from microdot_asyncio import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc():

    reds     = ["853737","ff6465"]
    yellows  = ["907A4A","ffd782"]
    greens   = ["4E7039","a5eb78"]

    red     =     reds[lights[0]]
    yellow  =  yellows[lights[1]]
    green   =   greens[lights[2]]

    return f'''
        <html>
            <head>
                <title>Hahn Traffic Light</title>
            </head>
            <body>
                <div>
                    <h1>Hahn's Traffic Light</h1>
                    <svg width="100" height="100" viewBox="0 0 512 512">
                      <path style="fill:#515262" d="M324.683 41.53H187.317c-28.304 0-51.249 22.946-51.249 51.249V460.75c0 28.305 22.946 51.249 51.249 51.249h137.366c28.304 0 51.249-22.946 51.249-51.249V92.779c0-28.303-22.945-51.249-51.249-51.249z"/>
                      <a href="/toggle/0">
                          <circle style="fill:#{red}" cx="255.995" cy="133.818" r="48.281"/>
                      </a>
                      <a href="/toggle/1">
                          <circle style="fill:#{yellow}" cx="255.995" cy="276.765" r="48.281"/>
                      </a>
                      <a href="/toggle/2">
                          <circle style="fill:#{green}" cx="255.995" cy="419.712" r="48.281"/>
                      </a>
                    </svg>
                </div>
            </body>
        </html>
        '''

lights = [0,0,1]

@app.route('/')
def hello(request):
    return htmldoc()


@app.route('/toggle/<light_index>')
def toggle_light(request, light_index):
    light_index = int(light_index)
    lights[light_index] = 1 - lights[light_index]
    return htmldoc()

app.run(debug=True, port=8008)


######################################################################
#Counter
######################################################################

from microdot_asyncio import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc(counter):
    return f'''
        <html>
            <head>
                <title>Counter Demo</title>
            </head>
            <body>
                <div>
                    <h1>Counter: {counter}</h1>
                    <a href="/change/{counter}/1"><button>Increment</button></a>
                    <a href="/change/{counter}/-1"><button>Decrement</button></a>
                </div>
            </body>
        </html>
        '''

@app.route('/')
def home(request):
    return htmldoc(0)

@app.route('/change/<current_counter>/<step>')
def change(request, current_counter, step):
    counter = int(current_counter) + int(step)
    return htmldoc(counter)

app.run(debug=True, port=8008)


import base64
import io
from io import BytesIO
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from microdot_asyncio import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'


@app.route("/")
@app.route("/<points>")
def hello(request,points = "10"):

    points = int(points)

    data = np.random.rand(points, 2)

    fig = Figure()
    FigureCanvas(fig)

    ax = fig.add_subplot(111)

    ax.scatter(data[:,0], data[:,1])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'There are {points} data points!')
    ax.grid(True)

    img = io.StringIO()
    fig.savefig(img, format='svg')
    #clip off the xml headers from the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    
    return svg_img
    
    
app.run(host="0.0.0.0",port=5000,debug = True)












######################################################################
# Pump Button Demo
######################################################################
from microdot_asyncio import Microdot, Response

app = Microdot()
Response.default_content_type = 'text/html'

system_state = {
    'water_pump': False,
    'air_pump': False,
}

def htmldoc(water_pump_status, air_pump_status):
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
                    .on {{
                        background-color: #4CAF50;
                    }}
                    .on:hover {{
                        background-color: #45a049;
                    }}
                    .off {{
                        background-color: #f44336;
                    }}
                    .off:hover {{
                        background-color: #da190b;
                    }}
                </style>
            </head>
            <body>
                <h1>Aquaponics System Control</h1>
                <div class="container">
                    <a href="/toggle/water_pump">
                        <button class="{('on' if water_pump_status == 'ON' else 'off')}" style="width:200px;">
                            Water Pump: {water_pump_status}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/air_pump">
                        <button class="{('on' if air_pump_status == 'ON' else 'off')}" style="width:200px;">
                            Air Pump: {air_pump_status}
                        </button>
                    </a>
                </div>
            </body>
        </html>
    '''

@app.route('/')
def control(request):
    return htmldoc(
        'ON' if system_state['water_pump'] else 'OFF',
        'ON' if system_state['air_pump'] else 'OFF'
    )

@app.route('/toggle/<component>')
def toggle(request, component):
    system_state[component] = not system_state[component]
    return htmldoc(
        'ON' if system_state['water_pump'] else 'OFF',
        'ON' if system_state['air_pump'] else 'OFF'
    )

app.run(debug=True, port=8008)




######################################################################
# List Demo
######################################################################
from microdot_asyncio import Microdot, Response

app = Microdot()
Response.default_content_type = 'text/html'

todos = []

def htmldoc():
    todo_list = ''.join([f'<li>{todo[1]} - <a href="/toggle/{i}">{"Complete" if not todo[0] else "Uncomplete"}</a> - <a href="/delete/{i}">Delete</a></li>' for i, todo in enumerate(todos)])

    return f'''
        <html>
            <head>
                <title>To-Do List</title>
            </head>
            <body>
                <h1>To-Do List</h1>
                <form method="post" action="/add">
                    <label for="task">New Task:</label>
                    <input type="text" id="task" name="task" required>
                    <button type="submit">Add</button>
                </form>
                <ul>
                    {todo_list}
                </ul>
            </body>
        </html>
        '''

@app.route('/', methods=['GET', 'POST'])
async def home(request):
    if request.method == 'POST':
        todos.append([False, request.form.get('task')])
    return htmldoc()

@app.route('/add', methods=['POST'])
async def add(request):
    todos.append([False, request.form.get('task')])
    return htmldoc()

@app.route('/toggle/<index>')
async def toggle(request, index):
    todos[int(index)][0] = not todos[int(index)][0]
    return htmldoc()

@app.route('/delete/<index>')
async def delete(request, index):
    todos.pop(int(index))
    return htmldoc()

app.run(debug=True, port=8008)





######################################################################
# Pump Demo 2
######################################################################


from microdot_asyncio import Microdot, Response
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
