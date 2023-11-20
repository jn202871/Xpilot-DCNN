# Jay Nash & Russell Kosovesky & Annika Hoag 2023 COM407
# agent that reads the neural network from the .pt file to control the ship

import libpyAI as ai
import torch

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
  if (enemy != -1):
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
    
    #Loading Model
    model = DCNNClassifier()
    model.load_state_dict(torch.load("model.pt")
    model.eval()
    
    outputs = model(area)
    #End of Loading Model
    
    #Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setPower(25)

ai.start(AI_loop,["-name","dcnn-agent","-join","localhost"])
