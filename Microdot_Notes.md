# Connecting Python, HTML, and SVG with Microdot

In this guide, we will explore how to connect Python, HTML, and SVG using Microdot, a lightweight Python web framework. This connection will allow us to serve dynamic web content, including mathematical plots and images, directly from Python.

## Table of Contents

- [Why Python, HTML, and SVG](#why-python-html-and-svg)
- [What is Microdot?](#what-is-microdot)
- [Creating a Simple Microdot Application](#creating-a-simple-microdot-application)
- [Generating Dynamic Plots with Matplotlib](#generating-dynamic-plots-with-matplotlib)
- [Displaying Images from a URL](#displaying-images-from-a-url)

## Why Python, HTML, and SVG

**Python** is a versatile programming language known for its simplicity and readability, which makes it a popular choice for a variety of applications, from data analysis to web development. 

**HTML** (HyperText Markup Language) is the standard language for creating web pages. By generating HTML in Python, we can serve dynamic web content based on data or calculations done on the server-side.

**SVG** (Scalable Vector Graphics) is an XML-based vector image format for two-dimensional graphics. SVG images can scale to any size without losing quality, which makes them ideal for web applications. In the context of a Python application, SVG can be useful for displaying graphical data, like plots or charts, generated using libraries like Matplotlib.

## What is Microdot?

Microdot is a minimalist web framework for Python, inspired by Flask. It is especially useful when you want to create a simple web server without the need for a full-featured framework like Django or Flask. Microdot supports asynchronous processing and is compatible with Python's asyncio library, making it a suitable choice for concurrent tasks.

## Creating a Simple Microdot Application

Let's start with a simple Microdot application. Here is an example of a basic "Hello, World!" application:

```python
from microdot import Microdot, Response

app = Microdot()

@app.route('/')
async def hello(request):
    return Response('Hello, World!')

app.run(port=8000)
```

In this example, we created a route (`/`) that responds to HTTP requests with the text "Hello, World!". 

## Generating Dynamic Plots with Matplotlib

We can take advantage of Python's extensive library ecosystem to serve dynamic content. For example, we can generate different types of plots with Matplotlib based on user input. Here's how you might create a scatter plot for a given number of points:

```python
from microdot_asyncio import Microdot, Response
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/scatter/<points>')
async def scatter(request, points = "10"):
    points = int(points)
    data = np.random.rand(points, 2)

    fig = Figure()
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.scatter(data[:,0], data[:,1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'There are {points} data points!')

    img = io.StringIO()
    fig.savefig(img, format='svg')
    svg = '<svg' + img.getvalue().split('<svg')[1]
    return svg

app.run(host="0.0.0.0",port=8000)
```

In this example, visiting `/scatter/100` will display a scatter plot with 100 randomly generated points.

## Displaying Images from a URL



We can also use Microdot to display images from a URL and provide interactive elements, like a button to toggle the grayscale state of the image:

```python
from microdot import Microdot, Response
from PIL import Image
import urllib.request
import io
import base64

app = Microdot()
Response.default_content_type = 'text/html'

image_url = 'https://example.com/image.jpg'
grayscale_state = False

@app.route('/')
def home(request):
    img_b64 = get_image()
    return f'''
        <html>
            <head><title>Image Dashboard</title></head>
            <body>
                <div>
                    <h1>Image Dashboard</h1>
                    <img src="data:image/jpeg;base64,{img_b64}" alt="Image" />
                    <a href="/toggle"><button>Toggle Grayscale</button></a>
                </div>
            </body>
        </html>'''

@app.route('/toggle')
def toggle_grayscale(request):
    global grayscale_state
    grayscale_state = not grayscale_state
    return home(request)

def get_image():
    global grayscale_state
    with urllib.request.urlopen(image_url) as url:
        f = io.BytesIO(url.read())
    img = Image.open(f)
    if grayscale_state:
        img = img.convert('L')
    b = io.BytesIO()
    img.save(b, 'JPEG')
    img_b64 = base64.b64encode(b.getvalue()).decode()
    return img_b64

app.run(port=8000)
```

In this example, visiting `/` will display the current image, and clicking the "Toggle Grayscale" button will change the image's grayscale state and refresh the page.

By using Python, HTML, and SVG with Microdot, we can quickly create dynamic and interactive web applications with minimal code. 


# A Basic Guide to the Microdot Microframework

Microdot is a lightweight web framework for Python. This guide will help you understand the basic features of Microdot and how to use them, by creating several simple examples.

## 1. Basic Setup

Installation: 

```python
pip install microdot
```

The basic setup for a Microdot application involves importing the necessary libraries and creating an instance of the Microdot application.


```python
from microdot import Microdot, Response

app = Microdot()
```

In this snippet, we imported the `Microdot` and `Response` classes from the `microdot` module and then created an instance of the `Microdot` application.

## 2. Setting a Response Type

You can set the default response content type for your application using `Response.default_content_type`. In most cases, when serving web pages, you would set this to `'text/html'`.

```python
Response.default_content_type = 'text/html'
```

## 3. Creating Routes

Routes in Microdot are created using the `@app.route()` decorator. This maps a URL path to a Python function.

### 3.1. Simple GET Route

The simplest type of route responds to a `GET` request to a specified URL. Here's an example:

```python
@app.route('/')
def home(request):
    return '<h1>Welcome to my Microdot App!</h1>'
```

This function will respond to `GET` requests at the root URL (`/`) with a simple HTML string.

### 3.2. Route with URL Parameters

You can also create routes that accept parameters in the URL. Here's an example:

```python
@app.route('/greet/<name>')
def greet(request, name):
    return f'<h1>Hello, {name}!</h1>'
```

This function will respond to `GET` requests at URLs like `/greet/Jane` with a personalized greeting.

### 3.3. Routes Responding to POST Requests

Routes can also respond to `POST` requests. These routes can access data sent in the body of the request:

```python
@app.route('/submit_form', methods=['POST'])
async def submit_form(request):
    name = request.form.get('name')
    return f'<h1>Form submitted successfully, {name}!</h1>'
```

This route will handle `POST` requests at the `/submit_form` URL and read data from the form sent in the request body.

## 4. Running the Application

After setting up routes, you can run your application using `app.run()`. Here's an example:

```python
app.run(debug=True, port=8008)
```

This starts your application with debug mode enabled, listening on port 8008.


Certainly, here are more examples:

## 5. Route with Multiple Parameters

You can add as many parameters as you want to a route. Here's an example with two parameters:

```python
@app.route('/add/<int:num1>/<int:num2>')
def add(request, num1, num2):
    return f'<h1>The sum is: {num1 + num2}</h1>'
```

This route will add two numbers given in the URL and display the result.

## 6. Route with Optional Parameters

Parameters can be made optional by providing a default value in the function definition:

```python
@app.route('/greet/<name>')
def greet(request, name="stranger"):
    return f'<h1>Hello, {name}!</h1>'
```

This route will display a generic greeting if no name is given.

## 7. Route Responding to Both GET and POST Requests

A single route can respond to multiple types of HTTP requests. It can perform different actions depending on the request type:

```python
@app.route('/submit_form', methods=['GET', 'POST'])
async def submit_form(request):
    if request.method == 'POST':
        name = request.form.get('name')
        return f'<h1>Form submitted successfully, {name}!</h1>'
    else:
        return '''
        <form method="POST" action="/submit_form">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name">
            <input type="submit" value="Submit">
        </form>
        '''
```

This route will display a form if visited with a `GET` request, and handle the form submission if visited with a `POST` request.

## 8. Redirecting

You can use the `redirect()` function to redirect the user to a different route:

```python
from microdot import redirect

@app.route('/old_route')
def old_route(request):
    return redirect('/new_route')

@app.route('/new_route')
def new_route(request):
    return '<h1>This is the new route</h1>'
```

Visiting `/old_route` will redirect the user to `/new_route`.
