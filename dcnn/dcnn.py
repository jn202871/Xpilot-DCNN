import wandb
import sqlite3
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import onnx

# Hyperparameters
alpha = 0.001
epochs = 10
hiddenlayers = 3
diagram = True
'''
# Initialize wandb
wandb.init(
    project="xpilot_dcnn",
    config={
        "leanring rate": alpha,
        "architecture": "DCNN",
        "epochs": epochs,
    }
)
print("Wandb run initialized")

# Connect to SQLite database
conn = sqlite3.connect('xpilot_data.db')
cursor = conn.cursor()
cursor.execute("SELECT winloss, rollout FROM data LIMIT 100000")
db_data = cursor.fetchall()
conn.close()
print("Connected to SQLite database and fetched data")
'''
# Preprocess data, WIP

# Create Dataset and Dataloader, WIP

# Construct DCNN classifier
class DCNNClassifier(nn.Module):
    def __init__(self):
        super(DCNNClassifier, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128,64)
        self.fc2 = nn.Linear(64,32)
        self.fc3 = nn.Linear(32,1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.conv1(x)
        x = torch.relu(x)
        # x.view?
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        x = torch.squeeze(x)
        return x

print("DCNN classifier constructed")

# Check GPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Using Compute Resource:", device)


# Move model to device
inputs = torch.randn(32,1,128,128)
model = DCNNClassifier().to(device)
'''
# Setup Training
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=alpha)

# Training Loop
for epoch in range(epochs):
    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    losses = []
    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            losses.append(loss.item())

    avg_loss = sum(losses) / len(losses)
    wandb.log({"epoch": epoch, "loss": avg_loss})
'''

# Produce Architecture Diagram
if(diagram):
	torch.onnx.export(model, inputs, 'dcnn.onnx', input_names=["playdata"], output_names=["fitness"])
