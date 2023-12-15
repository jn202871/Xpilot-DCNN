# Jay Nash & Russell Kosovsky & Annika Hoag 2023 COM407
# agent that reads the neural network from the .pt file to control the ship

import numpy as np
import libpyAI as ai
import torch.nn as nn
import torch
import math

outputs = 0

def AI_loop():

    #Get Frame
    
    area = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
    # Ship Heading And Position Tracking
    x_cord = int(ai.selfX() / 35)
    y_cord = 31 - int(ai.selfY() / 35)
    area[y_cord][x_cord] = 3
    aimdir = ai.aimdir(0)
    if (aimdir < 0):
        aimdir = -1
    print(aimdir)
    area[y_cord][x_cord+1] = int(ai.selfSpeed())
    area[y_cord][x_cord-1] = int(aimdir)
    area[y_cord+1][x_cord] = int(ai.selfHeadingDeg())
    area[y_cord-1][x_cord] = int(ai.selfTrackingDeg())
  
    # Enemy Heading And Position Tracking
    enemy = ai.closestShipId()
    if (enemy != -1):
      ex_cord = int(ai.screenEnemyX(0) / 35)
      ey_cord = 31 - int(ai.screenEnemyY(0) / 35)
      area[ey_cord][ex_cord] = 4
      area[ey_cord][ex_cord+1] = int(ai.enemySpeed(0))
      area[ey_cord+1][ex_cord] = int(ai.enemyHeadingDeg(0))
      enemyTracking = ai.enemyTrackingDeg(0)
      if (math.isnan(enemyTracking)):
          enemyTracking = ai.enemyHeadingDeg(0)
      area[ey_cord-1][ex_cord] = int(enemyTracking)
  
    # Bullet Tracking
    bulletIndex = 0
    bullets = []
    while(ai.shotAlert(bulletIndex) != -1):
      bulletX = int(ai.shotX(bulletIndex)/35)
      bulletY = 31 - int(ai.shotY(bulletIndex)/35)
      bulletAlert = int(ai.shotAlert(bulletIndex))
      if (bulletAlert == 30000):
        bulletAlert = 0
      bullets.append([bulletX,bulletY,bulletAlert])
      bulletIndex += 1
    for bullet in bullets:
      area[bullet[1]][bullet[0]] = 5
      area[bullet[1]][bullet[0]+1] = bullet[2]
      
    if (True):
      for row in area:
        for val in row:
          print(val, end="")
        print()
    
    area = torch.tensor(area, dtype=torch.float32).view(-1,1,32,32)
    outputs = model(area)
        #End of Loading Model
    outputs = outputs.detach().numpy()
        
        #Printing outputs
        
    
    print("Outputs: ", outputs)
        #print(outputs[0][0])
        
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    thrust = 0
    left = 0
    right = 0
    shot = 0
        #LEFT OFF: need to take values out of array and put into variabes; thrust, shoot, left, right
    if (outputs[0][0]>=0.8):
        thrust = 1
        ai.thrust(1)
        
    if (outputs[0][1]>=0.8):
        ai.fireShot()
        shot = 1
        
    if (outputs[0][2]>=0.8 and outputs[0][2]>outputs[0][3]):
        left = 1
        ai.turnLeft(1)
        
    if (outputs[0][3]>=0.8 and outputs[0][3]>outputs[0][2]):
        right = 1
        ai.turnRight(1)
    print("Actions: ", thrust, shot, left, right)
    
        #Release keys
        #ai.thrust(0)
        #ai.turnLeft(0)
        #ai.turnRight(0)
        #ai.setPower(25)
    
layerwidth = 4096
class DCNNClassifier(nn.Module):
    def __init__(self):
        super(DCNNClassifier, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=(1,1), padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=(1,1), padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.pool = nn.MaxPool2d((2,2))
        self.fc1 = nn.Linear(8192,layerwidth)
        self.bn3 = nn.BatchNorm1d(layerwidth)
        self.fc2 = nn.Linear(layerwidth,layerwidth)
        self.bn4 = nn.BatchNorm1d(layerwidth)
        self.fc3 = nn.Linear(layerwidth,layerwidth)
        self.bn5 = nn.BatchNorm1d(layerwidth)
        self.fc4 = nn.Linear(layerwidth,4)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.drop = nn.Dropout(0.5)

    def convStep(self, x):
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.pool(self.relu(self.bn2(self.conv2(x))))
        x = torch.flatten(x,1)
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
        x = self.fc3(x)
        x = self.bn5(x)
        x = self.relu(x)
        x = self.drop(x)
        x = self.fc4(x)
        x = self.sigmoid(x)
        return x
model = DCNNClassifier()
model.load_state_dict(torch.load('./dcnn/models/simpleNN32x32v2.pt', map_location=torch.device('cpu')))
model.eval()
ai.start(AI_loop,["-name","dcnn-agent","-join","localhost"])
