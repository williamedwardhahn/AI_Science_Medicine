from PIL import Image
import requests
from io import BytesIO
import numpy as np
import cv2
import base64
import matplotlib.pyplot as plt
from microdot import Microdot, Response

app = Microdot()
Response.default_content_type = 'text/html'

#url = 'https://i.pinimg.com/736x/20/37/3f/20373fb4dd2e6e969d978ab4d34ac9c9.jpg'
url = 'https://media.geeksforgeeks.org/wp-content/uploads/20230329095332/RGB-arrays-combined-to-make-image.jpg'
response = requests.get(url)
img = Image.open(BytesIO(response.content))
gray_img = img.convert('L')

def get_image_as_base64(image):
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')

def get_image_channel(img, channel_idx):
    img_np = np.array(img)
    if img_np.ndim == 3:
        channel = img_np[:, :, channel_idx]
    else:
        channel = img_np
    channel_img = Image.fromarray(channel.astype(np.uint8))
    return get_image_as_base64(channel_img)



def get_histogram_image(image):
    fig, axs = plt.subplots(1, 1,
                            figsize =(10, 7), 
                            tight_layout = True)
    
    img_arr = np.array(image)
    axs.hist(img_arr.ravel(), bins = 256, color = '#0504aa', alpha = 0.7)
    axs.grid(axis = 'y', alpha = 0.75)
    axs.set_xlabel('Value')
    axs.set_ylabel('Frequency')
    axs.set_title('Pixel Intensity Histogram')

    plt_byte_arr = BytesIO()
    plt.savefig(plt_byte_arr, format='PNG')
    plt_byte_arr = plt_byte_arr.getvalue()
    return base64.b64encode(plt_byte_arr).decode('utf-8')

def get_canny_image(image):
    image = np.array(image)
    edges = cv2.Canny(image, threshold1=30, threshold2=100)
    canny_img = Image.fromarray(edges)
    return get_image_as_base64(canny_img)

def htmldoc():
    global img
    global gray_img
    original_b64 = get_image_as_base64(img)
    red_b64 = get_image_channel(img, 0)
    green_b64 = get_image_channel(img, 1)
    blue_b64 = get_image_channel(img, 2)
    alpha_b64 = get_image_channel(img, 3) if len(np.array(img).shape) == 3 and np.array(img).shape[2] == 4 else None
    hist_b64 = get_histogram_image(img)
    canny_b64 = get_canny_image(img)
    
    return f'''
        <html>
            <head>
                <title>Image Dashboard</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                    }}
                    .container {{
                        display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        grid-gap: 10px;
                        margin: 0 auto;
                        max-width: 1200px;
                        padding: 20px;
                    }}
                    .grid-item {{
                        box-shadow: 0px 1px 3px 0px rgba(0, 0, 0, 0.2), 
                                    0px 1px 1px 0px rgba(0, 0, 0, 0.14), 
                                    0px 2px 1px -1px rgba(0, 0, 0, 0.12);
                        padding: 20px;
                    }}
                    .grid-item h2 {{
                        margin-top: 0;
                    }}
                    img {{
                        max-width: 100%;
                        height: auto;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="grid-item">
                        <h2>Original Image</h2>
                        <img src="data:image/png;base64,{original_b64}" alt="Original Image" />
                        <button onclick="location.href='/toggle'" type="button">Toggle Grayscale</button>
                    </div>
                    <div class="grid-item">
                        <h2>Red Channel</h2>
                        <img src="data:image/png;base64,{red_b64}" alt="Red Channel Image" />
                    </div>
                    <div class="grid-item">
                        <h2>Green Channel</h2>
                        <img src="data:image/png;base64,{green_b64}" alt="Green Channel Image" />
                    </div>
                    <div class="grid-item">
                        <h2>Blue Channel</h2>
                        <img src="data:image/png;base64,{blue_b64}" alt="Blue Channel Image" />
                    </div>
                    {f'<div class="grid-item"><h2>Alpha Channel</h2><img src="data:image/png;base64,{alpha_b64}" alt="Alpha Channel Image" /></div>' if alpha_b64 else ''}
                    <div class="grid-item">
                        <h2>Histogram</h2>
                        <img src="data:image/png;base64,{hist_b64}" alt="Histogram Image" />
                    </div>
                    <div class="grid-item">
                        <h2>Canny Edge</h2>
                        <img src="data:image/png;base64,{canny_b64}" alt="Canny Edge Image" />
                    </div>
                </div>
            </body>
        </html>
    '''



@app.route('/')
def home(req):
    return htmldoc()

@app.route('/toggle')
def toggle_grayscale(req):
    global img
    global gray_img
    img, gray_img = gray_img, img
    return htmldoc()

app.run(debug=True, host="0.0.0.0", port=8008)
