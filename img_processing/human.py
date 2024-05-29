import libpyAI as ai
import math
from pynput import keyboard

# Global variables to store the state of key presses
thrust = 0
fireShot = 0
turnLeft = 0
turnRight = 0

# Function to handle key presses
def on_press(key):
    global thrust, fireShot, turnLeft, turnRight
    try:
        if key.char == 'a':
            turnLeft = 1
        elif key.char == 's':
            turnRight = 1
    except AttributeError:
        if key == keyboard.Key.shift:
            thrust = 1
        elif key == keyboard.Key.enter:
            fireShot = 1

# Function to handle key releases
def on_release(key):
    global thrust, fireShot, turnLeft, turnRight
    try:
        if key.char == 'a':
            turnLeft = 0
        elif key.char == 's':
            turnRight = 0
    except AttributeError:
        if key == keyboard.Key.shift:
            thrust = 0
        elif key == keyboard.Key.enter:
            fireShot = 0

# Start the keyboard listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

def AI_loop():
  global thrust, fireShot, turnLeft, turnRight
	
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
  ai.setPower(25)
  #Set variables
  rTurn = False #Unused
  lTurn = True #Unused
  
    
  if (ai.selfAlive() == 1):
    frameStr = ','.join(str(item) for innerlist in area for item in innerlist)
    actionStr = str(thrust) + "," + str(fireShot) + "," +str(turnLeft) + "," + str(turnRight)
    file = open("dataHuman.txt", "a")
    file.write(frameStr + '\n')
    file.write(actionStr+ '\n')
    file.close()
  
ai.start(AI_loop, ["-name", "Human", "-join", "localhost"])
