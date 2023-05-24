```markdown
# A Basic Guide to the Microdot Microframework

Microdot is a lightweight web framework for Python. This guide will help you understand the basic features of Microdot and how to use them, by creating several simple examples.

## 1. Basic Setup

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
