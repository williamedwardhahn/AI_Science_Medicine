import base64
import io
from io import BytesIO
import numpy as np
from microdot_asyncio import Microdot, Response
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
async def landing(request):
    # Build the HTML
    page_content = f"""
	<html>
	<body>
	<h1>Welcome to our Matplotlib Showcase!</h1>
	<a href="/scatter/10">Scatter Plot</a> <br><br>
	<a href="/line/10">Line Plot</a></li>  <br><br>
	<a href="/histogram/10">Histogram</a>  <br><br>
	<a href="/bar/10">Bar Plot</a> <br>
	</body>
	</html>
    """
    return page_content


def get_svg(fig):
    img = io.StringIO()
    fig.savefig(img, format='svg')
    return '<svg' + img.getvalue().split('<svg')[1]
    
    


@app.route('/scatter')
@app.route('/scatter/')
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
    ax.grid(True)

    return get_svg(fig)

    

@app.route('/line')
@app.route('/line/')
@app.route('/line/<points>')
async def line(request, points = "10"):
    points = int(points)
    x = np.linspace(0, 10, points)
    y = x ** 2

    fig = Figure()
    FigureCanvas(fig)

    ax = fig.add_subplot(111)
    ax.plot(x, y,'.')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'{points} Points Line Plot!')
    ax.grid(True)

    
    return get_svg(fig)
    

@app.route('/histogram')    
@app.route('/histogram/')
@app.route('/histogram/<points>')
async def histogram(request, points = "10"):
    points = int(points)
    data = np.random.randn(points)

    fig = Figure()
    FigureCanvas(fig)

    ax = fig.add_subplot(111)
    ax.hist(data, bins=20)

    ax.set_xlabel('Bins')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{points} Points Histogram!')
    ax.grid(True)
    
    return get_svg(fig)
    

@app.route('/bar')    
@app.route('/bar/')
@app.route('/bar/<points>')
async def bar(request, points = "10"):
    points = int(points)
    x = np.arange(points)
    y = np.random.rand(points)

    fig = Figure()
    FigureCanvas(fig)

    ax = fig.add_subplot(111)
    ax.bar(x, y)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'{points} Bars Bar Plot!')
    ax.grid(True)

    return get_svg(fig)
    
    
app.run(host="0.0.0.0",port=8008,debug = True)
