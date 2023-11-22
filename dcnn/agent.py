# Jay Nash & Russell Kosovsky & Annika Hoag 2023 COM407
# agent that reads the neural network from the .pt file to control the ship

import numpy as np
import libpyAI as ai
import torch.nn as nn
import torch

outputs = 0

def AI_loop():

    #Get Frame
    area = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
  

    headingArr = [
    ["a","b","c","d","e","f","g","h","i","j","k","l"],
    ["A","B","C","D","E","F","G","H","I","J","K","L"]
    ]
    enemyHeadingArr = [
    ["o","p","q","r","s","t","u","v","w","x","y","z"],
    ["O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    ]
  
    # Ship Heading And Position Tracking
    x_cord = int(ai.selfX() / 35)
    y_cord = 31 - int(ai.selfY() / 35)
    heading = ai.selfHeadingDeg()
    if (heading == 360):
        heading -= 1
    tracking = ai.selfTrackingDeg()
    trackDiff = abs(((tracking-heading+540)%360)-180)
    headingIndex = int(heading/30)
    trackDiffIndex = False
    if (trackDiff > 90):
        trackDiffIndex = True
    headingSerRow = 0
    if (trackDiffIndex == True):
        headingSerRow = 1
    headingSerCol = headingIndex
    shipVal = headingArr[headingSerRow][headingSerCol]
    area[y_cord][x_cord] = 3
    area[y_cord][x_cord+1] = int(ai.selfSpeed())
    area[y_cord][x_cord-1] = int(ai.aimdir(0))
    area[y_cord+1][x_cord] = int(ai.selfHeadingDeg())
    area[y_cord-1][x_cord] = int(ai.selfTrackingDeg())
  
    # Enemy Heading And Position Tracking
    enemy = ai.closestShipId()
    #print("Enemy: ", enemy)
    if (enemy == -1): 
        ex_cord = int(ai.screenEnemyX(0) / 35)
        ey_cord = 31 - int(ai.screenEnemyY(0) / 35)
        heading = ai.enemyHeadingDeg(0)
        if (heading == 360):
            heading -= 1
        tracking = ai.selfTrackingDeg()
        trackDiff = abs(((tracking-heading+540)%360)-180)
        headingIndex = int(heading/30)
        trackDiffIndex = False
        if (trackDiff > 90):
            trackDiffIndex = True
        headingSerRow = 0
        if (trackDiffIndex == True):
            headingSerRow = 1
        headingSerCol = headingIndex
        enemyVal = enemyHeadingArr[headingSerRow][headingSerCol]
        area[ey_cord][ex_cord] = 4
        area[ey_cord][ex_cord+1] = int(ai.enemySpeed(0))
        area[y_cord+1][x_cord] = int(ai.enemyHeadingDeg(0))
        area[y_cord-1][x_cord] = int(ai.enemyTrackingDeg(0))
  
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
      
        #End of Get Frame
    
        
        # Construct DCNN classifier
        class DCNNClassifier(nn.Module):
            def __init__(self):
                super(DCNNClassifier, self).__init__()
                self.conv1 = nn.Conv2d(in_channels=1, out_channels=128, kernel_size=3, padding=1)
                self.fc1 = nn.Linear(128*32*32,64)
                self.fc2 = nn.Linear(64,64)
                self.fc3 = nn.Linear(64,32)
                self.fc4 = nn.Linear(32,4)
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
    
        #Loading Model
        #print("I'm about to go into DCNNClassifier")
        model = DCNNClassifier()
        model.load_state_dict(torch.load('model.pt', map_location=torch.device('cpu')))
        model.eval()
        #print("I'm out of DCNNClassifier")
        
        area = torch.tensor(area, dtype=torch.float32).view(-1,1,32,32)
        outputs = model(area)
        #End of Loading Model
        
        sigmoid = nn.Sigmoid()
        outputs = sigmoid(outputs)
        
        outputs = outputs.detach().numpy()
        
        #Printing outputs
        print("Outputs: ", outputs)
        #print(outputs[0][0])
        #LEFT OFF: need to take values out of array and put into variabes; thrust, shoot, left, right
        if outputs[0][0]>=0.5:
            #print("test")
            ai.thrust(1)
        
        if outputs[0][1]>=0.5:
            ai.fireShot()
        
        if outputs[0][2]>=0.5:
            ai.turnLeft(1)
        
        if outputs[0][3]>=0.5:
            ai.turnRight(1)
        
        #Release keys
        #ai.thrust(0)
        #ai.turnLeft(0)
        #ai.turnRight(0)
        #ai.setPower(25)
    

ai.start(AI_loop,["-name","dcnn-agent","-join","localhost"])
