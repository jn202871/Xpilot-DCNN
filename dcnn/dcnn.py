import wandb
import sqlite3
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import sys
from torchvision.transforms import v2
from PIL import Image

# Hyperparameters
alpha = 0.0001
epochs = 20
hiddenlayers = 3
'''
# Initialize wandb
wandb.init(
    project="xpilot_cloning",
    config={
        "leanring rate": alpha,
        "architecture": "DCNN",
        "batch_size": 1,
        "epochs": epochs,
        "dataset_size": 50000
    }
)
print("Wandb run initialized")
'''
# Connect to SQLite database
conn = sqlite3.connect('xpilot_data.db')
cursor = conn.cursor()
cursor.execute("SELECT frame, actions FROM frames LIMIT 50000")
db_data = cursor.fetchall()
conn.close()
print("Connected to SQLite database and fetched data")

# Preprocess data
actions = [[int(number) for number in string[1].split(',')] for string in db_data]
frames = [[int(number) for number in string[0].split(',')] for string in db_data]

def convert32x32(frame):
  return [frame[i:i + 32] for i in range(0,1024,32)]

frames = [convert32x32(frame) for frame in frames]

actions = torch.tensor(actions, dtype=torch.float32).view(len(actions), -1)
frames = torch.tensor(frames, dtype=torch.float32).view(-1,1,32,32)

print("Data preprocessed")
	
# Create Dataset and Dataloader
dataset = data.TensorDataset(frames, actions)

split_ratio = 0.8
split_idx = int(len(dataset) * split_ratio)
train_dataset, val_dataset = data.random_split(dataset, [split_idx, len(dataset) - split_idx])

train_loader = data.DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = data.DataLoader(val_dataset, batch_size=64, shuffle=False)

# Construct DCNN classifier
class DCNNClassifier(nn.Module):
    def __init__(self):
        super(DCNNClassifier, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128*32*32,256)
        self.fc2 = nn.Linear(256,256)
        self.fc3 = nn.Linear(256,256)
        self.fc4 = nn.Linear(256,4)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.conv1(x)
        x = torch.relu(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        x = torch.relu(x)
        x = self.fc4(x)
        #x = self.sigmoid(x)
        #x = torch.squeeze(x)
        return x

print("DCNN classifier constructed")

# Check GPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#device = torch.device('cpu')
print("Using Compute Resource:", device)


# Move model to device
model = DCNNClassifier().to(device)

# Setup Training
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=alpha)

# Training Loop
for epoch in range(epochs):
    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # Forward pass
        outputs = model(inputs)
        #outputs = outputs.unsqueeze(0)
        loss = criterion(outputs, targets)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    val_losses = []
    with torch.no_grad():
        for inputs, targets in val_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            val_outputs = model(inputs)
            #val_outputs = val_outputs.unsqueeze(0)
            val_loss = criterion(val_outputs, targets)
            val_losses.append(val_loss.item())
    avg_val_loss = sum(val_losses) / len(val_losses)
    print(f"Epoch {epoch+1}/{epochs}, Training Loss: {loss.item()}, Validation Loss: {avg_val_loss}")

    #wandb.log({"train_loss": loss.item(), "val_loss": avg_val_loss,"epoch": epoch})

# Save Trained Model
torch.save(model.state_dict(), "model.pt")
#wandb.finish()
print("Trained Model Saved")
