import torch
import torchvision
from torchvision import transforms
from torch import nn, optim
from microdot_asyncio import Microdot, Response
import json
import numpy as np

# Prepare the MNIST dataset
transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,), (0.5,))])
trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

# Define a simple 3-layer neural network
model = nn.Sequential(nn.Linear(784, 128),
                      nn.ReLU(),
                      nn.Linear(128, 64),
                      nn.ReLU(),
                      nn.Linear(64, 10),
                      nn.LogSoftmax(dim=1))

# Define loss function (negative log likelihood loss)
criterion = nn.NLLLoss()

# Define an optimizer (Stochastic Gradient Descent)
optimizer = optim.SGD(model.parameters(), lr=0.003)

# Train the model
epochs = 5
for e in range(epochs):
    running_loss = 0
    print('-')
    for images, labels in trainloader:
        print('.')
        # Flatten MNIST images into a 784 long vector
        images = images.view(images.shape[0], -1)
    
        # Training pass
        optimizer.zero_grad()
        
        output = model(images)
        loss = criterion(output, labels)
        
        # Backward pass
        loss.backward()
        
        # Optimize weights
        optimizer.step()
        
        running_loss += loss.item()

app = Microdot()

# Predict route
@app.route('/predict', methods=['POST'])
async def predict(request):
    global model
    try:
        # Get image data from request body
        img_data = np.array(json.loads(request.body))
        img_data = img_data.reshape(1, -1)

        # Transform the image data into a PyTorch tensor and make a prediction
        img_tensor = torch.Tensor(img_data).float()
        output = model(img_tensor)
        _, predicted = torch.max(output.data, 1)
        
        return {'digit': int(predicted[0])}
    except Exception as e:
        return {'error': str(e)}

app.run(host="0.0.0.0",port=8008,debug = True)
