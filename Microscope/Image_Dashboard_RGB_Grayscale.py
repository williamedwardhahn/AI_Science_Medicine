from microdot import Microdot, Response
from PIL import Image
import urllib.request
import io
import base64

app = Microdot()
Response.default_content_type = 'text/html'

# Initialize the image URL and grayscale state
image_url = 'https://i.pinimg.com/736x/20/37/3f/20373fb4dd2e6e969d978ab4d34ac9c9.jpg'
grayscale_state = False

def get_image():
    global grayscale_state

    # Fetch the image from the URL
    with urllib.request.urlopen(image_url) as url:
        f = io.BytesIO(url.read())

    # Open the image and optionally convert to grayscale
    img = Image.open(f)
    if grayscale_state:
        img = img.convert('L')

    # Convert the image to base64 for HTML display
    b = io.BytesIO()
    img.save(b, 'JPEG')
    img_b64 = base64.b64encode(b.getvalue()).decode()

    return img_b64

def htmldoc():
    img_b64 = get_image()

    return f'''
        <html>
            <head>
                <title>Image Dashboard</title>
            </head>
            <body>
                <div>
                    <h1>Image Dashboard</h1>
                    <img src="data:image/jpeg;base64, {img_b64}" alt="Image" />
                    <br/>
                    <a href="/toggle">
                        <button>Toggle Grayscale</button>
                    </a>
                </div>
            </body>
        </html>
        '''

@app.route('/')
def home(request):
    return htmldoc()

@app.route('/toggle')
def toggle_grayscale(request):
    global grayscale_state
    grayscale_state = not grayscale_state
    return htmldoc()

app.run(debug=True, port=8008)
