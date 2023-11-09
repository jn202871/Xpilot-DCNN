import libpyAI as ai
import math


FEELER_DIRS = []
FEELER_DIRS.append(0)
FEELER_DIRS.append(15)
FEELER_DIRS.append(-15)
FEELER_DIRS.append(30)
FEELER_DIRS.append(-30)
FEELER_DIRS.append(45)
FEELER_DIRS.append(-45)
FEELER_DIRS.append(60)
FEELER_DIRS.append(-60)
FEELER_DIRS.append(75)
FEELER_DIRS.append(-75)
FEELER_DIRS.append(90)
FEELER_DIRS.append(-90)


def open_wall(xdir, dist):
    if(xdir == -1 or dist == -1):
        return ai.selfTrackingDeg() + 180
    else:
        max = -1
        for i in range(12):
            w = ai.wallFeeler(dist, xdir+FEELER_DIRS[i])
            if w == dist:
                return i
            elif w > max:
                max = i
        return i
        

def AI_loop():

    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeedDeg(20)

    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    enemy = ai.closestShipId()
    renemy_x = ai.closestRadarX()
    renemy_y = ai.closestRadarY()
    radar_angle = int(math.degrees(math.atan(abs(renemy_y)/abs(renemy_x + 0.00000001))))
    heading_to_enemy = heading - ai.aimdir(0)
    heading_to_dodge = heading - ai.shotVelDir(0)

    # Wall Feelers
    wall_feeler0 = ai.wallFeeler(500, tracking)
    wall_feeler1 = ai.wallFeeler(500, tracking + 15)
    wall_feeler2 = ai.wallFeeler(500, tracking - 15)
    wall_feeler3 = ai.wallFeeler(500, tracking + 30)
    wall_feeler4 = ai.wallFeeler(500, tracking - 30)
    wall_feeler5 = ai.wallFeeler(500, tracking + 45)
    wall_feeler6 = ai.wallFeeler(500, tracking - 45)
    wall_feeler7 = ai.wallFeeler(500, tracking + 60)
    wall_feeler8 = ai.wallFeeler(500, tracking - 60)
    wall_feeler9 = ai.wallFeeler(500, tracking + 75)
    wall_feeler10 = ai.wallFeeler(500, tracking - 75)
    wall_feeler11 = ai.wallFeeler(500, tracking + 90)
    wall_feeler12 = ai.wallFeeler(500, tracking - 90)
    
    renemy_x = renemy_x - ai.selfRadarX()
    renemy_y = renemy_y - ai.selfRadarY()

    if renemy_x < 0 and renemy_y > 0:
        radar_angle = 180 - radar_angle
    elif renemy_x < 0 and renemy_y < 0:
        radar_angle = 180 + radar_angle
    elif renemy_x > 0 and renemy_y < 0:
        radar_angle = 360 - radar_angle


    print("open_wall: ",open_wall(tracking, 100))

    print("wall_feeler 1: ",wall_feeler1)
    print("wall_feeler 2: ",wall_feeler2)
    print("shot alert: ", ai.shotAlert(0))
    print("enemy id: ", enemy)
    print("aimdir: ", ai.aimdir(0))
    print("heading to enemy: ", heading_to_enemy)
    print("heading to dodge: ", heading_to_dodge)
    print("renemy_x: ", renemy_x)
    print("renemy_y: ", renemy_y)
    print("radar angle: ", radar_angle)
    print("-------")

    # Dodge shots
    if(ai.shotAlert(0) > -1 and ai.shotAlert(0) < 80):
        print("Dodging")
        ai.turn(heading_to_dodge)
        ai.thrust(1)

    # Shoot nearest enemy
    elif(ai.closestShipId() > -1 and abs(heading_to_enemy < 400)):
        print("Shooting")
        if(heading_to_enemy > 0):
            ai.turnRight(1)
        else:
            ai.turnLeft(1)
        ai.fireShot()

    # Point at closest enemy on radar and chase
    elif(ai.closestRadarX() > -1 and abs(radar_angle < 600)):
        ai.turnToDeg(radar_angle)
        if (ai.selfSpeed() < 10):
            ai.thrust(1)

    # Wall avoidance
    if((wall_feeler1 == wall_feeler2) and (wall_feeler1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(heading - (180 + tracking))
#        if(ai.selfSpeed() < 10):
        ai.thrust(1)
        print("Turning 1: ",heading - (180 + tracking))
    elif((wall_feeler1 < wall_feeler2) and (wall_feeler1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(heading - (180 - 15 + tracking))
        ai.turn(15)
 #       if(ai.selfSpeed() < 10):
        ai.thrust(1)
        print("Turning 2: ",heading - (180 - 15 +tracking))
    elif((wall_feeler1 > wall_feeler2) and (wall_feeler1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(heading - (180 + 15 + tracking))
        ai.turn(-15)
  #      if(ai.selfSpeed() < 10):
        ai.thrust(1)
        print("Turning 3: ",heading - (180 + 15 + tracking))

    #if(ai.selfSpeed() < 5):
    #    ai.thrust(1)

ai.start(AI_loop, ["-name", "Morton", "-join", "localhost"])