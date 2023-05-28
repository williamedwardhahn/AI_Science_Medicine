import torch
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np
import requests

# Define the transformations: Convert to tensor and normalize
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

# Download and load the test dataset
test_dataset = datasets.MNIST('~/mnist_data/', download=True, train=False, transform=transform)

# Select a test digit
test_digit = test_dataset[1][0].numpy()  # choose the index of the digit you want to test

# Display the selected digit
plt.imshow(test_digit.reshape(28,28), cmap='gray')
plt.show()

# Prepare for the POST request
test_digit = test_digit.reshape(-1).tolist()

# Send the POST request
response = requests.post('http://localhost:8008/predict', json=test_digit)

# Print the predicted digit
print(f'Predicted digit is: {response.json()["digit"]}')
