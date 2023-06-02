from microdot import Microdot, Response
from random import randint

app = Microdot()
Response.default_content_type = 'text/html'

correct_selections = 0
total_selections = 0

def generate_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g, b

def adjust_color(r, g, b, difficulty):
    adjust = lambda x: max(0, min(x + randint(-difficulty, difficulty), 255))
    return adjust(r), adjust(g), adjust(b)

def htmldoc(colors, different_index, feedback):
    return f'''
        <html>
            <head>
                <title>Tetrachromacy Test</title>
            </head>
            <body>
                <div>
                    <h1>Tetrachromacy Test</h1>
                    <p>{feedback}</p>
                    <p>Your score: {correct_selections}/{total_selections}</p>
                    <svg width="600" height="200" viewBox="0 0 600 200">
                        <a href="/select/0">
                            <rect x="0" y="0" width="200" height="200" style="fill:rgb{colors[0]}" />
                        </a>
                        <a href="/select/1">
                            <rect x="200" y="0" width="200" height="200" style="fill:rgb{colors[1]}" />
                        </a>
                        <a href="/select/2">
                            <rect x="400" y="0" width="200" height="200" style="fill:rgb{colors[2]}" />
                        </a>
                    </svg>
                </div>
            </body>
        </html>
        '''

base_color = generate_color()
colors = [base_color, base_color, base_color]
different_index = randint(0, 2)
colors[different_index] = adjust_color(*base_color, 20)

@app.route('/')
def home(request):
    return htmldoc(colors, different_index, "Click on the square that looks different.")

@app.route('/select/<int:index>')
def select(request, index):
    global colors, different_index, correct_selections, total_selections
    feedback = "Correct!" if index == different_index else "Incorrect!"
    if index == different_index:
        correct_selections += 1
    total_selections += 1
    base_color = generate_color()
    colors = [base_color, base_color, base_color]
    different_index = randint(0, 2)
    difficulty = max(5, 20 - correct_selections//5)  # The test gets harder every 5 points
    colors[different_index] = adjust_color(*base_color, difficulty)
    return htmldoc(colors, different_index, feedback)

app.run(debug=True, port=8008)
