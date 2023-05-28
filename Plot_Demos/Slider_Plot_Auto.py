from microdot_asyncio import Microdot, Response
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Microdot()
Response.default_content_type = 'text/html'

def get_svg(fig):
    img = io.StringIO()
    fig.savefig(img, format='svg')
    return '<svg' + img.getvalue().split('<svg')[1]

@app.route('/', methods=['GET', 'POST'])
async def landing(request):
    # Default points value
    points = "10"

    # If the request is POST, get the number of points from the form data
    if request.method == 'POST':
        points = request.form.get('points')

    # Generate scatter plot
    scatter_plot = scatter(points)

    # Build the HTML
    page_content = f"""
    <html>
    <head>
        <style>
            .slider {{
                width: 100%;
                height: 25px;
                background: #d3d3d3;
                outline: none;
                opacity: 0.7;
                -webkit-transition: .2s;
                transition: opacity .2s;
            }}
            
            .slider:hover {{
                opacity: 1;
            }}
            
            .slider::-webkit-slider-thumb {{
                -webkit-appearance: none;
                appearance: none;
                width: 25px;
                height: 25px;
                background: #4CAF50;
                cursor: pointer;
            }}
            
            .slider::-moz-range-thumb {{
                width: 25px;
                height: 25px;
                background: #4CAF50;
                cursor: pointer;
            }}

            .slider::-moz-range-track {{
                width: 100%;
                height: 8.4px;
                cursor: pointer;
                animate: 0.2s;
                box-shadow: 1px 1px 1px #000, 0 0 1px #0d0d0d;
                background: #3071a9;
                border-radius: 1.3px;
                border: 0.2px solid #010101;
            }}
            
            .slider::-moz-range-progress {{
                background: #4CAF50;
            }}
            
            .slider::-ms-fill-lower {{
                background: #2a6495;
                border: 0.2px solid #010101;
            }}
            
            .slider::-ms-fill-upper {{
                background: #3071a9;
                border: 0.2px solid #010101;
            }}
            
            .slider::-ms-track {{
                background: transparent;
                border-color: transparent;
                color: transparent;
            }}

            .ticks {{
                display: flex;
                justify-content: space-between;
                padding: 0 10px;
            }}

            .ticks p {{
                position: relative;
                display: flex;
                justify-content: center;
                text-align: center;
                width: 1px;
                background: #D3D3D3;
                height: 10px;
                line-height: 40px;
                margin: 0 0 20px 0;
            }}
            
            .plot-box {{
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
                margin-top: 30px;
                padding: 20px;
                background: #fff;
            }}

        </style>
        <script>
            function autoSubmit() {{
                document.getElementById('form').submit();
            }}
        </script>
    </head>
    <body>
    <h1>Welcome to our Matplotlib Showcase!</h1>
    <form id="form" method="post" action="/">
        <label for="points">Number of Points:</label>
        <input type="range" id="points" name="points" min="1" max="100" value="{points}" 
        oninput="this.nextElementSibling.value = this.value" onchange="autoSubmit()" class="slider">
        <output>{points}</output>
        <div class="ticks">
            <p>1</p><p>20</p><p>40</p><p>60</p><p>80</p><p>100</p>
        </div>
    </form>
    <div class="plot-box">
        {scatter_plot}
    </div>
    </body>
    </html>
    """
    return page_content

def scatter(points = "10"):
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

app.run(host="0.0.0.0",port=8008,debug = True)
