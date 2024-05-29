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
    if(dist > 2000):
        dist = 2000
    if(xdir == -1 or dist == -1):
        return ai.angleAdd(int(ai.selfTrackingDeg()),180)
    else:
        max = -1
        for i in range(12):
            w = ai.wallFeeler(dist, xdir+FEELER_DIRS[i])
            if w == dist:
                return i
            elif w > max:
                max = i
        return i
        
def change_tracking(direction):
	change_heading(ai.angleAdd(int(ai.selfTrackingDeg()), ai.angleDiff(direction, int(ai.selfTrackingDeg()))))
	
def change_heading(direction):
	ai.turn(ai.angleDiff(int(ai.selfHeadingDeg()), direction))

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
    heading_to_enemy = ai.angleDiff(heading, ai.aimdir(0))
    heading_to_dodge = ai.angleDiff(heading, ai.angleAdd(ai.shotVelDir(0),180))

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

    # Dodging and Shooting
    if(ai.shotAlert(0) > -1 and ai.shotAlert(0) < 80):
        print("Dodging")
        ai.turnToDeg(heading_to_dodge)
        ai.thrust(1)
        
    elif(ai.wallBetween(ai.selfX(),ai.selfY(),ai.screenEnemyX(0),ai.screenEnemyY(0)) != -1):
    	change_heading(open_wall(radar_angle,ai.enemyDistance(0)))
    	if(ai.selfSpeed() < 6):
    		ai.thrust(1)
    		
    elif(ai.closestShipId() > -1 and abs(ai.angleDiff(heading,ai.aimdir(0))) < 5):
    	change_heading(ai.aimdir(0))
    	ai.fireShot()
    	
    elif(ai.closestShipId() > -1 and abs(ai.angleDiff(heading,ai.aimdir(0))) > 5):
    	change_heading(ai.aimdir(0))
    	
    # Wall Avoidance
    
    if((wall_feeler1 == wall_feeler2) and (wall_feeler1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(ai.angleDiff(heading, ai.angleAdd(tracking, 180)))
        print("Turning 1: ",ai.angleDiff(heading, ai.angleAdd(tracking, 180)))
        
    elif((wall_feeler1 < wall_feeler2) and (wall_feeler1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(ai.angleDiff(heading, ai.angleAdd(180, ai.angleAdd(-15,tracking))))
        if(ai.angleDiff(heading, ai.angleAdd(180, ai.angleAdd(-15,tracking))) < 30):
        	ai.thrust(1)
        print("Turning 2: ",ai.angleDiff(heading, ai.angleAdd(180, ai.angleAdd(-15,tracking))))
        
    elif((wall_feeler1 > wall_feeler2) and (wall_feeler1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(ai.angleDiff(heading, ai.angleAdd(180, ai.angleAdd(15,tracking))))
        if(ai.angleDiff(heading, ai.angleAdd(180, ai.angleAdd(15,tracking))) < 30):
        	ai.thrust(1)
        print("Turning 3: ",ai.angleDiff(heading, ai.angleAdd(180, ai.angleAdd(15,tracking))))
    	

ai.start(AI_loop, ["-name", "ExpertSystem", "-join", "localhost"])
