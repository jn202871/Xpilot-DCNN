import wandb
import sqlite3
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import sys
import time
import os
import pickle
from torch.optim.lr_scheduler import ReduceLROnPlateau

# Hyperparameters
alpha = 0.0001
epochs = 1000
hiddenlayers = 4
firstwidth = 512
secondwidth = 256
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print("Hyperparameters Created")
print("Using Compute Resource:", device)

# Construct DCNN classifier
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
# Save Trained Model
#wandb.finish()
#print("Trained Model Saved")
