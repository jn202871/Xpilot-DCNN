#import wandb
import sqlite3
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import sys
import time
from torch.optim.lr_scheduler import ReduceLROnPlateau

firstwidth = 512
secondwidth = 256
class DCNNClassifier(nn.Module):
    def __init__(self):
        super(DCNNClassifier, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=(1,1), padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=(1,1), padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.pool = nn.MaxPool2d((2,2))
        self.fc1 = nn.Linear(8192, firstwidth)
        self.bn3 = nn.BatchNorm1d(firstwidth)
        self.fc2 = nn.Linear(firstwidth, secondwidth)
        self.bn4 = nn.BatchNorm1d(secondwidth)
        #self.fc3 = nn.Linear(secondwidth, secondwidth)
        #self.bn5 = nn.BatchNorm1d(secondwidth)
        #self.lstm = nn.LSTM(secondwidth, 256, num_layers=1, batch_first=True)
        #self.fc_out_lstm = nn.Linear(256, 4)  # Adjust the output size to match your label size
        self.fc_out = nn.Linear(secondwidth, 4)  # Adjust the output size to match your label size
        self.relu = nn.ReLU()
        self.drop = nn.Dropout(0.5)

    def convStep(self, x):
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.pool(self.relu(self.bn2(self.conv2(x))))
        x = torch.flatten(x, 1)
        return x

    def forward(self, x):
        x = self.convStep(x)
        x = self.fc1(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.bn4(x)
        x = self.relu(x)
        x = self.drop(x)
        #x = self.fc3(x)
        #x = self.bn5(x)
        #x = self.relu(x)
        #x = self.drop(x)
        #x = x.unsqueeze(1)
        #x, (hn, cn) = self.lstm(x)
        #x = self.fc_out_lstm(x[:, -1, :])
        x = self.fc_out(x)
        return x

def retrain_dcnn(database_path, model_save_path):
    # Hyperparameters
    alpha = 0.0001
    epochs = 5
    hiddenlayers = 4
    layerwidth = 4096
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #print(f"DCNN USING {device}")

    # Connect to SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT frame, actions FROM frames LIMIT 800000")
    db_data = cursor.fetchall()
    conn.close()

    # Preprocess data
    actions = [[int(number) for number in string[1].split(',')] for string in db_data]
    frames = [[int(number) for number in string[0].split(',')] for string in db_data]

    def convert32x32(frame):
      return [frame[i:i + 32] for i in range(0,1024,32)]

    frames = [convert32x32(frame) for frame in frames]

    actions = torch.tensor(actions, dtype=torch.float32).view(len(actions), -1)
    frames = torch.tensor(frames, dtype=torch.float32).view(-1,1,32,32)

    #print("Data preprocessed")
    #print("Actions Tensor Shape:", actions.shape)
    #print("Frames Tensor Shape:", frames.shape)
	    
    # Create Dataset and Dataloader
    dataset = data.TensorDataset(frames, actions)

    #split_ratio = 0.8
    #split_idx = int(len(dataset) * split_ratio)
    #train_dataset, val_dataset = data.random_split(dataset, [split_idx, len(dataset) - split_idx])

    train_loader = data.DataLoader(dataset, batch_size=64, shuffle=True, pin_memory=True, num_workers=4, drop_last=True)
    #val_loader = data.DataLoader(val_dataset, batch_size=64, shuffle=False, pin_memory=True, num_workers=4, drop_last=True)

    #print("TensorDataset and DataLoaders created")

    # Construct DCNN classifier


    #print("DCNN class constructed")

    # Check GPU availability
    model = DCNNClassifier()
    model.load_state_dict(torch.load(model_save_path, map_location=torch.device(device)))

    model.to(device)

    # Setup Training
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.AdamW(model.parameters(), lr=alpha, weight_decay=1e-5)
    #scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2)

    # Training Loop
    if (len(train_loader) > 0):
        for epoch in range(epochs):
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
            
    torch.save(model.state_dict(), model_save_path)
    
#worker_id=5
#retrain_dcnn(f"/tmp/match_data_{worker_id}.db",f"/tmp/Model_{worker_id}.pt")
