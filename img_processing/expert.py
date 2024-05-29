import libpyAI as ai
import math

def AI_loop():
  area = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
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

  # Ship Heading And Position Tracking
  x_cord = int(ai.selfX() / 35)
  y_cord = 31 - int(ai.selfY() / 35)
  area[y_cord][x_cord] = 3
  aimdir = ai.aimdir(0)
  if (aimdir < 0):
      aimdir = -1
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

    #Release keys
  ai.thrust(0)
  ai.turnLeft(0)
  ai.turnRight(0)
  ai.setPower(25)
  #Set variables
  rTurn = False #Unused
  lTurn = True #Unused
  thrust = 0
  fireShot = 0
  turnLeft = 0
  turnRight = 0
  
  # Wall Feelers
  heading = int(ai.selfHeadingDeg())
  tracking = int(ai.selfTrackingDeg())
  
  frontWall = ai.wallFeeler(1000,heading)
  frontWallL = ai.wallFeeler(1000,heading+10)
  frontWallR = ai.wallFeeler(1000,heading-10)
  
  leftWall = ai.wallFeeler(1000,heading+90)
  leftWallL = ai.wallFeeler(1000,heading+100)
  leftWallR = ai.wallFeeler(1000,heading+80)
  
  rightWall = ai.wallFeeler(1000,heading+270)
  rightWallL = ai.wallFeeler(1000,heading+280)
  rightWallR = ai.wallFeeler(1000,heading+260)
  
  backWall = ai.wallFeeler (1000,heading+180)
  backWallL = ai.wallFeeler(1000,heading+190)
  backWallR = ai.wallFeeler(1000,heading+170)
  
  frontWallT = frontWall+frontWallL+frontWallR
  leftWallT = leftWall+leftWallL+leftWallR
  rightWallT = rightWall+rightWallL+rightWallR
  backWallT = backWall+backWallL+backWallR
  
  trackWall = ai.wallFeeler(1000,tracking)
  trackWallL = ai.wallFeeler(1000,tracking+10)
  trackWallR = ai.wallFeeler(1000,tracking-10)
  
  trackWallT = trackWall+trackWallR+trackWallL
  
  # Small production system for thrust
  if frontWallT > 1500 and ai.selfSpeed() < 10:
    ai.thrust(1)
    thrust = 1
  elif frontWallT > leftWallT and frontWallT > rightWallT and frontWallT > backWallT and ai.selfSpeed() < 10:
    ai.thrust(1)
    thrust = 1
  elif trackWallT < 450 and 270 >= abs(tracking-heading) >= 90:
    ai.thrust(1)
    thrust = 1
  elif backWall < 10:
    ai.thrust(1)
    thrust = 1
  elif ai.selfSpeed() < 1 and frontWallT > 200:
    ai.thrust(1)
    thrust = 1
    
  # Main production system for turning and aiming
  if heading > ai.aimdir(0) and ai.enemyDistance(0) < 300 and trackWall > 100:
    ai.turnRight(1)
    turnRight = 1
  elif heading < ai.aimdir(0) and ai.enemyDistance(0) < 300 and trackWall > 100:
    ai.turnLeft(1)
    turnLeft = 1
  elif leftWallT > rightWallT and trackWallT > 900 and ai.selfSpeed() > 5:
    ai.turnLeft(1)
    turnLeft = 1
  elif leftWallT < rightWallT and trackWallT > 900 and ai.selfSpeed() > 5:
    ai.turnRight(1)
    turnRight = 1
  elif heading > (tracking+180)%360 and trackWallT < 900 and ai.selfSpeed() > 10:
    ai.turnRight(1)
    turnRight = 1
  elif heading < (tracking+180)%360 and trackWallT < 900 and ai.selfSpeed() > 10:
    ai.turnLeft(1)
    turnLeft = 1
  elif leftWallT > rightWallT and trackWallT < 500:
    ai.turnLeft(1)
    turnLeft = 1
  elif rightWallT > leftWallT and trackWallT < 500:
    ai.turnRight(1)
    turnRight = 1
  elif heading > ai.aimdir(0) and frontWallT > 100 and leftWallT > 100 and rightWallT > 100 and backWallT > 100:
    ai.turnRight(1)
    turnRight = 1
  elif heading < ai.aimdir(0) and frontWallT > 100 and leftWallT > 100 and rightWallT > 100 and backWallT > 100:
    ai.turnLeft(1)
    turnLeft = 1
  elif leftWallT > rightWallT:
    ai.turnLeft(1)
    turnLeft = 1
  elif leftWallT > rightWallT:
    ai.turnRight(1)
    turnRight = 1
    
  # Shooting
  if (ai.aimdir(0)+5)%360 >= heading >= (ai.aimdir(0)-5)%360:
    ai.fireShot()
    fireShot = 1
    
  if (ai.selfAlive() == 1):
    frameStr = ','.join(str(item) for innerlist in area for item in innerlist)
    actionStr = str(thrust) + "," + str(fireShot) + "," +str(turnLeft) + "," + str(turnRight)
    file = open("data.txt", "a")
    file.write(frameStr + '\n')
    file.write(actionStr+ '\n')
    file.close()
    
ai.start(AI_loop, ["-name", "ExpertSystem", "-join", "localhost"])
