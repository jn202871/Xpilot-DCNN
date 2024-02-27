import wandb
import sqlite3
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import sys
import time
from torch.optim.lr_scheduler import ReduceLROnPlateau

# Hyperparameters
a=torch.cuda.FloatTensor()
alpha = 0.0001
epochs = 100
hiddenlayers = 4
layerwidth = 1028
'''
# Initialize wandb
wandb.init(
    project="xpilot_cloning",
    config={
    	"architecture": "AALL",
        "leanring rate": alpha,
        "hiddenlayers": hiddenlayers,
        "layerwidth": layerwidth,
        "batch_size": 64,
        "epochs": epochs,
        "dataset_size": 50000
    }
)
print("Wandb run initialized")
'''
# Connect to SQLite database
conn = sqlite3.connect('neural_data.db')
cursor = conn.cursor()
cursor.execute("SELECT frame, actions FROM frames LIMIT 600000")
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

train_loader = data.DataLoader(train_dataset, batch_size=128, shuffle=True, pin_memory=True, num_workers=2)
val_loader = data.DataLoader(val_dataset, batch_size=128, shuffle=False, pin_memory=True, num_workers=2)

print("Tensor Dataset and DataLoaders created")

# Construct DCNN classifier
class DCNNClassifier(nn.Module):
    def __init__(self):
        super(DCNNClassifier, self).__init__()
        
        self.convBase = nn.Sequential(
                nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=(1,1), padding=1),
                nn.BatchNorm2d(16),
                nn.ReLU(),
                nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=(1,1), padding=1),
                nn.BatchNorm2d(32),
                nn.ReLU(),
                nn.MaxPool2d((2,2)))
                
        self.branch1 = nn.Sequential(
                nn.Linear(8192,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,1))
                
        self.branch2 = nn.Sequential(
                nn.Linear(8192,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,1))
        
        self.branch3 = nn.Sequential(
                nn.Linear(8192,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,1))
                
        self.branch4 = nn.Sequential(
                nn.Linear(8192,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,layerwidth),
                nn.BatchNorm1d(layerwidth),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(layerwidth,1))

    def forward(self, x):
        convOutRaw = self.convBase(x)
        convOut = torch.flatten(convOutRaw, 1)
        
        output1 = self.branch1(convOut)
        output2 = self.branch2(convOut)
        output3 = self.branch3(convOut)
        output4 = self.branch4(convOut)
        
        combinedOut = torch.cat((output1,output2,output3,output4), dim=1)
        
        return combinedOut

print("DCNN class constructed")

# Check GPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#device = torch.device('cpu')
print("Using Compute Resource:", device)


# Move model to device
model = DCNNClassifier().to(device)

# Setup Training
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.AdamW(model.parameters(), lr=alpha, weight_decay=1e-5)
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2, verbose=False)
print("Loss function and optimizer initialized")
# Training Loop
for epoch in range(epochs):
    start = time.time()
    model.train()
    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    val_losses = []
    model.eval()
    with torch.no_grad():
        for inputs, targets in val_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            val_outputs = model(inputs)
            val_loss = criterion(val_outputs, targets)
            val_losses.append(val_loss.item())
    avg_val_loss = sum(val_losses) / len(val_losses)
    scheduler.step(avg_val_loss)
    end = time.time()
    if (avg_val_loss <= 0.2):
        path = f"./gdrive/MyDrive/Colab/XP-DCNN/{avg_val_loss}model.pt"
        torch.save(model.state_dict(), path)
    form1, form2, form3 = "{:<05}", "{:e}", "{:02d}"
    print(f"Epoch {form3.format(epoch+1)}/{epochs}: Training Loss: {form1.format(round(loss.item(),3))}, Validation Loss: {form1.format(round(avg_val_loss,3))}, LR: {form2.format(optimizer.param_groups[-1]['lr'])} Time: {form1.format(round(end-start,2))}")
    #wandb.log({"train_loss": loss.item(), "val_loss": avg_val_loss,"epoch": epoch})

# Save Trained Model
#wandb.finish()
print("Trained Model Saved")
